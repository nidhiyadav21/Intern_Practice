from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Start Webdriver
driver = webdriver.Chrome()
driver.get("https://www.scrapethissite.com/pages/forms/")
driver.maximize_window()

time.sleep(2)
all_data =[]

#website has 4 pages
for page in range(1,5):
    print(f"Scraping page {page}...")

    #Get all rows
    rows = driver.find_elements(By.CLASS_NAME, "team")

    for row in rows:
        team_name = row.find_element(By.CLASS_NAME, "name").text.strip()
        year = row.find_element(By.CLASS_NAME, "year").text.strip()
        wins = row.find_element(By.CLASS_NAME, "wins").text.strip()
        losses = row.find_element(By.CLASS_NAME, "losses").text.strip()
        pct = row.find_element(By.CLASS_NAME, "pct").text.strip()

        data = {
            "Team": team_name,
            "Year": year,
            "Wins": wins,
            "Losses": losses,
            "Win %": pct,
        }

        all_data.append(data)

        #Click next page if not last
        if page < 4:
            next_button = driver.find_element(By.LINK_TEXT, str(page + 1))
            next_button.click()
            time.sleep(2)
        print("\nTotal Records:",len(all_data))
        print("\nFirst 5 Records:\n")

        for item in all_data[:5]:
            print(item)

        driver.quit()