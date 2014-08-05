from urllib import quote
from httplib import HTTPSConnection
import json
import time

import base
import tools
import secrets

class SlackApi(base.ApiBase):
    
    FAVICON_URL = "https://slack.com/favicon.ico"

    def __init__(self):
        base.ApiBase.__init__(self, "slack")
        self.state = ""
        self.token = ""

    def icon_url(self):
        return FAVICON_URL

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

    def _api_call(self, conn, job, args):
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
        result = self._api_call(conn, "oauth.access", args)

        if not result:
            return None
        if 'access_token' not in result:
            return None

        self.is_auth = True
        self.token = result['access_token']

        args = {
            'token':self.token,
        }
        result = self._api_call(conn, "auth.test", args)
        self.username = result['team'] + " " + result['user']

        conn.close()
        return self.token

    def update(self):

        conn = HTTPSConnection("slack.com")
        args = {
            'token':self.token,
        }
        channels = self._api_call(conn, "channels.list", args)

        result = {}

        for channel in channels['channels']:
            if channel['is_member']:
                args = {
                    'token':self.token,
                    'channel':channel['id'],
                }
                info = self._api_call(conn, "channels.info", args)

                name = '#' + channel['name']
                unread_count = info['channel']['unread_count']
                result[name] = unread_count

        return result

    def logout(self):
        self.is_auth = False
        self.token = ""

    def __str__(self):
        return json.dumps(self.pack())
