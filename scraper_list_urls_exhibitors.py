import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL_EXHIBITORS_LIST = "https://connections.arabhealthonline.com/event/arab-health-10/exhibitors/RXZlbnRWaWV3XzI5NjEzNw%3D%3D?_ga=2.4837744.2111117049.1641415109-843008023.1641415109&search=&fbclid=IwAR0ROqmN6Ob_h-YcnlwaiLqXF1BILlrbR5IXwPRT6GjlNQpeVS3fdkyYl_I"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL_EXHIBITORS_LIST)
time.sleep(2)  # Allow 2 seconds for the web page to open

urls_path_exhibitor_detail_page = []
screen_height = driver.execute_script("return window.screen.height;")
i = 1


while True:
    # scroll one screen height each time
    driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
    i += 1
    time.sleep(1)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")

    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if screen_height * i > scroll_height:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")
for a in soup.select_one(".infinite-scroll-component").find_all("a"):
    urls_path_exhibitor_detail_page.append(a.attrs["href"])

print(f"Number of scraped detail exhibitor urls: {len(urls_path_exhibitor_detail_page)}")

with open("list_urls_exhibitor_detail.txt", "w") as list_urls_exhibitor_detail:
    for element in urls_path_exhibitor_detail_page:
        list_urls_exhibitor_detail.write(f"https://connections.arabhealthonline.com{element}\n")

# Turn off Chrome driver session
driver.close()
