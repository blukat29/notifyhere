from httplib import HTTPSConnection
from urllib import quote
import json
import imaplib

url  = "https://accounts.google.com"
url += "/o/oauth2/auth"
url += "?response_type=code"
url += "&client_id=" + CLIENT_ID
url += "&redirect_uri=" + REDIRECT_URL
url += "&scope=" + quote("email https://mail.google.com/")

print url

code = raw_input("Input code: ")

conn = HTTPSConnection("accounts.google.com")

param  =  "grant_type=authorization_code"
param += "&code=" + code
param += "&client_id=" + CLIENT_ID
param += "&client_secret=" + CLIENT_SECRET
param += "&redirect_uri=" + REDIRECT_URL

conn.request("POST","/o/oauth2/token",param,{'Content-Type':'application/x-www-form-urlencoded'})
data = conn.getresponse().read()
print data
tok = json.loads(data)['access_token']

conn.close()

mail = imaplib.IMAP4_SSL("imap.gmail.com")
auth = "user="+EMAIL+"\1auth=Bearer "+tok+"\1\1"
mail.authenticate('XOAUTH2', lambda x: auth)
mail.select('INBOX')

ret, mailboxes = mail.list()
print ret
print mailboxes

mail.close()
mail.logout()


