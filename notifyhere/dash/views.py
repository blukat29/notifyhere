from django.shortcuts import render, redirect
from django.http import HttpResponse

from api.tools import getApi
import api.slack
import api.github

def index(request):

    if request.method == 'POST':
        try:
            link = getApi(request.POST['service']).oauth_link()
            return redirect(link)
        except ValueError:
            return HttpResponse("Login to " + request.POST['service'] + " not ready.")

    if request.method == 'GET':
        services = ['slack','github']
        args = []
        for service in services:
            tok = request.session.get(service + '_token')
            if tok:
                args.append((service, True))
            else:
                args.append((service, False))
        return render(request, 'dash/index.html', {'services':args})

def auth(request, service=None):

    if 'code' in request.GET:
        tok = getApi(service).access_token(request.GET['code'])
        request.session[service+'_token'] = tok

    return redirect('/dash')

def ajax(request, service=None):

    try:
        tok = request.session.get(service+'_token')
        noti = getApi(service).notifications(tok)
        result = [(name, str(noti[name])) for name in sorted(noti, key=noti.get, reverse=True)]
        return render(request, 'dash/noti.html', {'result':result})
    except ValueError:
        pass

    return render(request, 'dash/noti.html', {'result':None})
