from urllib import quote
from httplib import HTTPSConnection
import json

import secrets

def auth_url():
    url  = "https://slack.com/oauth/authorize"
    url += "?client_id=" + secrets.SLACK_CLIENT_ID
    url += "&redirect_uri=" + quote(secrets.BASE_REDIRECT_URL + "slack")
    url += "&scope=" + "read"
    return url

def access_token(code):
    url  = "/api/oauth.access"
    url += "?client_id=" + secrets.SLACK_CLIENT_ID
    url += "&client_secret=" + secrets.SLACK_CLIENT_SECRET
    url += "&code=" + code
    url += "&redirect_uri=" + quote(BASE_REDIRECT_URL + "slack")
    conn = HTTPSConnection("slack.com")
    conn.request("GET", url, "", {})
    resp = conn.getresponse()
    try:
        return json.loads(resp.read())['access_token']
    except (KeyError, ValueError):
        return None

