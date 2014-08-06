from httplib import HTTPSConnection
import json
import imaplib
import re

import base
import tools
import secrets

class GmailApi(base.ApiBase):

    list_re = re.compile(r'\((.+)\) "(.+)" "(.+)"')

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
            "scope":"https://mail.google.com/ https://www.googleapis.com/auth/userinfo.email",
            "approval_prompt":"force",
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

        conn.close()

        conn = HTTPSConnection("www.googleapis.com")
        conn.request("GET","/oauth2/v1/tokeninfo?alt=json&access_token="+self.token,"",{})
        resp = conn.getresponse()
        self.username = json.loads(resp.read())['email']

    def update(self):
        auth = "user=%s\1auth=Bearer %s\1\1" % (self.username, self.token)
        
        m = imaplib.IMAP4_SSL("imap.gmail.com")
        m.authenticate("XOAUTH2", lambda x: auth)

        status, raw_list = m.list()
        boxes = []
        for line in raw_list:
            attr, root, raw_name = GmailApi.list_re.search(line).groups()
            if "Noselect" in attr:
                continue
            decoded_name = raw_name.replace("&","+").decode("utf-7")
            boxes.append((raw_name, decoded_name))

        noti = {}
        for box in boxes:
            raw_name, decoded_name = box
            
            status, result = m.select(raw_name)
            total = int(result[0])

            status, result = m.search(None, "(UNSEEN)")
            unseen = len(result[0].split())
            
            noti[decoded_name] = unseen

        m.close()
        m.logout()
        return noti

    def logout(self):
        self.is_auth = False
        self.token = ""

