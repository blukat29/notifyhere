from urllib import quote
from httplib import HTTPSConnection
import json

import secrets

def auth_url():
    url  = "https://github.com/login/oauth/authorize"
    url += "?client_id=" + secrets.GITHUB_CLIENT_ID
    url += "&rediret_uri=" + quote(secrets.BASE_REDIRECT_URL + "github")
    url += "&scope=" + "notifications"
    url += "&state=" + "aaaa"
    return url

def access_token(code):
    body  =  "client_id=" + secrets.GITHUB_CLIENT_ID
    body += "&client_secret=" + secrets.GITHUB_CLIENT_SECRET
    body += "&code=" + code
    body += "&redirect_uri=" + quote(secrets.BASE_REDIRECT_URL + "github")

    headers = {
        'Accept':'application/json',
        'Content-Length':str(len(body))
    }

    conn = HTTPSConnection("github.com")
    conn.request("POST", "/login/oauth/access_token", body, headers)
    resp = conn.getresponse()

    return json.loads(resp.read())['access_token']

def github_api_call(conn, job, args):
    url  = "/" + job + "?"
    for key in args:
        url += key + "=" + args[key] + "&"
    url = url[:-1]

    headers = {
        'Accept':'application/vnd.github.v3+json',
        'User-Agent':'Python-2.7.6-httplib'
    }

    conn = HTTPSConnection("api.github.com")
    conn.request("GET", url, "", headers)
    resp = conn.getresponse()
    if resp.status != 200:
        return None

    try:
        return json.loads(resp.read())
    except ValueError:
        return None

def notifications(token):
    conn = HTTPSConnection("api.github.com")
    args = {
        'access_token' : token,
    }
    notis = github_api_call(conn, "notifications", args)

    result = {}

    for noti in notis:
        name = noti['repository']['full_name']
        if name in result: result[name] += 1
        else: result[name] = 1

    return result
