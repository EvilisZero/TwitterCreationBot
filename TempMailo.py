import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
class Tempomailo:
    def __init__(self, proxy):
        self.proxy = proxy
        options = uc.ChromeOptions()
        # options.add_argument('--proxy-server=http://%s' % self.proxy)
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito")
        options.headless =  False
        options.add_argument("--log-level=3")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"  #complete
        self.driver = uc.Chrome(excutable_path='chromedriver.exe', options=options, desired_capabilities=caps)

    def get_email(self):
        self.driver.implicitly_wait(5)
        self.driver.get('https://fakermail.com/')
        time.sleep(2)
        email = self.driver.find_element(By.ID, 'email-address').get_attribute('value')
        print(email)

if __name__ == '__main__':
    p = Tempomailo('23.229.107.49:7574')
    p.get_email()