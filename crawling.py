from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen

driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/discordbot/chromedriver')
driver.implicitly_wait(60)

driver.get("https://www.naver.com")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

naver_rank = soup.select('#NM_RTK_ROLLING_WRAP > ul > li:nth-child(1)')



for list in naver_rank:
    print(list.text.strip())
