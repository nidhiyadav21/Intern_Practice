import requests
from bs4 import BeautifulSoup


base_url = "http://www.scrapethissite.com/pages/forms/"

def fetch_page(page_number):
    if page_number == 1:
        url = base_url
    else:
        url = f"{base_url}?page_num={page_number}"
    response = requests.get(url)


    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch page:",page_number)
        return None

def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")
    teams = soup.find_all("tr",class_="team")
    page_data = []

    for team in teams:
        team_name = team.find("td",class_="name").text.strip()
        year = team.find("td",class_="year").text.strip()
        wins = team.find("td",class_="wins").text.strip()
        losses = team.find("td",class_="losses").text.strip()
        #win_percentage = team.find("td",class_="win_percentage").text.strip()

        data ={
            "Team":team_name,
            "Year":year,
            "Wins":wins,
            "Losses":losses,
           # "Win Percentage":win_percentage,
        }
        page_data.append(data)

    return page_data

def scrape_all_pages(total_pages):
    all_data = []
    for page in range(1,total_pages+1):
        print(f"Scraping page {page}...")
        html = fetch_page(page)

        if html:
            page_data = extract_data(html)
            all_data.extend(page_data)

    return all_data

def main():
    # total_pages = 4
    # data = scrape_all_pages(total_pages)
    #
    # print("\nTotal Records:",len(data))
    # print("\nFirst 5 Records:\n")
    # for item in data[:5]:
    #     print(item)

    total_pages = 4
    data = scrape_all_pages(total_pages)

    print("\n--- SCRAPING VERIFICATION ---")

    # Each page has 25 records.
    # We loop from 0 to 100, skipping 25 records at a time.
    for page_num in range(total_pages):
        start_index = page_num * 25
        end_index = start_index + 5

        print(f"\nFirst 5 Records of Page {page_num + 1}:")
        print("-" * 30)

        # Slice the data for the current page's first 5 items
        page_chunk = data[start_index:end_index]

        for item in page_chunk:
            print(item)

if __name__ == "__main__":
    main()




