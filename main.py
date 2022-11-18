import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSeypVEDdp80hocyqu8fkl6jZjW8Jn0_jLnLM0zyI3vQ3qGq7w/viewform?usp=sf_link'
URL = 'https://www.zillow.com/homes/for_sale/?utm_medium=cpc&utm_source=google&utm_content=18806865550|142739413803|aud-455958732640:kwd-570802407|603457706088|&semQue=null&gclid=Cj0KCQiA1NebBhDDARIsAANiDD2N47UyCRen-B68fsVVnbVyMpRe9TEvPwYvbFwOYgXsalplmly8rKMaAtetEALw_wcB&searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-84.44240062890626%2C%22east%22%3A-83.93153637109376%2C%22south%22%3A33.575570762774746%2C%22north%22%3A34.0098261564241%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22price%22%3A%7B%22max%22%3A150000%7D%2C%22mp%22%3A%7B%22max%22%3A740%7D%2C%22beds%22%3A%7B%22min%22%3A3%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22pagination%22%3A%7B%7D%7D'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
PATH = '/Users/a/Library/Mobile Documents/com~apple~CloudDocs/Development/chromedriver'

response = requests.get(headers=header, url=URL)
response.raise_for_status()
zillow_text = response.text
soup = BeautifulSoup(zillow_text, 'html.parser')
ADDRESS = []
LINK = []
PRICE = []

zillow_link = soup.select('article div div a[tabindex="0"]', class_='lhIXlm', href=True)
for link in zillow_link:
    if link in LINK:
        continue
    else:
        LINK.append(link['href'])

zillow_address = soup.select('a address', class_='StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0')
for addy in zillow_address:
    ADDRESS.append(addy.getText())

listings = soup.select('article div div div span[data-test="property-card-price"]',
                       class_='StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0')
for listing in listings:
    PRICE.append(listing.getText())


class Form:

    def __init__(self):
        opt = Options()
        opt.add_experimental_option('detach', True)
        ser = Service(PATH)
        self.driver = webdriver.Chrome(service=ser, options=opt)

    def fill_out_form(self, address, price, link):
        self.driver.get(url=FORM_LINK)
        time.sleep(2)
        row1 = self.driver.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        row1.send_keys(address)
        time.sleep(1)
        row2 = self.driver.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        row2.send_keys(price)
        time.sleep(1)
        row3 = self.driver.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        row3.send_keys(link)
        time.sleep(1)
        self.driver.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()


fill_form = Form()
for n in range(0, len(LINK)-1):
    fill_form.fill_out_form(address=ADDRESS[n], price=PRICE[n], link=LINK[n])


