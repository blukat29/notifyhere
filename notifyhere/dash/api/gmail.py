from httplib import HTTPSConnection
import json

import base
import tools
import secrets

class GmailApi(base.ApiBase):

    def __init__(self):
        base.ApiBase.__init__(self, "gmail")
        self.token = ""

    def icon_url(self):
        return "https://mail.google.com/favicon.ico"
    
    def oauth_link(self):
        url = "https://accounts.google.com/o/oauth2/auth"
        args = {
            "response_type":"code",
            "client_id":secrets.GMAIL_CLIENT_ID,
            "redirect_uri":secrets.BASE_REDIRECT_URL + "gmail",
            "scope":"https://mail.google.com/",
        }
        return url + "?" + tools.encode_params(args)
    
    def oauth_callback(self, params):

        if 'code' not in params:
            return None

        conn = HTTPSConnection("accounts.google.com")
        body = tools.encode_params({
            "grant_type":"authorization_code",
            "code":params['code'],
            "client_id":secrets.GMAIL_CLIENT_ID,
            "client_secret":secrets.GMAIL_CLIENT_SECRET,
            "redirect_uri":secrets.BASE_REDIRECT_URL + "gmail",
        })
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
        }
        conn.request("POST", "/o/oauth2/token", body, headers)

        resp = conn.getresponse()
        try:
            self.token = json.loads(resp.read())['access_token']
            self.is_auth = True
        except (KeyError, ValueError):
            return None

    def logout():
        self.is_auth = False
        self.token = ""

