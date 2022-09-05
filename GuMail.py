import requests
import json


class GuMail:
    def __init__(self, proxy):
        self.proxy = proxy
        self.ip = proxy.split(':')[0]
        self.s  = requests.Session()
        self.id = ''

    def check_mail(self):
        headers = {
            'Cookie': 'PHPSESSID=ABC1234'
        }
        payload = {
            'f': 'check_email',
            'ip': self.ip,
            'agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G955N Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
            'seq': self.id

        }

        r = self.s.get(url='http://api.guerrillamail.com/ajax.php', headers=headers,params=payload, proxies={'http': 'http://' + self.proxy, 'http': 'http://' + self.proxy})
        code = r.json()['list'][0]['mail_subject'].split(' ')[0]
        print(code)
        return code

    def get_mail(self):
        headers = {
            'Cookie': 'PHPSESSID=ABC1234'
        }
        payload = {
            'f': 'get_email_address',
            'ip': self.ip,
            'agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G955N Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'

        }

        r = self.s.get(url='http://api.guerrillamail.com/ajax.php', headers=headers,params=payload, proxies={'http': 'http://' + self.proxy, 'http': 'http://' + self.proxy})
        x = json.loads(r.text)
        email = x['email_addr']
        id = x['sid_token']
        self.id = id
        # hash.append(self.s)
        return email
    