import json

class ApiBase:

    def __init__(self, name):
        self.name = name
        self.is_auth = False
        self.username = ""

    def icon_url(self):
        raise NotImplementedError

    def oauth_link(self):
        raise NotImplementedError

    def oauth_callback(self, params):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def pack(self):
        return self.__dict__

    def unpack(self, data):
        if data:
            self.__dict__.update(data)
        return self

    def __str__(self):
        return "ApiBase " + str(self.__dict__) 
