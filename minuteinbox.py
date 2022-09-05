import requests,json,random,re
from time import sleep as s
from bs4 import BeautifulSoup

class MinuteInBox(object):
	def __init__(self,proxy):
		self.pers_UA  = random.choice(tuple(set(re.sub('\r\n', '\n', requests.get('http://pastebin.com/raw/VtUHCwE6').text).splitlines())))
		self.min_sess = requests.Session()
		self.proxy    = proxy
		self.minuteinbox_headers = {
			'User-Agent': self.pers_UA,
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'en-US;q=0.7,en;q=0.3',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive',
			'Referer': 'https://www.minuteinbox.com/',
		}

	def parse_html(self,input):return(' '.join(BeautifulSoup(input, 'html.parser').stripped_strings))

	def create_email(self):
		global minuteinbox_cookies
		r = self.min_sess.get('https://www.minuteinbox.com/index/index', headers=self.minuteinbox_headers, proxies={'http': 'http://' + self.proxy, 'https': 'http://' + self.proxy})
		minuteinbox_email=json.loads(r.content.decode('utf-8-sig'))['email']
		minuteinbox_cookies = {'MI': minuteinbox_email,}
		split_email=minuteinbox_email.split('@')[0].split('.')
		first_name=split_email[0].capitalize()
		last_name=split_email[1].capitalize()
		company_suffix=['Solutions','Software Inc.','Technology Inc.','Technologies','Computers','Systems','IT','Connect','Digital','Tech','PC Professionals','Technology Partners','Group','Tech Services','& Co','Labs','PLLC','Tech','Corp.','LLC','LLP','LP','P.C','Incorporated','S.A.S.','GmbH & Co. KG','AG & Co. KG','SE & Co. KGaA']
		company_name=str(split_email[1][:random.randint(2,5)].capitalize()+split_email[0][:2]+' '+random.choice(company_suffix))
		return({'email': minuteinbox_email, 'fname':first_name, 'lname':last_name, 'company': company_name})

	def get_inbox(self):
		r = self.min_sess.get('https://www.minuteinbox.com/index/refresh', headers=self.minuteinbox_headers, cookies=minuteinbox_cookies, proxies={'http': 'http://' + self.proxy, 'https': 'http://' + self.proxy})
		try:
			email_status=json.loads(self.parse_html(r.content.decode('utf-8-sig')))[0] #might bug here if there's weird special characters
		except Exception as e:
			print('\nERROR: Empty response from MinuteInbox, most likely caused by a bad character in the E-Mail\n')
			print(e)
			s(10)
			exit()
		if email_status['id'] == 2:
			return(email_status['predmet'])


