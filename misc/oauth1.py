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

CONSUMER_KEY = "cChZNFj6T5R0TigYB9yd1w"
CONSUMER_SECRET = "L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg"
URL = "https://api.twitter.com/oauth/request_token"
CALLBACK = "http://localhost/sign-in-with-twitter/"

### STAGE 1. Get Unauthorized Token.
### Uses CONSUMER_KEY and CONSUMER_SECRET to get request_token.

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

auth = {
    "oauth_callback":escape(CALLBACK),
    "oauth_consumer_key":CONSUMER_KEY,
    "oauth_nonce":get_nonce(),
    "oauth_signature_method":"HMAC-SHA1",
    "oauth_timestamp":get_timestamp(),
    "oauth_version":"1.0",
}

sign = sign_request(CONSUMER_SECRET, "POST", URL, auth)

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

print "\n[2-1] Use your browser to go to this location."
print "https://api.twitter.com/oauth/authorize?oauth_token=" + request_token

