import os
os.environ['WDM_LOG'] = '0' 
os.environ['WDM_LOG_LEVEL'] = '0'
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as MsOptions
from selenium.webdriver.chrome.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests
from scam.elements import *
from management.log import *

class Bot:
    nb_error = 0
    nb_scam = 0
    def __init__(self,referal) -> None:
        log("Init ScamDriver",Type.Warn)
        options = MsOptions()
        options.add_argument('log-level=3')
        options.add_argument("--mute-audio")
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #options.add_argument("user-agent = my-user-agent")
        self._options = options
        self._driver = webdriver.Edge(EdgeChromiumDriverManager().install(),options=self._options)
        self._wait = WebDriverWait(self._driver,5)
        self._referal = referal
        self.email = ""
        log("Init success",Type.Success)

    def gen_email(self):
        url = f"https://www.1secmail.com/api/v1/?action=genRandomMailbox"
        response = requests.request("GET", url)
        self.email =  response.text.split("@")[0].split('"')[1]

    def get_mails(self):
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={self.email}&domain=bheps.com"
        response = requests.request("GET", url)
        return response.json()

    def get_code(self,mail_id):
        url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.email}&domain=bheps.com&id={mail_id}"
        response = requests.request("GET", url)
        body = response.json()['body']
        log("Getting code")
        return body.rstrip("\n").split(": ")[1]


    def scam(self):
        self.gen_email()
        d = self._driver
        d.delete_all_cookies()
        d.get(self._referal)
        try:
            self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,EMAIL_INPUT)))
            d.find_element(By.CSS_SELECTOR,EMAIL_INPUT).send_keys(f"{self.email}@bheps.com")
            d.find_element(By.CSS_SELECTOR,EMAIL_CONFIRM).click()
            self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,CODE_INPUT)))
            Bot.nb_error = 0
            mail_id = None
            log("Checking mails...",Type.Info)
            while mail_id == None:
                sleep(5)
                mails = self.get_mails()
                if(len(mails) > 0):
                    mail_id = mails[0]['id']
                else:
                    log("Ask new code",Type.Info)
                    d.find_element(By.CSS_SELECTOR,RESEND_MAIL).click()


            code = self.get_code(mail_id)
            d.find_element(By.CSS_SELECTOR,CODE_INPUT).send_keys(code)
            try:
                self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,CONFIRM_AFFILIATE)))
                log("Scam Success",Type.Success)
                Bot.nb_scam += 1
            except:
                log("Cant Verify Success",Type.Warn)
        except:
            log("IP Terminated",Type.Error)
            Bot.nb_error += 1
        d.close()
            
        
