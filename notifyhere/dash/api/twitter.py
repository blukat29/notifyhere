from urllib import quote
from httplib import HTTPSConnection
from urlparse import parse_qsl
import json
import time
import hmac
import hashlib

import base
import tools
import secrets

class TwitterApi(base.ApiBase):

    def __init__(self):
        self.is_auth = False
        self.name = "twitter"
        self.token = ""
        self.username = ""

    def icon_url(self):
        return "https://www.twitter.com/favicon.ico"

    def oauth_link(self):
        auth = {
            "oauth_callback":TwitterApi.escape(secrets.BASE_REDIRECT_URL + "twitter"),
            "oauth_consumer_key":secrets.TWITTER_CONSUMER_KEY,
            "oauth_nonce":TwitterApi.get_nonce(),
            "oauth_signature_method":"HMAC-SHA1",
            "oauth_timestamp":TwitterApi.get_timestamp(),
            "oauth_version":"1.0",
        }
        auth_header = TwitterApi.sign_request(secrets.TWITTER_CONSUMER_SECRET, None,
                                     "POST", "https://api.twitter.com/oauth/request_token",
                                     auth)
        conn = HTTPSConnection("api.twitter.com")
        conn.request("POST", "/oauth/request_token", "", {"Authorization":auth_header})
        resp = conn.getresponse()

        d = dict(parse_qsl(resp.read()))
        request_token = d['oauth_token']
        request_secret = d['oauth_token_secret']

        return "https://api.twitter.com/oauth/authorize?oauth_token=" + request_token

    @staticmethod
    def escape(s):
        return quote(s, "")

    @staticmethod
    def get_timestamp():
        return str(int(time.time()))

    @staticmethod
    def get_nonce():
        return "ea9ec8429b68d6b77cd5600adbbb0456"

    @staticmethod
    def calculate_sign(consumer_secret, token_secret, method, url, params):
        # Secret key for signing.
        key = consumer_secret + '&'
        if token_secret: key += token_secret

        # Preprocess params.
        params = [k+'='+params[k] for k in sorted(params)]
        params = '&'.join(params)

        # Build base string.
        params = TwitterApi.escape(params)
        url = TwitterApi.escape(url)
        base_str = '&'.join([method, url, params])

        # Sign with HMAC-SHA1
        hashed = hmac.new(key, base_str, hashlib.sha1)
        return hashed.digest().encode('base64').rstrip('\n')

    @staticmethod
    def sign_request(consumer_secret, token_secret, method, url, auth):
        sign = TwitterApi.calculate_sign(consumer_secret, token_secret, method, url, auth)
        auth['oauth_signature'] = TwitterApi.escape(sign)

        header = [k+'="'+v+'"' for k,v in auth.iteritems()]
        header = ','.join(header)

        return "OAuth " + header

