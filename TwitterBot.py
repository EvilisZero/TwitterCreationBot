
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import numpy as np
import pandas as pd
import faker
from bs4 import BeautifulSoup
import re
import undetected_chromedriver as uc
from tempMail2 import TempMail
import warnings
import requests
import random
from requests_oauthlib import OAuth1
import random
import pandas as pd
import time
import threading
from glob import glob
import copy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import imaplib
import email
import outlook
from detect import run
# from smsactivateru import Sms, SmsService, GetNumber, SmsTypes


class TwitterBot:
    warnings.filterwarnings("ignore")
 
    def set_proxy(self):
        options = uc.ChromeOptions()
        if self.Proxies:
            options.add_argument('--proxy-server=http://%s' % str(self.proxy))
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito")
        options.headless =  False
        # options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        # options.add_argument(r"--user-data-dir=C:\Users\Ahmed\Desktop\Projcts\Gmail-Twitter\ChromeProfiles\profile0") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        # options.add_argument(r'--profile-directory=YourProfileDir') #e.g. Profile 3
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-site-isolation-trials')
        options.add_argument('--disable-application-cache')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        if self.Proxies:
            return options
        else:
            return options


    def __init__(self, name, url,tries_counetr,proxy_counter,email,hashe,mail_tries, thread,Proxies, Proxy_list,database,hotmail,type):
        self.name        = name
        self.url         = url
        self.email       = email
        self.hashe       = hashe
        self.thread      = thread
        self.Proxy_list  = Proxy_list
        self.mail_tries  = mail_tries
        self.tries_counter = tries_counetr
        self.status  = True
        self.Proxies = True
        self.is_phone_required = 0
        self.proxy_counter     = proxy_counter 
        self.taken     = 0
        self.database  = database
        self.hotmail   = hotmail
        self.proxy  = str(self.Proxy_list[random.choice(range(len(self.Proxy_list)))])
        self.type   = type
        self.email_State  = False
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"  #complete
        # self.capabilities = self.set_proxy()[0]
        # self.driver = webdriver.Firefox(capabilities = self.set_proxy()[0])
        if self.Proxies:
            options = self.set_proxy()
        else:
            options = self.set_proxy()
        self.driver = uc.Chrome(excutable_path='chromedriver.exe', options=options, desired_capabilities=caps)
        self.used = False

    def guest_activate(self):
        headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F'}
        counter = 0
        while counter < 5:
            try:
                http = 'https'
                response = requests.post('https://api.twitter.com/1.1/guest/activate.json' ,proxies={http: 'http://' + self.proxy, 'http': 'http://' + self.proxy},headers=headers,verify=False)
                if b'Rate limit exceeded' in response.content:
                    print('Rate limit exceeded')
                    break
                guest_token = response.json()['guest_token']
                break
            except Exception as e:
                print(e)
        return guest_token

    def get_access(self,user,Pass, user_id, request_id, proxy):
        global proxies
        url = 'https://api.twitter.com/oauth/access_token'
        data = 'x_auth_mode=client_auth&x_auth_login_verification=1&x_auth_login_challenge=1&send_error_codes=true&login_verification_user_id=' + user_id + '&login_verification_request_id=' + request_id
        url2 = url + '?' + data
        auth = OAuth1('3nVuSoBZnx6U4vzUxf5w', 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys')
        http = 'https'
        while 1:
            try:
                response = requests.get(url2, auth=auth, proxies={http: 'http://' + proxy}, verify=False)
                break
            except Exception as e:
                print('retrying ...', e)

        tweets = response.json()
        if 'oauth_token' in tweets:
            return tweets
        else:
            return False

    def login_challenge2(self,User, Pass, data, url, twt_sess, personalization_id, proxy,guest_token):
        cookies = {'guest_id': 'v1%3A' + guest_token,
           '_twitter_sess': twt_sess,
           'lang': 'en'}
        headers = {'Host': 'twitter.com',
           'Connection': 'close',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Origin': 'https://twitter.com',
           'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G955N Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Referer': url,
           'Accept-Encoding': 'gzip,deflate',
           'Accept-Language': 'en-EG,en-US;q=0.8',
           'X-Requested-With': 'com.twitter.android'}
        data = data
        iiii = 0
        http = 'https'
        while 1:
            try:
                response = requests.post('https://twitter.com/account/login_challenge', proxies={http: 'http://' + proxy}, headers=headers, cookies=cookies, data=data, allow_redirects=False, verify=False)
                l = response.headers['location']
                break
            except:
                print('Requesting Error For Challenge ')
                print('retrying ...')
                iiii += 1
                if iiii >= 5:
                    break

        if 'success' in response.headers['location']:
            print('challenge Completed.')
            request_id = data.split('challenge_id=')[1].split('&')[0]
            user_id = data.split('user_id=')[1].split('&')[0]
            return self.get_access(User,Pass, user_id, request_id, proxy)
        else:
            print('challenge Failed.')
            return False

    def login_challenge(self,url, User, Pass, proxy,guest_token,Email):
        cookies = {'guest_id': 'v1%3A' + guest_token}
        headers = {'Host': 'twitter.com',
                   'Connection': 'close',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G955N Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
                   'Accept-Encoding': 'gzip,deflate',
                   'Accept-Language': 'en-EG,en-US;q=0.8',
                   'X-Requested-With': 'com.twitter.android'}
        http = 'https'
        counter = 0
        while 1:
            try:
                response = requests.get(url, proxies={http: 'http://' + proxy}, headers=headers, cookies=cookies,
                                        verify=False)
                break
            except Exception as e:
                print('retrying ...', e)
                if counter < 5:
                    continue
                else:
                    break
        twt_sess = response.headers['set-cookie'].split('_twitter_sess=')[1].split(';')[0]
        personalization_id = ''
        values = re.findall('type="hidden" name=".*" value=".*"', response.text)
        data = ''
        for val in values:
            if data != '':
                data += '&'
            name = val.split('name="')[1].split('" value')[0]
            value = val.split('value="')[1].split('"')[0]
            data += name + '=' + value
        data += '&challenge_response=' + Email
        return self.login_challenge2(User,Pass, data, url, twt_sess, personalization_id, proxy,guest_token)

    def access(self,proxy, User, Pass,Email,guest_token):
        Tokens = []
        headers = {'X-Guest-Token': guest_token, 'Accept-Language': 'en-EG',
                   'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'x_auth_identifier': User,
                'x_auth_password': Pass,
                'send_error_codes': 'true',
                'x_auth_login_verification': '1',
                'x_auth_login_challenge': '1',
                'x_auth_country_code': 'EG'}
        http = 'https'
        response = requests.post('https://api.twitter.com/auth/1/xauth_password.json',proxies={http: 'http://' + proxy, 'http': 'http://' + proxy}, headers=headers,data=data, timeout=5, verify=False)
        r = response
        x = response.json()
        print(x)
        if b'Bad guest token' in response.content:
            try:
                self.guest_activate()
            except Exception as e:
                print(e)
        if b'oauth_token' in response.content:
            print('Login Success.')
            responsee = x['oauth_token'] + ':' + x['oauth_token_secret'] + User + ":" + Pass + proxy

            save = open('Access.txt', 'a+')
            save.write(responsee + '\n')
            save.close()
        if b'login_verification_request_url' in response.content:
            print('challenge Required.')
            lvr_url = x['login_verification_request_url']
            try:
                print('challenge required')
                x = self.login_challenge(lvr_url, User,Pass, proxy,guest_token,Email)
                
            except Exception as e:
                print(e)
                try:
                    x = self.login_challenge(lvr_url, User,Pass, proxy,guest_token,Email)
                except Exception as e:
                    print(e)
                    print('challenge Error Happenned.')
                    responsee = False
        Tokens.append(x['oauth_token'])
        Tokens.append(x['oauth_token_secret'])
        print(Tokens)
        return Tokens

    def specific_string(self,length):
        sample_string = 'pqrstuvwxy'  # define the specific string
        # define the condition for random string
        result = ''.join((random.choice(sample_string)) for x in range(length))
        return result

    def skip_not(self):
        """
        Eleventh part: skipping notifications

        """
        time.sleep(1)
        try:
            self.click('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]')

        except:
            self.click("/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]")

        print("The bot has skipped the notifications part")
    
    def continue_to_site(self):
        continue_to_site = self.driver.find_element(By.XPATH, '//*[@id="id__78"]' )
        action_chain = ActionChains(self.driver)
        action_chain.click(continue_to_site).perform()

    def random_name_generator(self):
        fake = faker.Faker()
        return "".join(fake.words(4))

    def skipping_username_selection(self):
        """
        eleventh part: skipping username
        """
        self.driver.refresh()
        try:
            self.click('//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div')
        except:
            pass
        time.sleep(1)
        try:
            self.skip_not()
        except:
            pass
        username_input = self.driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/span')
        self.username = username_input.text
        print(f"This username was retrieved from the username section: {self.username}")

    def get_tempmail(self):
        try :
            tm = TempMail("511f1f0011mshf1be72a86ae67e1p158688jsn41a319fa3dba")
            list_of_emails = tm.get_mailbox(self.email.encode("utf-8"), email_hash=self.hashe)
            splitted_message = list_of_emails[0]["mail_subject"].split(" ")
            code = splitted_message[0]
            return code
        except Exception as e:
            print(e)
            self.driver.quit()
            return False   
    def log_to_outlook(self):
        try:
            
            mail = outlook.Outlook()
            mail.login(self.email, self.hashe)
            mail.inbox()
            twitter_mesggaes = []
            for (something, content) in mail.unread().items():
                if something == "Subject":
                    if 'is your Twitter verification code' in content:
                        twitter_mesggaes.append(content)

            # for (something, content) in mail.read().items():
            #     if something == "Subject":
            #         if 'is your Twitter verification code' in content:
            #             twitter_mesggaes.append(content)
            print(twitter_mesggaes[0].split(" ")[0])
            code = twitter_mesggaes[0].split(" ")[0]
            return code
        except:
            print("Seems like such an account is locked thus it can't be used")
            self.status = False
            return 0
    def get_gmail(self): 
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        email1 = 'your email without @gmail.com'
        password = 'your apps password'
        mail.login(email1+'@gmail.com', password)
        mail.list()
        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox") # connect to inbox.
        result, data = mail.search(None, "ALL")

        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        latest_email_id = id_list[-30:] # get the latest

        # fetch the email body (RFC822) for the given ID
        for id in reversed(latest_email_id):
            result, data = mail.fetch(id, "(RFC822)") 
            raw_email = data[0][1]
            email_message = str(email.message_from_string(str(raw_email)))
            x = email_message.split("\\r\\n")
            to = x[0].split(':')[1].strip(' ')
            if  to == self.email.strip('\n'):
                code = re.findall("Subject: (.*) is your Twitter verification code", email_message)[0]
                print(code)
                return code
    def get_10minutecode(self):
        return str(self.hashe.getMessage(self.hashe.anyNewMessage(0) - 1)[0]['subject']).split(" ")[0]

    def get_Gumail(self):
        try:
            time.sleep(2)
            code    = self.hashe.check_mail()
            return code
        except Exception as e:
            print(e)
            self.driver.quit()
            return False

    def get_MinuteInBox(self):
        code = self.hashe.get_inbox().split(' ')[0]
        print(code)
        return code

    def get_MailTm(self):
        return self.hashe.get_code()

    def has_numbers(self,inputString):
        return any(char.isdigit() for char in inputString)
    def click(self, route):
        try:
            self.driver.find_element(By.XPATH, route).click()
        except:
            self.driver.find_element(By.NAME, route).click()

    def write(self, path, content):
        self.driver.find_element(By.NAME, path).send_keys(content)
    #Added
    def screenshot(self,challenge):
        for i in range(1,7):
                name = "test\{}.png".format(faker.Faker().sentence().strip(' '))
                element = self.driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div/div[2]/div/ul/li[{i}]/a")
                element.screenshot(name)
                potatod = run(weights=r"best.pt", source=name)
                print(potatod)
                if potatod == challenge:
                    print(potatod)
                    self.click(f"/html/body/div/div/div[1]/div/div[2]/div/ul/li[{i}]/a")
                    return True
                

    def first_section(self):
       try:
         
            # Loading the website
            # UseNord.connect_to_vpn()
            self.driver.implicitly_wait(5)
            self.driver.get(self.url)
            self.driver.maximize_window()
            
            """
            First part entering details like name and email
            """
            time.sleep(5)
            self.click("//div[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/div")
            # typing in name and email
            name_random = self.random_name_generator()
            self.write('name',name_random)

            # clicking on email_instead
            self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[3]')
            self.write('email', self.email)
        
            # print("Entered email")

            # Inserting birth date
            select = Select(self.driver.find_element(By.ID,'SELECTOR_1'))
            month = str(np.random.randint(1, 12))
            select.select_by_value(month)
            select = Select(self.driver.find_element(By.ID,'SELECTOR_2'))
            day = str(np.random.randint(1, 30))
            select.select_by_value(day)
            select = Select(self.driver.find_element(By.ID,'SELECTOR_3'))
            select.select_by_visible_text("1999")
            # print("entered birth dates")

            time.sleep(2)
            # pressing_next
            try: 
                self.click('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
            except:
                self.status = False

            self.driver.delete_all_cookies()

            """
            Second part: Customizing expernience
            """
            time.sleep(1.5)
            # pressing next
            try: 
                self.click('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
            except:
                self.status = False
            # print("The bot has passed the customization part")
            self.driver.delete_all_cookies()

            """
            Third part : Signing up
            """
            time.sleep(1.5)
            if self.type == 'Gumail':
                time.sleep(10)
            try:
               self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div')
            except:
                self.status = False
            # print("The bot has passed the sign up part")
            self.driver.delete_all_cookies()
            try:
                time.sleep(10)
                self.driver.delete_all_cookies()
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/iframe'))
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '/html/body/div/div/iframe'))
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '/html/body/div/div/div/iframe'))
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/iframe'))
                self.click('/html/body/div/div/div[1]/button')
                # time.sleep(5)
                # url = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[2]/div/ul/li[1]/a").get_attribute("src")
                # urlretrieve(url, "local-filename.jpg")
                time.sleep(2)
                challenge = self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/div[1]/h2').text.split(' ')[2]
                print(self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/div[1]/h2').text)
                self.screenshot(challenge)
                # self.click('/html/body/div/div/div[1]/div/div[2]/div/ul/li[5]/a')
                time.sleep(4)
                try:
                    step1 = self.screenshot(challenge)
                except:
                    pass
                # self.click('/html/body/div/div/div[1]/div/div[2]/div/ul/li[5]/a')
                time.sleep(4)
                try:
                    self.screenshot(challenge)
                except: 
                    pass
            except:
                print("Verfication Failed")
                self.driver.quit()
                return False
            """
            Fourth part: Getting verification code and inserting it as an input to verification code area
            """
            code = None

            time.sleep(7)
            if self.hotmail == False:
                if   self.type == 'tempmail':
                    code = self.get_tempmail()
                elif self.type == 'gmail':
                    code = self.get_gmail()
                elif self.type == '10minute':
                    code = self.get_10minutecode()
                elif self.type == 'Gumail':
                    code = self.get_Gumail()
                elif self.type == 'MinuteInBox':
                    code = self.get_MinuteInBox()
                elif self.type == 'MailTm':
                    code = self.get_MailTm()
            else:
                code = self.log_to_outlook()
            # entering the code
            if not self.has_numbers(code):
                print("There is no code retrieved")
                self.tries_counter += 2
                self.driver.quit()
                return False
            elif code != "" and code is not None and code != 0 :
                verification_code_input = self.driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
                action_chain = ActionChains(self.driver)
                action_chain.click(verification_code_input).send_keys(code).perform()
                # print("The bot has passed the verification part by entering code")


                # Pressing next
                time.sleep(2)
                self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div')
                self.driver.delete_all_cookies()

                time.sleep(2.5)
                html = self.driver.execute_script("return document.body.innerHTML; ")
                bs = BeautifulSoup(html,"html.parser")

                all_span_tags = bs.find_all("span")


                phone_number = False
                for span_tag in all_span_tags:
                    if "Add a phone number" in span_tag.text:
                        self.is_phone_required += 1
                        phone_number = True
                        
                if phone_number:
                    print('\033[31m' + "Phone number was required" + '\033[0m')
                    self.used = True
                    self.is_phone_required += 1
                    self.driver.quit()
                    return False

                return self.email
       except:
           self.tries_counter += 1
           self.driver.quit()
           return False

    #Added
    def second_section(self):

        """
        Fifth part: entering password
        """
        # time.sleep(2)

        #entering password
        password = "BOTwownow24368"
        self.write('password', password)
        print('\033[92m'+"Phone number was not required"+'\033[0m')
        self.used= True
        # time.sleep(3.5)
        try:
            #pressing next
            self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
            time.sleep(2)
            try:
                self.click('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
            except Exception as e:
                print(e)
            try:
                self.click('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
            except Exception as e:
                print(e)
            # print("The bot has passed the sign up part")
            try:
                self.skipping_username_selection()
            except:
                self.driver.quit()
                return None
            self.driver.quit()
        except Exception as e:
            print(e)
            self.skipping_username_selection()
            self.driver.quit()
            return False

    def create_account(self):
        self.username = ""
        do = self.first_section()
        print(do)
        if do == False:
            return False
        self.second_section()
        if self.username != '':
            username = self.username
        else:
            self.driver.save_screenshot("password.png")
            self.skip_not()
    
        """
        Final part : closing the window and saving the email details

        """
        
        time.sleep(2)
        if self.username != '':
            # , "proxy": self.set_proxy()[1
            print(f"username is: {username}")
            guest_token = self.guest_activate()
            n = 0
            proxy = self.proxy
            while n < 5:
                try:
                    Tokens = self.access(proxy,self.username, "BOTwownow24368",self.email,guest_token)
                            # Thread.join()
                    time.sleep(0)
                    break
                except Exception as e:
                    n +=1
                    proxy = random.choice(self.Proxy_list)
                    continue
            account = Tokens[0] + ':' + Tokens[1] + ':' + self.username + ':'+"BOTwownow24368" + ':'+str(self.email) + ':'+ proxy
            ser = pd.Series({'key': Tokens[0],'secret': Tokens[1],"username": username[1:], "password": "BOTwownow24368", "email":str(self.email), "proxy":self.proxy,"port":self.proxy.split(":")[1]})
            with open('acc_temp.txt', 'a') as f:
                f.write(Tokens[0] + ':' + Tokens[1] + ':' + self.username + ':'+"BOTwownow24368" + ':'+str(self.email)+ ':'+ self.proxy+"\n")
                f.close()
            return account
        else:
            return False

