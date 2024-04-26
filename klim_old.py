from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

# driver = webdriver.Edge()
driver = webdriver.Chrome()

url = "https://htreviews.org/experts"

driver.get(url)

last_height = 0

position = []
rating = []
stats = []
reviews = []

scrll_ps_tm = 0.4

while True:
    html = driver.page_source

    driver.maximize_window()

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(scrll_ps_tm)
    driver.execute_script("window.scrollTo(0, document.body.scrollTop);")
    time.sleep(scrll_ps_tm)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(html, "html.parser")

items = soup.find_all(class_="experts_list_item")

for item in items:
    parent_div1 = item.find(class_="experts_list_item_position")
    parent_div2 = item.find(class_="list_item_rating")
    parent_div3 = item.find(class_="list_item_stats")
    parent_div4 = item.find(class_="list_item_reviews")

    pos_elem = int(parent_div1.find_all("p")[0].string)
    rat_elem = int(parent_div2.find_all("span")[0].string)
    stat_elem = int(parent_div3.find_all("span")[0].string)
    rev_elem = int(parent_div4.find_all("span")[0].string)

    position.append(pos_elem)
    rating.append(rat_elem)
    stats.append(stat_elem)
    reviews.append(rev_elem)

driver.close()
driver.quit()

df = pd.DataFrame({
    "Position": position,
    "Rating"  : rating,
    "Stats"   : stats,
    "Reviews" : reviews
})

df.to_csv("test.csv", index=False)
