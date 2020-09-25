from http.server import HTTPServer, BaseHTTPRequestHandler
from .parse import *
from pathlib import Path
import traceback
from cgi import parse_multipart, parse_header

workingDir = Path().absolute()

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        # retrieve the request by parsing the URL, and transfer it to the correct view
        request = parseURL(self, workingDir)
        if request['type'] == 404:
            # if the page isn't found, raise a 404 error
            content = "404 page not found".encode('utf-8')
            if exists((path404:=join(workingDir, "404.html"))):
                content = open(path404).read().encode('utf-8')
            self.send_response(404)
        elif request['type'] == 403:
            # forbidden access
            content = "Error 403 forbidden".encode('utf-8')
            self.send_response(403)
        elif request['type'] == 500:
            content = "500 Server error".encode()
            if exists((path500:=join(workingDir, '500.html'))):
                content = open(path500).read().encode('utf-8')
            self.send_response(500)
        elif request['type'] == 'file':
            # if the target is a file, just display the content
            content = request['content']
            self.send_response(200)
        else:
            # if the target is a view, call it by passing the request data as an argument
            content = request['view']({'method': 'GET', 'queries': request['data']}).encode('utf-8')
            self.send_response(200)

        self.end_headers()
        # send the content back to the client
        self.wfile.write(content)
        

    def do_POST(self):
        # retrieve the request by parsing the URL, and transfer it to the correct view
        request = parseURL(self, workingDir)
        # print(request)
        if request['type'] == 404:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', "/404")
        else:
            # read the content of the request
            length = int(self.headers.get('content-length'))
            ctype, pdict = parse_header(self.headers.get('content-type'))
            if ctype.startswith('multipart/form-data'):
                pdict['boundary'] = pdict['boundary'].encode('ascii')
                data = parse_multipart(self.rfile, pdict)
            else:
                data = parseForm(self.rfile.read(length))
            # transfer the request to the correct view
            try:
                self.send_response(301)
                response = request['view']({'data': data, 'method': 'POST'})
                self.send_header('Location', response)
                self.send_header("content-type", "text/html")
            except Exception:
                # if something goes wrong
                self.send_response(500)
                self.send_header("content-type", "text/html")
                self.send_header("Location", "/500")
                print(traceback.format_exc())

        self.end_headers()