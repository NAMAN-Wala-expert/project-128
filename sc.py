from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars"


browser = webdriver.Chrome()
browser.get(START_URL)
time.sleep(100)
scraped_data1 = []


def scrape_more_data(hyperlink) :
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_lists = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}) :
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags :
                try:
                    temp_lists.append(td_tag.find_all("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    temp_lists.append("")
        scraped_data1.append(temp_lists)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)



planet_df = pd.read_csv("scraped_data.csv")


for index,row in planet_df.iterrows() :
    print(row['hyperlink'])
    scrape_more_data(row['hyperlink'])
    print(f"data scraping at hyperlink{index + 1} completed")


    
print(scraped_data1[0:10])
scraped_data = []


for row in scraped_data1 : 
    replaced = []
    for el in row :
        el = el.replace("\n","")
        replaced.append(el)
    scraped_data.append(replaced)


print(scraped_data)