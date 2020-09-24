from json import load, dump

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
        return "/?u={0}".format(name)


    else:
        return open('form.html').read()