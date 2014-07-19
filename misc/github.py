import httplib, json

token = 'c913f84cd56c272641aea0ed24958a5b12fa65cf'

def github_call(conn, url, **kwargs):
    params = ""
    for key in kwargs:
        params += key + "=" + kwargs[key] + "&"

    if params != "":
        url = url + "?" + params[:-1]

    # Explicitly require Github API v3.
    headers = {
        'Authorization':'token ' + token,
        'Accept':'application/vnd.github.v3+json',
        'User-Agent':'python',
    }
    conn.request("GET",url,"",headers)
    
    print url

    resp = conn.getresponse()
    if resp.status == 200:
        return json.loads(resp.read())
    else:
        print resp.status, resp.reason
        print resp.read()
        return None

conn = httplib.HTTPSConnection("api.github.com")

result = github_call(conn, "/notifications")
for noti in result:
    print noti['repository']['full_name'], noti['subject']['title'], noti['reason'], noti['unread']


