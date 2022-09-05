import requests
from random_username.generate import generate_username
import json
class MailTm:
    def __init__(self, proxy):
        self.domain = 'knowledgemd.com'
        self.user   = '{}@{}'.format((generate_username(1)[0]).lower(), self.domain)
        self.password = (generate_username(1)[0]).lower()
        self.proxy  = proxy
        self.url    = 'https://api.mail.tm'
        
    def get_email(self, make_account):
        if make_account:
            print('Getting email...')
            endpoint = 'accounts'
        else:
            endpoint = 'token'
        account = {"address": self.user, "password": self.password}
        headers = {
            "accept": "application/ld+json",
            "Content-Type": "application/json"
        }
        r = requests.post(url="{}/{}".format(self.url, endpoint),
                          data=json.dumps(account), headers=headers)
        if r.status_code not in [200, 201]:
            return False
        if make_account:
            return self.user
        else:
            return r.json()['token']
    
    def get_code(self):
        token  = self.get_email(False)
        auth_headers = {
            "accept": "application/ld+json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
        r = requests.get("{}/messages?page={}".format(self.url, 1),
                         headers=auth_headers)
        code = r.json()["hydra:member"][0]['subject'].split(' ')[0]
        return code

