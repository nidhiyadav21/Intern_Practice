import requests
from bs4 import BeautifulSoup

with open("sample.html","r") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
# print(soup.prettify())

#Title
# print(soup.title.string,type(soup.title))

#div
# print(soup.div)

# print(soup.find_all("div"))

for link in soup.find_all("a"):
    print(link.get("href"))
    print(link.get_text())

s = soup.find(id="link3")
print(s.get("href"))

print(soup.select("div.italic"))


