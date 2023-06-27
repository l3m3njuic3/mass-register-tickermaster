from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import string
import time
from utils.utils import *

#! simulate human mouse movement
#! check if browser history is part of requirements

class Gmail:
    def __init__(self):
        self.url = 'https://accounts.google.com/signup/v2/createaccount?biz=false&cc=SG&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%3Ftab%3Drm%26ogbl&dsh=S-1425664771%3A1687760756623121&emr=1&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%3Ftab%3Drm%26ogbl&ifkv=Af_xneHjp_aaa6oVXLW-UVvhYm8tNEN4U-xlYaYyBwYsAipCNsmXn70LXmfH3wUIsxd2jstU02uyPw&osid=1&service=mail'
        self.SELECTORS = {
            'firstname_input': '//*[@id="firstName"]',
            'firstname_next': '//*[@id="collectNameNext"]/div/button',
            'birth_day_input': '//*[@id="day"]',
            'birth_month_select': '//*[@id="month"]', 
            'birth_year_input': '//*[@id="year"]',
            'gender': '//*[@id="gender"]',
            'birthdaygender_next': '//*[@id="birthdaygenderNext"]/div/button',
            'create_own_address': '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div/div[2]',
            'address_input': '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input',
            'address_next': '//*[@id="next"]/div/button',
            'password_input': '//*[@id="passwd"]/div[1]/div/div[1]/input',
            'confirm_password_input': '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input',
            'password_next': '//*[@id="createpasswordNext"]/div/button'
        }
        self.headless = False
    
    def generate_random_info(self) -> dict:
        """
        Generates random account information
        
        Returns:
            info (dict): account information
        """        
        letters = string.ascii_lowercase
        length = 8 # length of username
        firstname = ''.join(random.choice(letters) for _ in range(length))
        
        info = {
            'firstname': firstname,
            'gmail': f'{firstname}@gmail.com',
            'birth_day': str(random.randint(1, 28)),
            'birth_month': random.randint(1, 12),
            'birth_year': str(random.randint(1970, 2000)),
            'gender': random.randint(2, 3), # 1 is male, 2 is female
            'password': firstname + '@password'
        }
        
        return info
        
    def open_browser(self):
        """
        Opens a Selenium session
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # disable logging 
        
        if self.headless:
            chrome_options.add_argument('--headless') # set headless so that it runs in the background
            
        chrome_options.add_argument(r'--user-data-dir=C:\Users\laijj\AppData\Local\Google\Chrome\User Data')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
    
    def click_element(self, selector):
        """
        Clicks the selector passed

        Args:
            selector (str): XPATH of element
        """
        element = WebDriverWait(self.driver, 8).until(
            EC.presence_of_element_located((By.XPATH, selector))
        )        
        element.click()
    
    def send_keys(self, selector, data):
        """
        Sends data to the selector

        Args:
            selector (str): XPATH of element
            data (str/int): Data to pass
        """
        element = WebDriverWait(self.driver, 8).until(
            EC.presence_of_element_located((By.XPATH, selector))
        )
        
        # simulate human typing
        human_type(message=data, element=element)
    
    def create_gmail(self, count):
        """
        Navigates the browser session
        """
        for _ in range(count):
            self.open_browser()
            info = self.generate_random_info()
            
            # fill in first name        
            self.send_keys(selector=self.SELECTORS['firstname_input'], data=info['firstname'])
            
            # go to the next page
            self.click_element(selector=self.SELECTORS['firstname_next'])
            
            # fill in birth day
            self.send_keys(selector=self.SELECTORS['birth_day_input'], data=info['birth_day'])
            
            # fill in birth month
            self.click_element(selector=self.SELECTORS['birth_month_select']) # click on the dropdown
            self.click_element(selector=f'{self.SELECTORS["birth_month_select"]}/option[{info["birth_month"]}]')
            
            # fill in birth year
            self.send_keys(selector=self.SELECTORS['birth_year_input'], data=info['birth_year'])
            
            # fill in gender
            self.click_element(selector=self.SELECTORS['gender']) # click on the dropdown
            self.click_element(selector=f'{self.SELECTORS["gender"]}/option[{info["gender"]}]')
            
            # go to the next page
            time.sleep(1) # else bot might not have enough time to click on the dropdown
            self.click_element(selector=self.SELECTORS['birthdaygender_next'])
            
            # create gmail using firstname
            self.click_element(selector=self.SELECTORS['create_own_address'])
            self.send_keys(selector=self.SELECTORS['address_input'], data=info['firstname'])
            
            # go to the next page
            self.click_element(selector=self.SELECTORS['address_next'])
            
            # fill in password and confirm password
            self.send_keys(selector=self.SELECTORS['password_input'], data=info['password'])
            self.send_keys(selector=self.SELECTORS['confirm_password_input'], data=info['password'])
            
            # go to the next page
            self.click_element(selector=self.SELECTORS['password_next'])
            
            # write accounts created to text file
            data = f'{info["firstname"]}@gmail.com,{info["password"]} \n'
            self.writedown(data=data)
    
    def writedown(self, data):
        with open('gmail_accounts.txt', 'a+') as outfile:
            outfile.write(data)