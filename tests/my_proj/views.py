from json import load, dump
from imghdr import what
from datetime import datetime

def index(request):
    if request['queries'] is None:
        return open("index.html").read()
    return str(request['queries'])

def formTest(request):
    if request['method'] == 'POST':
        users = load(open('users.json'))
        name = request['data']['name']
        age = int(request['data']['age'])
        users[name] = age
        with open('users.json', 'w') as out:
            dump(users, out, indent=4)
        return "/"

    else:
        return open('form.html').read()

def fileForm(request):
    if request['method'] == 'GET':
        return open('file-form.html').read()
    content = request['data']['file'][0]
    imageType = what(None, h=content)
    if imageType is None:
        return '/file-form?error=wrong-type'
    time = datetime.utcnow()
    name = '{0}_{1}_{2}_{3}_{4}_{5}.{6}'.format(
        time.day, time.month, time.year, time.hour, time.minute, time.second, imageType
    )
    with open('media/{0}'.format(name), 'wb') as output:
        output.write(content)
    return '/media/{0}'.format(name)