from django.shortcuts import render, redirect
from django.http import HttpResponse

import api.slack

def index(request):

    if request.method == 'POST':
        if request.POST['service'] == 'slack':
            return redirect(api.slack.auth_url())

    if request.method == 'GET':
        tok = request.session.get('slack_token')
        return render(request, 'dash/index.html', {})

def auth(request, service=None):

    if service == 'slack':
        if 'code' in request.GET:
            tok = api.slack.access_token(request.GET['code'])
            request.session['slack_token'] = tok

    return redirect('/dash')

def ajax(request, service=None):

    if service == 'slack':
        tok = request.session.get('slack_token')
        noti = api.slack.notifications(tok)
        result = [(name, str(noti[name])) for name in sorted(noti, key=noti.get)]
        return render(request, 'dash/noti.html', {'result':result})
