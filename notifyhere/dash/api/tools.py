from urllib import quote

from slack import SlackApi
from github import GithubApi
from gmail import GmailApi
from twitter import TwitterApi

def getAllApis():
    return ['slack','github','gmail','twitter']

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
    if service == 'twitter':
        return TwitterApi()
    raise ValueError("Unknown service name: " + service)

