import time
import pandas as pd
import numpy as np
import json
import requests
from bs4 import BeautifulSoup

"""
課程類別, 課程總數, 學生均數 a, 募資均價 b, 線上均價 c, 平均課長 d(分鐘), 相關係數 ab, 相關係數 ac, 相關係數 ad
"""

CATEFORIES = ['music', 'language', 'photography', 'art', 'design', 'humanities', 'marketing', 'programming',
              'finance-and-investment', 'career-skills', 'handmade', 'lifestyle']
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/59.0.3071.115 Safari/537.36'}
test = []
for page in range(1, 2):
    URL = 'https://api.hahow.in/api/group/'
    resp = requests.get(URL + 'music/courses?page=' + str(page), headers=HEADERS).json()
    course_data = resp['data']

    if len(course_data) == 0:
        break

    for data in course_data:
        test.append([data['numSoldTickets'], data['preOrderedPrice'], data['price'], data['totalVideoLengthInSeconds']/60])

    time.sleep(2)

print(test)
print(len(test))
print(sum(test[3]))
corrcoef = np.corrcoef([test[0], test[1], test[2], test[3]])
print('募資價與學生數之相關係數: ', corrcoef[0, 1])  # 0.18
print('上線價與學生數之相關係數: ', corrcoef[0, 2])  # 0.36
print('課程長度與學生數之相關係數: ', corrcoef[0, 3])  # 0.65


test = pd.DataFrame(test)
#
# # HEADERS = ['課程類別', '課程總數', '學生均數 a', '募資均價 b', '線上均價 c', '平均課長 d(分鐘)', '相關係數 ab', '相關係數 ac', '相關係數 ad']
HEADERS = ['a','b','c','d']
test.to_csv('hahow_statistics.csv', header=HEADERS, index=0)


# soup = json.loads(soup)
# print(soup)
# print(data)
