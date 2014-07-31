from urllib import quote
from httplib import HTTPSConnection
import json
import time

import base
import tools
import secrets

class SlackApi(base.ApiBase):

    def __init__(self):
        self.is_auth = False
        self.name = "slack"
        self.state = ""
        self.token = ""
        self.icon = "https://slack.com/favicon.ico"

    def oauth_link(self):
        self.state = str(int(time.time()))
        url = "https://slack.com/oauth/authorize"
        args = {
            "client_id":secrets.SLACK_CLIENT_ID,
            "redirect_uri":secrets.BASE_REDIRECT_URL+"slack",
            "scope":"read",
            "state":str(self.state),
        }
        return url + "?" + tools.encode_params(args)

    @staticmethod
    def slack_api_call(conn, job, args):
        url = "/api/" + job + "?" + tools.encode_params(args)
        conn.request("GET", url, "", {})
        resp = conn.getresponse()
        if resp.status != 200:
            return None
        try:
            return json.loads(resp.read())
        except ValueError:
            return None

    def oauth_callback(self, params):

        if 'error' in params:
            return None
        if 'state' not in params:
            return None
        if 'code' not in params:
            return None
        if params['state'] != self.state:
            return None

        conn = HTTPSConnection("slack.com")
        args = {
            'client_id':secrets.SLACK_CLIENT_ID,
            'client_secret':secrets.SLACK_CLIENT_SECRET,
            'code':params['code'],
            'redirect_uri':secrets.BASE_REDIRECT_URL + "slack",
        }
        result = SlackApi.slack_api_call(conn, "oauth.access", args)

        if not result:
            return None
        if 'access_token' not in result:
            return None

        self.is_auth = True
        self.token = result['access_token']
        return self.token

    def update(self):

        conn = HTTPSConnection("slack.com")
        args = {
            'token':self.token,
        }
        channels = SlackApi.slack_api_call(conn, "channels.list", args)

        result = {}

        for channel in channels['channels']:
            if channel['is_member']:
                args = {
                    'token':self.token,
                    'channel':channel['id'],
                }
                info = SlackApi.slack_api_call(conn, "channels.info", args)

                name = '#' + channel['name']
                unread_count = info['channel']['unread_count']
                result[name] = unread_count

        return result

    def pack(self):
        return {
            'is_auth':self.is_auth,
            'name':self.name,
            'state':self.state,
            'token':self.token,
        }

    def unpack(self, data):
        if data:
            self.is_auth = data.get('is_auth',False)
            self.state = data.get('state',"")
            self.token = data.get('token',"")

    def __str__(self):
        return json.dumps(self.pack())
