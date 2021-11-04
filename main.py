from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib

page = "https://www.six-group.com/en/products-services/" \
       "the-swiss-stock-exchange/market-data/shares/share-explorer/share-details.CH0012221716CHF4.html#/"
full_page = urlopen(page)

bs = BeautifulSoup(full_page, 'html.parser')
print(bs.h1)

dataKeyList = bs.find_all('dt', {'class': 'data-pair-key'})
dataValueList = bs.find_all('dd', {'class': 'data-pair-value'})
for key in dataKeyList:
    print(key.get_text())
for value in dataValueList:
    print(value.get_text())