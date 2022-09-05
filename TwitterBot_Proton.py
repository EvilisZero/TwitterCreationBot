
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
from test_sadas import TestSadas
import copy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from smsactivateru import Sms, SmsService, GetNumber, SmsTypes


class TwitterBot:
    warnings.filterwarnings("ignore")
 
    def set_proxy(self):
        options = uc.ChromeOptions()
        if self.Proxies:
            options.add_argument('--proxy-server=http://%s' % str(self.proxy))
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito")
        options.headless =  True
        # options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        # options.add_argument(r"--user-data-dir=C:\Users\Ahmed\Desktop\Projcts\proton-twitter\ChromeProfiles\profile0") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        # options.add_argument(r'--profile-directory=YourProfileDir') #e.g. Profile 3
        options.add_argument('--disable-blink-features=AutomationControlled')
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
        self.hotmail   = False
        self.proxy  = str(self.Proxy_list[random.choice(range(len(self.Proxy_list)))])
        self.type   = type
        if self.type == 'proton':
            self.proton  = TestSadas(thread)
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

    def guest_activate(self):
        headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm'}
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
        auth = OAuth1('IQKbtAYlXLripLGPWd0HUA', 'GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU')
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
                   'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm',
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
    def make_proton(self):
        self.email = self.proton.test_sadas()
        if not self.email:
            self.driver.quit()
    def click(self, route):
        try:
            self.driver.find_element(By.XPATH, route).click()
        except:
            self.driver.find_element(By.NAME, route).click()

    def write(self, path, content):
        self.driver.find_element(By.NAME, path).send_keys(content)
    #Added
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
            if self.type == 'proton':
                t =  threading.Thread(target=self.make_proton)
                t.daemon = True
                t.start()
            name_random = self.random_name_generator()
            self.write('name',name_random)

            # clicking on email_instead
            self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[3]')
            if self.type == 'proton':
                while True:
                    time.sleep(3)
                    if self.proton.ready:
                        break
                    if self.proton.error:
                        break
                    print(self.proton.error)
                if not self.email:
                    self.driver.quit()
                    return False
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
            self.click('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
            # print("The bot has passed the customization part")
            self.driver.delete_all_cookies()

            """
            Third part : Signing up
            """
            time.sleep(1.5)

            self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div')
            # print("The bot has passed the sign up part")
            self.driver.delete_all_cookies()

            """
            Fourth part: Getting verification code and inserting it as an input to verification code area
            """
            code = None

            time.sleep(3)
            if self.hotmail == False:
                if   self.type =='tempmail':
                    code = self.get_tempmail()
                elif self.type == 'proton':
                    code = self.proton.get_code()

            # entering the code
            if not code:
                print("There is no code retrieved")
                self.tries_counter += 2
                self.driver.quit()
                with open('notused.txt','a') as f:
                    f.write(self.email +":"+ self.proton.password + '\n')
                    f.close()
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
                    if self.type == 'proton':
                        with open('notused.txt','a') as f:
                            f.write(self.email +":"+ self.proton.password + '\n')
                            f.close()
                    return False

                return self.email
       except:
           self.tries_counter += 1
           self.driver.quit()
           if self.type == 'proton':
            self.proton.driver.quit()
            if self.proton.ready:
                with open('notused.txt','a') as f:
                        f.write(self.email +":"+ self.proton.password + '\n')
                        f.close()
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
        self.used= False
        # time.sleep(3.5)
        try:
            #pressing next
            self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
            time.sleep(2)
            self.click('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
            try:
                self.click('/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
            except Exception as e:
                print(e)
            # print("The bot has passed the sign up part")
            try:
                self.skipping_username_selection()
            except:
                return None
        except Exception as e:
            print(e)
            self.skipping_username_selection()
            pass

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
            try:
                guest_token = self.guest_activate()
                Tokens = self.access(self.proxy,self.username, "BOTwownow24368",self.email,guest_token)
                         # Thread.join()
                time.sleep(0)
            except Exception as e:
                pass
            with open('acc_temp.txt', 'a') as f:
                f.write(self.username + ':'+"BOTwownow24368" + ':'+str(self.email))
                f.close()
            account = Tokens[0] + ':' + Tokens[1] + ':' + self.username + ':'+"BOTwownow24368" + ':'+str(self.email) + ':'+ self.proxy 
            ser = pd.Series({'key': Tokens[0],'secret': Tokens[1],"username": username[1:], "password": "BOTwownow24368", "email":str(self.email), "proxy":self.proxy,"port":self.proxy.split(":")[1]})

            twitter_hotmail_collection = self.database["TwitterTemp"]
            twitter_hotmail_collection.insert_one(ser.to_dict())
            self.driver.kill()
            return account
        else:
            return False

