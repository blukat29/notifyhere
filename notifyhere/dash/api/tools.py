from urllib import quote

from slack import SlackApi
from github import GithubApi
from gmail import GmailApi

def getAllApis():
    return ['slack','github','gmail']

def encode_params(args):
    args = {k: quote(v) for k,v in args.iteritems()}
    args = [k + "=" + v for k,v in args.iteritems()]
    return '&'.join(args)

def getApi(service):
    if service == 'slack':
        return SlackApi()
    if service == 'github':
        return GithubApi()
    if service == 'gmail':
        return GmailApi()
    raise ValueError("Unknown service name: " + service)

