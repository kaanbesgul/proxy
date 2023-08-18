from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.by import By
from math import *
import time
import requests
from bs4 import BeautifulSoup
from random import choice

#Get ip from https://www.sslproxies.org/ website format like ip:port

def getProxy():
    url="https://www.sslproxies.org/"
    r=requests.get(url=url)
    soup=BeautifulSoup(r.content,'html.parser')
    return choice(list(map(lambda x: x[0]+":"+x[1],list(zip(list(map(lambda x:x.text,soup.find_all('td')[::8])),(map(lambda x:x.text,soup.find_all('td')[1::8])))))))


#Check if the proxy is accessing the site I want

def check_proxy():
    proxy=getProxy()
    

    if "." in proxy:
        print(proxy)
    else:
        check_proxy()


    proxies={
        "http":proxy
    }

    try:
        response = requests.get("https://www.instagram.com/", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("Proxy calisiyor.")
            return proxy
        else:
            print("Proxy calismiyor. Yanit kodu:", response.status_code)
            check_proxy()
    except requests.exceptions.RequestException as e:
        print("Proxy baglantisi basarisiz:", str(e))
        check_proxy()



def prepare_browser():

    proxy=check_proxy()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options= chrome_options)
    stealth(driver=driver,
        user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
        languages= ["tr-TR", "tr"],
        vendor=  "Google Inc.",
        platform=  "Win32",
        webgl_vendor=  "Intel Inc.",
        renderer=  "Intel Iris OpenGL Engine",
        fix_hairline= True,
        run_on_insecure_origins= False,
        )
    return driver

def scrape():
    url = f'https://www.instagram.com/'
    chrome = prepare_browser()
    chrome.get(url)
    print (f"Attempting: {chrome.current_url}")
    if "login" in chrome.current_url:
        print ("Failed/ redir to login")
        chrome.quit()
    else:
        print ("Success")
        time.sleep(10)
        resp_body = chrome.find_element(By.TAG_NAME, "body").text
        print(resp_body)
        chrome.quit()

scrape()