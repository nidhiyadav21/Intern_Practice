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
for page in range(0,4):
    print(f"Scraping page {page}...")

    #Get all rows
    rows = driver.find_elements(By.CSS_SELECTOR, ".team")

    for row in rows:
        team_name = row.find_element(By.CSS_SELECTOR, ".name").text.strip()
        year = row.find_element(By.CSS_SELECTOR, ".year").text.strip()
        wins = row.find_element(By.CSS_SELECTOR, ".wins").text.strip()
        losses = row.find_element(By.CSS_SELECTOR, ".losses").text.strip()
        pct = row.find_element(By.CSS_SELECTOR, ".pct").text.strip()

        data = {
            "Team": team_name,
            "Year": year,
            "Wins": wins,
            "Losses": losses,
            "Win %": pct,
        }

        all_data.append(data)

        #Click next page if not last
    # if page < 4:
    #     next_button_css = f'a[aria-label="Page {page+1}"]'
    #     next_button = driver.find_element(By.CSS_SELECTOR,f'a[aria-label="Page {page+1}"]')
    #     next_button.click()
    #     time.sleep(2)

    # Click next page if not last
    if page < 4:
        # 1. Scroll to the bottom so the pagination is visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        try:
            # 2. Use a simpler CSS selector to find the 'Next' link (>>)
            # This looks for the link inside the 'next' list item
            next_button = driver.find_element(By.CSS_SELECTOR, "ul.pagination li a[aria-label='Next']")
            next_button.click()

            # 3. Wait for the page to refresh
            time.sleep(2)
        except Exception as e:
            print(f"Error navigating to page {page + 1}: {e}")
            break

print("\nTotal Records:",len(all_data))
print("\nFirst 5 Records:\n")

for item in all_data[:5]:
        print(item)

driver.quit()