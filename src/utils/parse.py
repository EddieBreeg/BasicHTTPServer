from inspect import getmembers
import json
from urllib.parse import parse_qs, unquote
import re
from os.path import join, dirname, basename, exists, isfile
import sys

def parseForm(content):
    '''Parses the POST request to get the data'''
    for k in (data:=parse_qs(content.decode('utf-8'))):
        data[k] = data[k][0]
    return data


def parseURL(request, workingDir):     
    """        
    Parses the request url to create the appropriate response
    """
    # generating the full target path (fp) and its parent (p)
    if request.path=="/" or request.path.startswith('/?'):
        fp = p = workingDir
        base = ""
    elif request.path=="/500":
        # handle error 500
        return {'type': 500}
    else:
        fp = join(workingDir, request.path[1:].split('?')[0])
        p = dirname(fp)
        base = basename(fp)
        print(fp)
    # if the target folder doesn't exist, 404 error
    if not exists(p):
        print("{0} doesn't exist!")
        return {"type": 404}
    if isfile(fp):
        # if the full path corresponds to a file, we check if said file is accessible
        settings = json.load(open(join(workingDir, "settings.json")))
        d = request.path[1:].split('/')[0]
        if not (d in settings['static_dirs'] or d in settings['media_dirs']):
            # if the file is a static or media file, access is forbidden
            return {'type': 403}
        # else we return the bytes content
        return {
            "type": "file",
            "content": open(fp, 'rb').read()
        }
    # if the targer isn't a file we try to load the url pattern
    try:
        urls = json.load(open(
            join(p, "urls.json")
        ))
    except FileNotFoundError:
        # if no pattern is found, throw 404
        return {'type': 404}
    if not base in urls:
        print(base)
        # if the url doesn't correspond to any view, throw 404
        return {'type': 404}
    viewName = urls[base]
    # adding p to sys.path to import the views module
    sys.path.append(
        p
    )
    try:
        import views
        resp = {'type': 'view', 
        'view': None,
        'data': None
        }
        # check if the module contains the target view
        for m in getmembers(views):
            if m[0] == viewName:
                resp['view'] = m[1]
                # get the queries data
                if '?' in request.path:
                    data = parse_qs(
                        request.path.split('?')[1]
                    )
                    for k in data:
                        data[k] = unquote(data[k][0])
                    resp['data'] = data
                return resp
    except ModuleNotFoundError:
        return {'type':404}