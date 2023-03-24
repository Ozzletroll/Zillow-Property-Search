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
TARGET_URL = ""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Accept-Language": "en-GB,en;q=0.5",
}
response = requests.get(TARGET_URL, headers=headers)
response.encoding = "utf-8"
html_text = response.text
soup = BeautifulSoup(html_text, "html.parser")


# Selenium driver setup
service = Service("C:/Program Files (x86)/Google/Chrome/chromedriver.exe")
options = ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)

driver.get(GOOGLE_FORM_URL)
