from django.shortcuts import render, redirect
from django.http import HttpResponse

import api.slack
import api.github

def index(request):

    if request.method == 'POST':
        if request.POST['service'] == 'slack':
            return redirect(api.slack.auth_url())
        if request.POST['service'] == 'github':
            return redirect(api.github.auth_url())
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

    if service == 'slack':
        if 'code' in request.GET:
            tok = api.slack.access_token(request.GET['code'])
            request.session['slack_token'] = tok

    if service == 'github':
        if 'code' in request.GET:
            tok = api.github.access_token(request.GET['code'])
            request.session['github_token'] = tok

    return redirect('/dash')

def ajax(request, service=None):

    if service == 'slack':
        tok = request.session.get('slack_token')
        noti = api.slack.notifications(tok)
        result = [(name, str(noti[name])) for name in sorted(noti, key=noti.get, reverse=True)]
        return render(request, 'dash/noti.html', {'result':result})

    if service == 'github':
        tok = request.session.get('github_token')
        noti = api.github.notifications(tok)
        result = [(name, str(noti[name])) for name in sorted(noti, key=noti.get, reverse=True)]
        return render(request, 'dash/noti.html', {'result':result})

    return render(request, 'dash/noti.html', {'result':None})
