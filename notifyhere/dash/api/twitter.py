from urllib import quote
from httplib import HTTPSConnection
import json

import base
import tools
import secrets

class TwitterApi(base.ApiBase):

    def __init__(self):
        self.is_auth = False
        self.name = "twitter"
        self.token = ""
        self.username == ""

