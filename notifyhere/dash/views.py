from django.shortcuts import render, redirect
from django.http import HttpResponse

import secrets

from urllib import quote
from httplib import HTTPSConnection

BASE_REDIRECT_URL = "http://cert.kaist.in:8000/dash/auth/"

def slack_auth():
    url  = "https://slack.com/oauth/authorize"
    url += "?client_id=" + secrets.SLACK_CLIENT_ID
    url += "&redirect_uri=" + quote(BASE_REDIRECT_URL + "slack")
    url += "&scope=" + "read"
    return redirect(url)

def slack_access(code):
    url  = "/api/oauth.access"
    url += "?client_id=" + secrets.SLACK_CLIENT_ID
    url += "&client_secret=" + secrets.SLACK_CLIENT_SECRET
    url += "&code=" + code
    url += "&redirect_uri=" + quote(BASE_REDIRECT_URL + "slack")
    conn = HTTPSConnection("slack.com")
    conn.request("GET", url, "", {})
    return conn.getresponse().read()

def index(request):

    if request.method == 'GET':
        return render(request, 'dash/index.html', {})

    if request.method == 'POST':
        if request.POST['service'] == 'slack':
            return slack_auth()

def auth(request, service=None):
    output  = 'Thx! you authorized my access to your ' + str(service) + ' account'

    if 'error' in request.GET:
        output = 'Ouch! what did I do wrong? you did not authorize me..'
        return HttpResponse(output)

    elif 'code' in request.GET:
        output += '<br>The code was ' + request.GET['code']
        tok = slack_access(request.GET['code'])
        output += '<br>The token is ' + tok

    return HttpResponse(output)
