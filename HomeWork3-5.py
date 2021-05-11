import time
import pandas as pd
import numpy as np
import requests


def hahow_crawl():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/59.0.3071.115 Safari/537.36'}
    categories = ['music', 'language', 'photography', 'art', 'design', 'humanities', 'marketing', 'programming',
                  'finance-and-investment', 'career-skills', 'handmade', 'lifestyle']

    hahow_statistics = []
    for cate in categories:
        single_categories_data = [cate]
        course_student = []
        course_pre_price = []
        course_price = []
        course_length = []
        for page in range(1, 3):
            URL = 'https://api.hahow.in/api/group/'
            resp = requests.get(URL + cate + '/courses?page=' + str(page), headers=headers).json()
            course_data = resp['data']

            if len(course_data) == 0:
                break

            for data in course_data:
                if data.get('totalVideoLengthInSeconds') is None:
                    break
                course_student.append(data['numSoldTickets'])
                course_pre_price.append(data['preOrderedPrice'])
                course_price.append(data['price'])
                course_length.append(data['totalVideoLengthInSeconds'] / 60)

            time.sleep(2)

        mean_data = [np.mean(course_student), np.mean(course_pre_price), np.mean(course_price), np.mean(course_length)]
        corrcoef = np.corrcoef([course_student, course_pre_price, course_price, course_length])
        corr = [corrcoef[0, 1], corrcoef[0, 2], corrcoef[0, 3]]
        single_categories_data.append(len(course_student))
        single_categories_data.extend(mean_data)
        single_categories_data.extend(corr)
        single_categories_data[2:9] = list(map(lambda x: round(x, 2), single_categories_data[2:9]))
        hahow_statistics.append(single_categories_data)
        print(cate + " 類完成")
        print(single_categories_data)
    headers = ['課程類別', '課程總數', '學生均數 a', '募資均價 b', '線上均價 c', '平均課長 d(分鐘)', '相關係數 ab', '相關係數 ac', '相關係數 ad']
    hahow_statistics = pd.DataFrame(hahow_statistics)
    hahow_statistics.to_csv('hahow_statistics.csv', header=headers, index=0)


if __name__ == '__main__':
    hahow_crawl()
