import urllib.request
from bs4 import BeautifulSoup
# import requests

url = "https://www.imdb.com/title/tt0050212/"
url = "http://www.imdb.com/title/tt0049406/"

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "lxml")

# all_tables = soup.find_all("table")

right_table = soup.find('div', class_='poster')

imglink = right_table.find('img').get('src')

urllib.request.urlretrieve(imglink, 'fun.jpg')
