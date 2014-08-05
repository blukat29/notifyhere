from urllib import quote
from httplib import HTTPSConnection
import json
import time

import base
import tools
import secrets

class GithubApi(base.ApiBase):

    FAVICON_URL = "http://github.com/favicon.ico"

    def __init__(self):
        base.ApiBase.__init__(self, "github")
        self.state = ""
        self.token = ""

    def icon_url(self):
        return FAVICON_URL

    def oauth_link(self):
        self.state = str(int(time.time()))
        url  = "https://github.com/login/oauth/authorize"
        args = {
            "client_id":secrets.GITHUB_CLIENT_ID,
            "rediret_uri":secrets.BASE_REDIRECT_URL + "github",
            "scope":"notifications",
            "state":self.state,
        }
        return url + "?" + tools.encode_params(args)

    def oauth_callback(self, params):

        if 'state' not in params:
            return None
        if 'code' not in params:
            return None
        if params['state'] != self.state:
            return None

        args = {
            "client_id":secrets.GITHUB_CLIENT_ID,
            "client_secret":secrets.GITHUB_CLIENT_SECRET,
            "code":params['code'],
            "redirect_uri":secrets.BASE_REDIRECT_URL + "github",
        }
        body = tools.encode_params(args)
        headers = {
            'Accept':'application/json',
            'Content-Length':str(len(body))
        }

        conn = HTTPSConnection("github.com")
        conn.request("POST", "/login/oauth/access_token", body, headers)
        resp = conn.getresponse()

        try:
            self.token = json.loads(resp.read())['access_token']
            self.is_auth = True
        except (KeyError, ValueError):
            return None

    def _api_call(self, conn, job, args):
        url  = "/" + job + "?" + tools.encode_params(args)

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

    def update(self):
        conn = HTTPSConnection("api.github.com")
        args = {
            'access_token':self.token,
        }
        notis = self._api_call(conn, "notifications", args)

        result = {}

        for noti in notis:
            name = noti['repository']['full_name']
            if name in result: result[name] += 1
            else: result[name] = 1

        return result

    def logout(self):
        self.is_auth = False
        self.token = ""

    def __str__(self):
        return json.dumps(self.pack())
