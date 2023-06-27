from urllib.request import urlopen
from bs4 import BeautifulSoup

myurl = "https://www.airport.kr/co/ko/cpr/statisticCategoryOfLocal.do"

response = urlopen(myurl)
html = response.read()

soup = BeautifulSoup(html, "html.parser")

print(soup.prettify())

trtag = soup.find("tr").string
print(trtag)
