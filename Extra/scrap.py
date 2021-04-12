import selenium
from selenium import webdriver as wb
import pandas as pd
import time

webD=wb.Chrome('/home/akshay/Downloads/chromedriver_linux64 (1)/chromedriver')

webD.get('https://www.amazon.in/s?k=redmi+note+5+pro')


listOflinks =[]
condition =True
while condition:
    time.sleep(3)
    productInfoList=webD.find_elements_by_class_name('a-size-mini')
    for el in productInfoList:
        if(el.text !=""):
            pp2=el.find_element_by_tag_name('a')
            listOflinks.append(pp2.get_property('href'))
    try:
        webD.find_element_by_class_name('a-link-normal').find_element_by_tag_name('a').get_property('href')
        webD.find_element_by_class_name('a-last').click()
    except:
        condition=False

len(listOflinks)