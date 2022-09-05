
from Run import Hotmail
from TwitterBot import TwitterBot
import time
import os
from TenMinuteMailGenerator import TenMinuteMailGenerator
from tempMail2 import TempMail
from glob import glob
import random
from GuMail import GuMail
from minuteinbox import MinuteInBox
from MailTm import MailTm
class controller:
    def __init__(self,thread, Proxies, Proxy_list,database):
        self.prox = []
        for i in Proxy_list[thread][0]:
            self.prox.append(i)
        with open('emails.txt', 'r') as f:
            self.emails = f.readlines()
            f.close()
        self.database                = database
        self.thread                  = thread
        self.Proxies                 = False
        self.proxy_list              = Proxy_list
        self.database                = database
        self.proxy_counter           = 0
        self.email                   = ''
        self.number_of_proxies       = len(self.prox)
        self.last_email              = ""
        self.email                   = ""
        self.hash                    = ""
        self.mail_tries              = 0
        self.tries_counter           = 0
        self.account                 = {}
        self.hotmail_accounts        = []
        self.choose                  = ['MinuteInBox','Gumail']
        self.type                    = 'proton'
        self.hotmail                 = True
        self.Data                    = ''

    def get_hotmail(self):
        self.Data = self.database.get()
        self.email = self.Data.split("|")[0]
        self.hash = self.Data.split("|")[1]

    def tempmail(self):
        try:
            tm    = TempMail("511f1f0011mshf1be72a86ae67e1p158688jsn41a319fa3dba")
            email = tm.get_email_address()
            hash  = tm.get_hash(email=email.encode("utf-8"))
            self.hotmail = False

        except Exception as e:
            print(e)
        return email, hash

    def mainTemp(self):
        while True:
            if self.proxy_counter >= self.number_of_proxies:
                self.proxy_counter = 0
            if (self.database.qsize() == 0):
                print("It Seems that there are no more accounts in the database thus the bot will use tempmail")
                self.hotmail = False
                self.type = 'gmail'
                if self.type   == 'tempmail':
                    print('potato')
                    try:
                        data   = self.tempmail()
                    except Exception as e:
                        print(e)
                        continue
                    self.email = data[0]
                    self.hash  = data[1]
                elif self.type == 'gmail':
                    self.email = random.choice(self.emails)
                elif self.type == '10minute':
                    self.hash  = TenMinuteMailGenerator()
                    self.email = self.hash.get10MinuteMail()
                elif self.type == 'Gumail':
                    self.hash  = GuMail(random.choice(self.prox))
                    self.email = self.hash.get_mail()
                    print(self.email)
                elif self.type == 'MinuteInBox':
                    self.hash  = MinuteInBox(random.choice(self.prox))
                    self.email = self.hash.create_email().get('email')
                elif self.type == 'MailTm':
                    self.hash  = MailTm(random.choice(self.prox))
                    self.email = self.hash.get_email(make_account=True)
            else:
                self.get_hotmail()

            try:
                    bot = TwitterBot("twitter", "https://twitter.com/i/flow/signup",self.tries_counter,self.proxy_counter,self.email ,self.hash,self.mail_tries,self.thread, self.Proxies, self.prox, self.database,self.hotmail, self.type)
                    ser = bot.create_account()
            except Exception as e:
                if self.hotmail:
                    try:
                        if bot.status:
                            self.database.put(self.Data)
                    except:
                        self.database.put(self.Data)
                self.proxy_counter += 1
                continue
            else:
                self.proxy_counter += 1
                if not ser:
                    if self.hotmail and bot.status:
                        self.database.put(self.Data)
                    continue
                co = 0
                while co < 5:
                    try:
                        bot.driver.quit()

                        co = 5
                    except:
                        os.system("taskkill /im chromedriver.exe")
                        co += 1
                bot.driver.quit()
                self.mail_tries = 0
                if self.hotmail:
                    with open('UsedHotmail.txt', 'a') as f:
                        f.write(self.email + '|' + self.hash + '\n')
                        f.close()
                return ser
                




