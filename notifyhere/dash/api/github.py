from urllib import quote
from httplib import HTTPSConnection
import json
import time

import base
import tools
import secrets

class GithubApi(base.ApiBase):

    def __init__(self):
        self.is_auth = False
        self.name = "github"
        self.state = ""
        self.token = ""

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

    @staticmethod
    def github_api_call(conn, job, args):
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
        notis = GithubApi.github_api_call(conn, "notifications", args)

        result = {}

        for noti in notis:
            name = noti['repository']['full_name']
            if name in result: result[name] += 1
            else: result[name] = 1

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
