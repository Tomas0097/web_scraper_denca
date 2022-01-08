import time
import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

workbook = xlsxwriter.Workbook('databaze.xlsx')
worksheet = workbook.add_worksheet()

# ----------------------------------------------------------------------------------------------------------------------------
# Fields
# ----------------------------------------------------------------------------------------------------------------------------
F_EXHIBITOR_NAME = "Exhibitor Name"
# Field with same names as on the web:
F_FEATURED_EXHIBITOR = "Featured Exhibitor"
F_COUNTRY_PAVILON = "Country Pavilion"
F_COUNTRY = "Country"
F_COUNTRY_COVERAGE = "Country Coverage"
F_NATURE_OF_BUSINESS = "Nature of Business"
F_INTERESTED_TO_CONNECT_WITH = "Interested to connect with"
F_PRODUCT_CATEGORY_OFFERED = "Product Category Offered"
F_PRODUCT_SUBCATEGORY_OFFERED = "Product Sub-category Offered"
# Social media fields:
F_FACEBOOK = "Facebook"
F_INSTAGRAM = "Instagram"
F_TWITTER = "Twitter"
F_LINKEDIN = "Linkedin"
F_YOUTUBE = "Youtube"
F_PINTEREST = "Pinterest"
# Contact fields:


# Sets the column number for the fields.
WORKSHEET_FIELDS_COLUMNS = {
    F_EXHIBITOR_NAME: 0,
    F_FEATURED_EXHIBITOR: 1,
    F_COUNTRY_PAVILON: 2,
    F_COUNTRY: 3,
    F_COUNTRY_COVERAGE: 4,
    F_NATURE_OF_BUSINESS: 5,
    F_INTERESTED_TO_CONNECT_WITH: 6,
    F_PRODUCT_CATEGORY_OFFERED: 7,
    F_PRODUCT_SUBCATEGORY_OFFERED: 8,
    F_FACEBOOK: 9,
    F_INSTAGRAM: 10,
    F_TWITTER: 11,
    F_LINKEDIN: 12,
    F_YOUTUBE: 13,
    F_PINTEREST: 14,
}

# Write headers into worksheet
for k, v in WORKSHEET_FIELDS_COLUMNS.items():
    worksheet.write(0, v, k)

# Starting rows. Rows are zero indexed. Headers are in row: 0
row = 1

with open("my_projects/web_scraper_denca/list_urls_exhibitor_detail.txt", "r") as file:
    for url in range(1):
        driver.get("https://connections.arabhealthonline.com/event/arab-health-10/exhibitor/RXhoaWJpdG9yXzYxNDU2OA%3D%3D")
        time.sleep(2)  # Allow 2 seconds for the web page to open

        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_all_fields = soup.select_one(".sc-eQGPmX")
        div_basic_fields = div_all_fields.find_all("div", {"class": "sc-kbGplQ"})
        div_social_media_fields = div_all_fields.find_all("a")

        # Save Exhibitor name
        exhibitor_name = div_all_fields.select_one(".sc-hMjcWo").text
        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EXHIBITOR_NAME], exhibitor_name)

        # Save basic information
        for field in div_basic_fields:
            field_name = field.select_one(".sc-exdmVY").text

            if field_name in [F_COUNTRY_PAVILON, F_NATURE_OF_BUSINESS]:
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[field_name], field.contents[1].text)

            elif field_name in [F_COUNTRY, F_COUNTRY_COVERAGE, F_INTERESTED_TO_CONNECT_WITH, F_PRODUCT_CATEGORY_OFFERED, F_PRODUCT_SUBCATEGORY_OFFERED]:
                spans = field.find_all("span", {"class": "sc-fATqzn"})
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[field_name], ", ".join([s.text for s in spans]))

        # Save social media information
        for field in div_social_media_fields:
            href = field["href"]

            if F_FACEBOOK.lower() in href:
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_FACEBOOK], href)
            elif F_INSTAGRAM.lower() in href:
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_INSTAGRAM], href)
            elif F_TWITTER.lower() in href:
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_TWITTER], href)
            elif F_LINKEDIN.lower() in href:
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_LINKEDIN], href)
            elif F_PINTEREST.lower() in href:
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_PINTEREST], href)
            elif F_YOUTUBE.lower() in href:
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_YOUTUBE], href)

        row += 1


workbook.close()
