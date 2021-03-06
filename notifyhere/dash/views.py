from django.shortcuts import render, redirect
from django.http import HttpResponse

from api.tools import getAllApis, getApi

def index(request):
    services = getAllApis()
    args = []
    for service in services:
        agent = getApi(service).unpack(request.session.get(service))
        args.append(agent)
    return render(request, 'dash/index.html', {'services':args})

def auth_redirect(request, service=None):
    agent = getApi(service)
    link = agent.oauth_link()
    request.session[service] = agent.pack()
    return redirect(link)

def auth_callback(request, service=None):
    agent = getApi(service).unpack(request.session[service])
    agent.oauth_callback(request.GET)
    request.session[service] = agent.pack()
    return render(request, 'dash/callback.html', {'service':service, 'success':agent.is_auth})

def auth_logout(request, service=None):
    agent = getApi(service).unpack(request.session[service])
    agent.logout()
    request.session[service] = agent.pack()
    return redirect('/dash')

def ajax(request, service=None):
    try:
        agent = getApi(service).unpack(request.session[service])
        noti = agent.update()
        result = [(name, str(noti[name])) for name in sorted(noti, key=noti.get, reverse=True)]
        return render(request, 'dash/noti.html', {'result':result})
    except ValueError:
        pass

    return render(request, 'dash/noti.html', {'result':None})
