from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
import os
from time import sleep
url = "https://www.twitch.tv/directory/all"

def main():
    channels = set() # tee tästä setti?
    service = Service(executable_path=(os.getcwd() + 'chromedriver.exe'))
    opt = webdriver.ChromeOptions()
    opt.add_argument('headless')
    driver = webdriver.Chrome(options=opt,service=service)
    driver.implicitly_wait(10)
    driver.get(url)
    sleep(5)
    #print(bs(driver.page_source,'html5lib').prettify())
    souped = bs(driver.page_source, 'html5lib')
    souped = souped.find('div',{"class":"root-scrollable scrollable-area"})
    print(souped.prettify())
    t = ""

    while len(channels) < 500:
        souped = bs(driver.page_source, 'html5lib')
        souped = souped.find('div', {"class": "root-scrollable scrollable-area"})
        for item in souped.find_all('p', {"class":"CoreText-sc-1txzju1-0 jiepBC"}):
            try:
                #channels.append(('#' + item['title']))
                channels.add(item['title'])
                t = item['title']
                print(item['title'])

            except KeyError:
                pass
        if(len(channels) > 0):
            scrollTarget = driver.find_element(By.XPATH, f"//p[@title='{t}']")
            scrollTarget = ScrollOrigin.from_element(scrollTarget)
            #ActionChains(driver).scroll_to_element(scrollTarget).perform()
            ActionChains(driver).scroll_from_origin(scrollTarget,0,1000).perform()
            sleep(2)
            print(len(channels))
            #print("herer :" + scrollTarget.text)



    print(type(souped))
    driver.quit()
    print(len(channels))
    print(channels)
    return channels






if __name__ == '__main__':
    main()