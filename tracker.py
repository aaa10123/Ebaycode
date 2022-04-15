import webbrowser
import pandas as pd
import urllib
from urllib import request
from time import sleep
import selenium
from selenium import webdriver
import numpy as np



driver = webdriver.Chrome(executable_path=r"C:\Users\Dov Fischman\Desktop\chromedriver.exe")

df = pd.read_excel(r"C:\Users\Dov Fischman\Desktop\code\new-python\ebay calc\ebay2.xlsx")

delivered = []
for val in df['tracking']:
    if type(val) is str:
        URL = ('https://t.17track.net/en#nums=' + val)
        driver.get(URL)
        sleep(5)
        content = driver.page_source
        if 'Delivered ' in content:
            delivered.append(val)
for val in df['tracking']:
    if val in delivered:
        df['tracking'].mask(df['tracking'] == val, val + ' yes', inplace=True)
df.to_excel(r"C:\Users\Dov Fischman\Desktop\code\new-python\ebay calc\ebay24.xlsx", index=False)
