import httplib, json

t = 'xoxp-2160778816-2162067512-2465014375-3e32f8'

def slack_call(conn, job, **kwargs):
    """
    Return the result of GET https://slack.com/api/<JOB>?k1=v1&k2=v2
    JOB can be like 'channels.list' or 'search.messages'
    other arguments are passed through KWARGS.
    """
    url = "/api/" + job + "?"
    for key in kwargs:
        url += key + "=" + kwargs[key] + "&"
    if url[-1] == '&':
        url = url[:-1]
    
    conn.request("GET",url,"",{})
    resp = conn.getresponse()
    if resp.status == 200:
        return json.loads(resp.read())
    else:
        return None

conn = httplib.HTTPSConnection("slack.com")

result = slack_call(conn, "channels.list", token=t)
channels = result['channels']

for channel in channels:
    if channel['is_member']:
        result = slack_call(conn, "channels.info", token=t, channel=channel['id'])
        print channel['name'], result['channel']['unread_count']


