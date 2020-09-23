from http.server import HTTPServer, BaseHTTPRequestHandler
from inspect import getmembers
import json
from urllib.parse import parse_qs
import re
from os.path import join, dirname, basename, exists, isfile
from pathlib import Path
import sys

workingDir = Path().absolute()

class Server(BaseHTTPRequestHandler):
    def parseForm(self, content):
        return parse_qs(content.decode('utf-8'))

    def parseURL(self):
        global workingDir
        if self.path=="/":
            fp = p = workingDir
        else:
            fp = join(workingDir, self.path[1:])
            p = dirname(fp)
            print(fp)
        if not exists(p):
            return {"type": 404}
        if isfile(fp):
            settings = json.load(open(join(workingDir, "settings.json")))
            d = self.path[1:].split('/')[0]
            if not (d in settings['static_dirs'] or d in settings['media_dirs']):
                return {'type': 403}
            return {
                "type": "file",
                "content": open(fp, 'rb').read()
            }
        try:
            urls = json.load(open(
                join(p, "urls.json")
            ))
        except FileNotFoundError:
            return {'type': 404}
        if not (baseName := basename(self.path)) in urls:
            return {'type': 404}
        viewName = urls[baseName]
        sys.path.append(
            p
        )
        try:
            import views
            resp = {'type': 'view', 
            'view': None,
            'data': None
            }
            for m in getmembers(views):
                if m[0] == viewName:
                    resp['view'] = m[1]
                    if '?' in self.path:
                        resp['data'] = parse_qs(
                            self.path.split('?')[1]
                        )
                    return resp

        except ModuleNotFoundError:
            return {'type':404}

    def do_GET(self):
        query = self.parseURL()
        if query['type'] == 404:
            content = "404 page not found".encode('utf-8')
            if exists((path404:=join(workingDir, "404.html"))):
                content = open(path404).read().encode('utf-8')
            self.send_response(404)
        elif query['type'] == 403:
            content = "Error 403 forbidden".encode('utf-8')
            self.send_response(403)
        elif query['type'] == 'file':
            content = query['content']
            self.send_response(200)
        else:
            content = query['view']({'method': 'GET', 'queries': query['data']}).encode('utf-8')
            self.send_response(200)

        self.end_headers()
        self.wfile.write(content)
        

    def do_POST(self):
        query = self.parseURL()
        if query['type'] == 404:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', "/404")
        else:
            length = int(self.headers.get('content-length'))
            data = self.parseForm(self.rfile.read(length))
            response = query['view']({'data': data, 'method': 'POST'})
            self.send_response(301)
            self.send_header("content-type", "text/html")
            self.send_header('Location', response)

        self.end_headers()