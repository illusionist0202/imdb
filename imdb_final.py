import time

import requests
import pandas as pd
from pandas import ExcelWriter

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# inputs
url_add = str(input("Paste URL,Hit Space and then Enter\n"))
filename = str(input("name your output file\n"))

# runtime
start_time = time.time()

# calculating maxclicks
source_code = requests.get(url_add)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, 'html.parser')

for number_of_reviews in soup.findAll('div', {'class': 'header'}):
    c = number_of_reviews.text
    s = c.split()
    s = str(s[0])
    s = int(s.replace(",", ""))
    break
maxclicks = s//25
print('maxclicks='+str(maxclicks))


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 100)

driver.get(url_add)

# click more until no more results to load
clicks = 0
while True:
    clicks += 1
    if clicks <= maxclicks:
        more_button = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "ipl-load-more__button"))).click()

        # driver.find_element_by_class_name("ipl-load-more__button").click()

    else:
        break
    print(str(clicks) + "click")
print('out of loop')
time.sleep(25)
source_code = driver.page_source

# not source_code.text since here source_code is obtained from selenium is string not a beautifulsoup object

plain_text = source_code
soup = BeautifulSoup(plain_text, 'html.parser')
# print(soup)

database = []
pageno = 1
rating_list = []
title_list = []
review_list = []

for r in soup.findAll('div', {'class': 'lister-item-content'}):

    if "ipl-ratings-bar" in str(r):

        for rating in r.findAll('span', {'class': 'rating-other-user-rating'}):
            rating = str(rating.text)
            if rating == '':
                rating = 'NaN'
                rating_list.append(rating.strip())
            else:
                rating_list.append(rating.strip())
            # print(rating_list)
    else:

        rating = 'NaN'
        rating_list.append(rating.strip())

    for title in r.findAll('div', {'class': 'title'}):
        title = str(title.text)

        if title == '':
            title = 'NaN'
            title_list.append(title)
        else:
            title_list.append(title)

    for review in r.findAll('div', {'class': 'text'}):
        review = str(review.text)
        if review == '':
            review = 'NaN'
            review_list.append(review)
        else:
            review_list.append(review)

# print(title_list)
# print(rating_list)
# print(review_list)

df1 = pd.DataFrame(title_list, columns=['title'])
df2 = pd.DataFrame(rating_list, columns=['rating'])
df3 = pd.DataFrame(review_list, columns=['review'])
df12 = df1.join(df2)
df = df12.join(df3)
print(df)

# import openpyxl

writer = ExcelWriter(filename + '.xlsx')
df.to_excel(writer, 'Sheet1', index=False)
writer.save()

elapsed_time = time.time() - start_time
print(elapsed_time)
