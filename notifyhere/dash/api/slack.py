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

def slack_api_call(conn, job, args):
    url = "/api/" + job + "?"
    for key in args:
        url += key + "=" + args[key] + "&"
    url = url[:-1]

    conn.request("GET", url, "", {})
    resp = conn.getresponse()
    if resp.status != 200:
        return None

    try:
        return json.loads(resp.read())
    except ValueError:
        return None

def access_token(code):
    conn = HTTPSConnection("slack.com")
    args = {
        'client_id' : secrets.SLACK_CLIENT_ID,
        'client_secret' : secrets.SLACK_CLIENT_SECRET,
        'code' : code,
        'redirect_uri' : quote(BASE_REDIRECT_URL + "slack"),
    }
    result = slack_api_call(conn, "oauth.access", args)

    if result:
        if 'access_token' in result:
            return result['access_token']
    return None

def notifications(token):
    conn = HTTPSConnection("slack.com")
    args = {
        'token' : token,
    }
    channels = slack_api_call(conn, "channels.list", args)

    result = {}

    for channel in channels['channels']:
        if channel['is_member']:
            args = {
                'token' : token,
                'channel' : channel['id'],
            }
            info = slack_api_call(conn, "channels.info", args)

            result[channel['name']] = info['channel']['unread_count']

    return result
