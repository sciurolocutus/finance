import requests

class AuthClient:
    def __init__(self, baseurl):
        self.baseurl = baseurl + '/auth'

    def getAuth(self, username, password):
        headers={'Content-Type': 'application/json'}
        body = {'username': username, 'password': password}
        resp = requests.post("{0}".format(self.baseurl), json=body)
        resp.raise_for_status()
        return resp.json()['access_token']
