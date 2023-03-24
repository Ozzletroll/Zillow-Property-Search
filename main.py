import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Google forms
GOOGLE_FORM_URL = "https://forms.gle/s47EAP9p7nDHY8xb9"

# Beautiful Soup
TARGET_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22" \
             "%3A%7B%22west%22%3A-122.6211020173259%2C%22east%22%3A-122.28876559154465%2C%22south%22%3A37" \
             ".5434903621639%2C%22north%22%3A37.859677554621875%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A" \
             "%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value" \
             "%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22" \
             "%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22" \
             "%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C" \
             "%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Accept-Language": "en-GB,en;q=0.5",
}
response = requests.get(TARGET_URL, headers=headers)
response.encoding = "utf-8"
html_text = response.text
soup = BeautifulSoup(html_text, "html.parser")
search_results = soup.findAll(name="li", class_="ListItem-c11n-8-85-1__sc-10e22w8-0")
results_list = []
for entry in search_results:
    try:
        div = entry.find(class_="StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 bqsBln")
        # Get entry price
        price = div.contents[0].getText()
        # Get entry address
        address = entry.find(class_="StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0").getText()
        # Get entry URL
        url = f"https://www.zillow.com/{entry.find('a').get('href')}"
    except AttributeError:
        pass
    else:
        dict_entry = {
            "address": address,
            "price": price.split("+")[0],
            "url": url,
        }
        results_list.append(dict_entry)
print(results_list)

# Selenium driver setup
service = Service("C:/Program Files (x86)/Google/Chrome/chromedriver.exe")
options = ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)

for result in results_list:
    driver.get(GOOGLE_FORM_URL)
    time.sleep(1)
    address_entry = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > "
                                                         "div:nth-child(1) > div > div > div.AgroKb > div > "
                                                         "div.aCsJod.oJeWuf > div > div.Xb9hP > input")
    address_entry.send_keys(result["address"])
    price_entry = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > "
                                                       "div:nth-child(2) > div > div > div.AgroKb > div > "
                                                       "div.aCsJod.oJeWuf > div > div.Xb9hP > input")
    price_entry.send_keys(result["price"])
    url_entry = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child("
                                                     "3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > "
                                                     "div.Xb9hP > input")
    url_entry.send_keys(result["url"])
    submit = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb "
                                                  "> div.lRwqcd > div > span > span")
    submit.click()
