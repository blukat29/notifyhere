from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib import quote

BASE_REDIRECT_URL = "http://cert.kaist.in:8000/dash/auth/"
SLACK_CLIENT_ID = "2160778816.2472356570"

def slack_auth():
    url  = "https://slack.com/oauth/authorize"
    url += "?client_id=" + SLACK_CLIENT_ID
    url += "&redirect_uri=" + quote(BASE_REDIRECT_URL + "slack")
    return redirect(url)

def index(request):

    if request.method == 'GET':
        return render(request, 'dash/index.html', {})

    if request.method == 'POST':
        if request.POST['service'] == 'slack':
            return slack_auth()

def auth(request, service=None):
    output  = 'Thx! you authorized my access to your ' + str(service) + ' account'

    if 'code' in request.GET:
        output += '<br>The code was ' + request.GET['code']

    return HttpResponse(output)
