import hmac
import hashlib
from urllib import quote
from pprint import pprint
from urlparse import parse_qsl
from httplib import HTTPSConnection
import time

# Implementation of the exmaple:
# https://dev.twitter.com/docs/auth/implementing-sign-twitter
# Correct signature from the example is F1Li3tvehgcraF8DMJ7OyxO4w9Y%3D

# With helps from:
# http://stackoverflow.com/questions/8338661/implementaion-hmac-sha1-in-python
# http://oauth.googlecode.com/svn/code/javascript/example/signature.html
# http://tools.ietf.org/html/draft-hammer-oauth-10#section-3.4.1.1
# https://github.com/leah/python-oauth

CONSUMER_KEY = "cChZNFj6T5R0TigYB9yd1w"
CONSUMER_SECRET = "L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg"
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
CALLBACK = "http://localhost/sign-in-with-twitter/"

### HELPER FUNCTIONS

def get_timestamp(): return str(int(time.time()))
def get_nonce(): return "ea9ec8429b68d6b77cd5600adbbb0456"

def escape(s): return quote(s, '')

def sign_request(secret, method, url, params):
    # Secret key for signing.
    key = secret + '&'

    # Preprocess params.
    params = [k+'='+params[k] for k in sorted(params)]
    params = '&'.join(params)
    params = escape(params)

    # Build base string.
    url = escape(url)
    base_str = '&'.join([method, url, params])

    # Sign with HMAC-SHA1
    hashed = hmac.new(key, base_str, hashlib.sha1)
    return hashed.digest().encode('base64').rstrip('\n')

### STAGE 1. Get Unauthorized Token.
### Uses CONSUMER_KEY and CONSUMER_SECRET to get request_token.
auth = {
    "oauth_callback":escape(CALLBACK),
    "oauth_consumer_key":CONSUMER_KEY,
    "oauth_nonce":get_nonce(),
    "oauth_signature_method":"HMAC-SHA1",
    "oauth_timestamp":get_timestamp(),
    "oauth_version":"1.0",
}

sign = sign_request(CONSUMER_SECRET, "POST", REQUEST_TOKEN_URL, auth)
auth['oauth_signature'] = escape(sign)

header = [k+'="'+v+'"' for k,v in auth.iteritems()]
header = ','.join(header)

print "\n[1-1] Request Sent:"
print "POST /oauth/request_token HTTP/1.1"
print "Host: api.twitter.com"
print "Authorization: OAuth " + header

conn = HTTPSConnection("api.twitter.com")
conn.request("POST", "/oauth/request_token", "", {"Authorization":"OAuth " + header})
resp = conn.getresponse()

request_dict = dict(parse_qsl(resp.read()))
request_token = request_dict['oauth_token']
request_secret = request_dict['oauth_token_secret']

print "\n[1-2] Response Got:"
print resp.status, resp.reason
pprint(request_dict)

### STAGE 2. Get Authorized.
### Uses REQUEST_TOKEN to browse to twitter's authorization page.

print "\n[2-1] Use your browser to go to this location."
print "https://api.twitter.com/oauth/authorize?oauth_token=" + request_token

verifier = raw_input("\nEnter the 'oauth_verifier' you received: ")

### STAGE 3. Convert to Access Token.
### Uses REQUEST_TOKEN, OAUTH_VERIFIER to get an ACCESS_TOKEN.

auth = {
    "oauth_consumer_key":CONSUMER_KEY,
    "oauth_timestamp":get_timestamp(),
    "oauth_nonce":get_nonce(),
    "oauth_version":"1.0",
    "oauth_token":request_token,
    "oauth_verifier":verifier,
    "oauth_signature_method":"HMAC-SHA1"
}

sign = sign_request(CONSUMER_SECRET, "GET", ACCESS_TOKEN_URL, auth)
auth['oauth_signature'] = escape(sign)

header = [k+'="'+v+'"' for k,v in auth.iteritems()]
header = ','.join(header)

print "\n[1-1] Request Sent:"
print "POST /oauth/access_token HTTP/1.1"
print "Host: api.twitter.com"
print "Authorization: OAuth " + header

conn.request("POST", "/oauth/access_token", "", {"Authorization":"OAuth " + header})
resp = conn.getresponse()

print resp.status, resp.reason
print resp.read()



