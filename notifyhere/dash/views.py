from django.shortcuts import render, redirect
from django.http import HttpResponse

from api.tools import getApi
import api.slack
import api.github

def index(request):

    if request.method == 'POST':
        try:
            service = request.POST['service']
            agent = getApi(service)
            link = agent.oauth_link()
            request.session[service] = agent.pack()
            return redirect(link)
        except ValueError:
            return HttpResponse("Login to " + request.POST['service'] + " not ready.")

    if request.method == 'GET':
        services = ['slack']
        args = []
        for service in services:
            agent = getApi(service)
            agent.unpack(request.session.get(service))
            args.append(agent)
        return render(request, 'dash/index.html', {'services':args})

def auth(request, service=None):

    if 'code' in request.GET:
        agent = getApi(service)
        agent.unpack(request.session[service])
        agent.oauth_callback(request.GET)
        request.session[service] = agent.pack()
    else:
        return HttpResponse("ouch!")

    return redirect('/dash')

def ajax(request, service=None):

    try:
        agent = getApi(service)
        agent.unpack(request.session[service])
        noti = agent.update()
        result = [(name, str(noti[name])) for name in sorted(noti, key=noti.get, reverse=True)]
        return render(request, 'dash/noti.html', {'result':result})
    except ValueError:
        pass

    return render(request, 'dash/noti.html', {'result':None})
