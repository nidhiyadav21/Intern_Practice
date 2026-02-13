import requests
from bs4 import BeautifulSoup


#1. Fetch HTML

def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    return response.text
#2.Extract Title

def extract_title(soup):
    title = soup.find("h1")
    return title.get_text(strip=True)if title else "No Title Found"

#3.Extract Headings and Paragraphs
def extract_content(soup):
    content_data = []

    for tag in soup.find_all(["h2","h3","p"]):
        text =(tag.get_text(strip=True))
        if text:
            content_data.append(text)
    return content_data

#4.Extract Code Blocks
def extract_code(soup):
    codes = []
    for code in soup.find_all("pre"):
        codes.append(code.get_text())
    return codes

def main():
    url = "https://www.geeksforgeeks.org/web-scraping/introduction-to-web-scraping/"
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    print("\n --- TITLE ---\n")
    print(extract_title(soup))
    print("\n --- CONTENT ---\n")

    content = extract_content(soup)
    for line in content[:20]:
        print(line)
    print("\n --- CODE ---\n")
    codes = extract_code(soup)
    for c in codes:
        print(c)
        print("-" * 50)

if __name__ == "__main__":
    main()



