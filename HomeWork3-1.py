import requests
from bs4 import BeautifulSoup

keyword = str(input("請輸入中文或英文以進行翻譯： "))
resp = requests.get('https://tw.dictionary.search.yahoo.com/search?p=' + keyword)
soup = BeautifulSoup(resp.text, 'html.parser')

res1 = soup.findAll('div', 'dictionaryExplanation')
res2 = soup.findAll('div', 'pos_button')

for i in range(len(res1)):
    if len(res2) > 0:
        print(res2[i].text, end=" ")
    print(res1[i].text)

if len(res1) == 0:
    print("Invalid query!")