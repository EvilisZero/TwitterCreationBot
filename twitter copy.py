import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import numpy as np
import pandas as pd
import re
import undetected_chromedriver as uc
from requests_oauthlib import OAuth1
import random
import pandas as pd
import time
import threading
from glob import glob
import copy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import faker
import os
from urllib.request import urlretrieve
from detect import run
class Collector:
   def __init__(self):
        self.url = 'https://signup.live.com/signup?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1661517973&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26signup%3d1%26RpsCsrfState%3dcef3bde9-030c-ce46-a942-2285f26b87c6&id=292841&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015&lic=1&uaid=f5c9569392f94930ac4767021aaf5c93'
        options = uc.ChromeOptions()
        with open('proxies.csv', 'r') as f:
            self.proxy = random.choice(f.readlines())
        self.name = faker.Faker().sentence().strip(' ')
        options.add_argument('--proxy-server=http://%s' % str(self.proxy))
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito")
        options.headless =  False
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        # options.add_argument(r"--user-data-dir=C:\Users\Ahmed\Desktop\Projcts\proton-twitter\ChromeProfiles\profile0") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        # options.add_argument(r'--profile-directory=YourProfileDir') #e.g. Profile 3
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"  #complete
        self.driver = uc.Chrome(excutable_path='chromedriver.exe', options=options, desired_capabilities=caps)
        self.email = self.random_name_generator(4)
        self.password = 'A7med24368@@'

   def click(self, route):
        try:
            self.driver.find_element(By.XPATH, route).click()
        except:
            self.driver.find_element(By.NAME, route).click()

   def write(self, path, content):
    try:
        self.driver.find_element(By.NAME, path).send_keys(content)
    except:
        self.driver.find_element(By.XPATH, path).send_keys(content)

   def random_name_generator(self,n):
        fake = faker.Faker()
        return "".join(fake.words(n))
   def screenshot(self,challenge):
    for i in range(1,6):
            name = "{}.png".format(faker.Faker().sentence().strip(' '))
            element = self.driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div/div[2]/div/ul/li[{i}]/a")
            element.screenshot(name)
            potatod =  run(weights=r"best.pt", source=name)
            print(potatod)
            if potatod == challenge:
                print(potatod)
                self.click(f"/html/body/div/div/div[1]/div/div[2]/div/ul/li[{i}]/a")
                return True

   def collect(self):
        try:
            self.driver.implicitly_wait(5)
            self.driver.get(self.url)
            self.driver.maximize_window()
            
            """
            First part entering details like name and email
            """
            time.sleep(5)
            self.write('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[1]/fieldset/div[1]/div[3]/div[2]/div/input', self.email )
            time.sleep(5)
            self.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[1]/div[2]/div/div/div/div[3]/input')
            time.sleep(5)
            self.write('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[3]/div/input[2]', self.password)
            self.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[7]/div/div/div[2]/input')
            time.sleep(5)
            self.write('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[1]/div[3]/div[1]/input', self.random_name_generator(1))
            self.write('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[1]/div[3]/div[2]/input', self.random_name_generator(1))
            self.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[2]/div/div/div[2]/input')
            time.sleep(5)
            select = Select(self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[4]/div[3]/div[1]/select'))
            month  = str(np.random.randint(1, 12))
            select.select_by_value(month)
            select = Select(self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[4]/div[3]/div[2]/select'))
            day    = str(np.random.randint(1, 30))
            select.select_by_value(day)
            self.write('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[4]/div[3]/div[3]/input', random.choice(range(1975, 2000)) )
            self.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[6]/div/div/div[2]/input')
            time.sleep(7)
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div[3]/iframe'))
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH,'/html/body/div/div/iframe'))
            self.click('/html/body/div/div/div[1]/button')
            challenge = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[1]/h2').text
            print(challenge)
            # select = Select(self.driver.find_element(By.ID,'SELECTOR_3'))
            # select.select_by_visible_text("1999")
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
            time.sleep(6)

            self.click('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div')
            # print("The bot has passed the sign up part")
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
            self.screenshot(challenge)
            # self.click('/html/body/div/div/div[1]/div/div[2]/div/ul/li[5]/a')
            time.sleep(4)
            self.screenshot(challenge)
            # self.click('/html/body/div/div/div[1]/div/div[2]/div/ul/li[5]/a')
            time.sleep(4)
            self.screenshot(challenge)
            self.driver.quit()
            # self.driver.save_screenshot("{}.png".format(self.name + "1"))
            # time.sleep(2)
            # self.click('/html/body/div/div/div[1]/div/div[2]/div/ul/li[5]/a')
            # self.driver.save_screenshot("{}.png".format(self.name + "2"))
        except:
            self.driver.quit()



if __name__ == '__main__':
    while True:
        try:
            p = Collector()
            p.collect()
        except:
            continue

