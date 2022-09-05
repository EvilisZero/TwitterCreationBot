
from TwitterBot_Proton import TwitterBot
import time
import pymongo
import os
import faker
from tempMail2 import TempMail
from glob import glob
import random
import tempfile
import shutil
class controller2:
    def __init__(self,thread, Proxies, Proxy_list,database):
        self.prox = []
        for i in Proxy_list[thread][0]:
            self.prox.append(i)
        self.thread                  = thread
        self.Proxies                 = False
        self.proxy_list              = Proxy_list
        self.database                = database
        self.proxy_counter           = 0
        self.email                   = ''
        self.hotmail_collection      = database["Hotmail"]
        self.pending_collections     = database["Pending"]
        self.used_hotmail_collection = database["UsedHotMail"]
        self.locked_accounts         = database["LockedAccounts"]
        self.number_of_proxies       = len(self.prox)
        self.last_email              = ""
        self.email                   = ""
        self.hash                    = ""
        self.mail_tries              = 0
        self.tries_counter           = 0
        self.account                 = {}
        self.hotmail_accounts        = []
        self.choose                  = ['proton','tempmail']
        self.type                    = 'proton'
        self.hotmail                 = True
    
    def id(self,dict,choice):
        pending_counter = 0
        while pending_counter <= 5:
            try:
                if choice:
                    dict.delete_one(filter={"_id": self.account["_id"]})
                else:
                    dict.insert_one(self.account)
            except:
                print("The bot failed to delete the document from the pending collection thus the bot would try again")
                pending_counter += 1
            else:
                print("the bot successfully managed to delete the document from the pending collection")
                break

    def get_hotmail(self):
        for documnet in self.hotmail_collection.find().sort("_id", direction=pymongo.DESCENDING):
            self.hotmail_accounts.append(documnet)

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
            self.hotmail_accounts = []
            if self.proxy_counter >= self.number_of_proxies:
                self.proxy_counter = 0
            
            self.get_hotmail()
            if (len(self.hotmail_accounts) == 0):
                print("It Seems that there are no more accounts in the database thus the bot will use tempmail")
                self.get_hotmail()
                self.type = 'proton'
                if self.type   == 'tempmail':
                    print('potato')
                    try:
                        data   = self.tempmail()
                    except Exception as e:
                        print(e)
                        continue
                    self.email = data[0]
                    self.hash  = data[1]
                else:
                    self.email   = ''
                    self.hotmail = False
            if self.hotmail:
                self.account = self.hotmail_accounts[0]
                self.email= self.account['email']

                id(self.hotmail_collection,True)
                print("The current email will be added to the pending collection")
                id(self.pending_collections,False)

            try:
                    bot = TwitterBot("twitter", "https://twitter.com/i/flow/signup",self.tries_counter,self.proxy_counter,self.email ,self.hash,self.mail_tries,self.thread, self.Proxies, self.prox, self.database,self.hotmail, self.type)
                    ser = bot.create_account()
            except Exception as e:
                if self.hotmail:
                    if bot.status:
                        id(self.hotmail_collection,False)
                        time.sleep(2)
                    else:
                        id(self.used_hotmail_collection,False)
                    id(self.pending_collections,True)
                self.proxy_counter += 1
                bot.driver.delete_all_cookies()
                bot.driver.quit()
                continue
            else:
                self.proxy_counter += 1
                if not ser:
                    continue
                if self.hotmail:
                    id(self.hotmail_collection,True)
                    id(self.used_hotmail_collection,False)
                co = 0
                while co < 5:
                    try:
                        bot.driver.quit()

                        co = 5
                    except:
                        os.system("taskkill /im chromedriver.exe")
                        co += 1
                
                self.mail_tries = 0
                return ser




