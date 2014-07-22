from urllib import quote
from httplib import HTTPSConnection
import json

import base
import tools
import secrets

class SlackApi(base.ApiBase):
    @staticmethod
    def oauth_link():
        url = "https://slack.com/oauth/authorize"
        args = {
            "client_id":secrets.SLACK_CLIENT_ID,
            "redirect_uri":secrets.BASE_REDIRECT_URL+"slack",
            "scope":"read",
        }
        return url + "?" + tools.encode_params(args)

    @staticmethod
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

    @staticmethod
    def access_token(code):
        conn = HTTPSConnection("slack.com")
        args = {
            'client_id' : secrets.SLACK_CLIENT_ID,
            'client_secret' : secrets.SLACK_CLIENT_SECRET,
            'code' : code,
            'redirect_uri' : quote(secrets.BASE_REDIRECT_URL + "slack"),
        }
        result = SlackApi.slack_api_call(conn, "oauth.access", args)

        if result:
            if 'access_token' in result:
                return result['access_token']
        return None

    @staticmethod
    def notifications(token):
        conn = HTTPSConnection("slack.com")
        args = {
            'token' : token,
        }
        channels = SlackApi.slack_api_call(conn, "channels.list", args)

        result = {}

        for channel in channels['channels']:
            if channel['is_member']:
                args = {
                    'token' : token,
                    'channel' : channel['id'],
                }
                info = SlackApi.slack_api_call(conn, "channels.info", args)

                name = '#' + channel['name']
                unread_count = info['channel']['unread_count']
                result[name] = unread_count

        return result
