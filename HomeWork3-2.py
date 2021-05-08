import os

import requests
import bs4
import re
import json
import time
import matplotlib.pyplot as plt
import pandas as pd


def crawl_article(url):
    try:
        my_headers = {'cookie': 'over18=1;'}
        response = requests.get(url, headers=my_headers)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        header = soup.find_all('span', 'article-meta-value')
        date = header[3].text

        main_container = soup.find(id='main-container')
        all_text = main_container.text
        pre_text = all_text.split('--')[0]

        texts = pre_text.split('\n')
        contents = texts[2:]
        content = '\n'.join(contents)
    except Exception as e:
        print(e)
        date = ""
        content = ""

    return date, content


def save(list_date, list_content):
    file_date = open("ptt/date.txt", mode='w', encoding='utf-8')
    file_content = open("ptt/content.txt", mode='w', encoding='utf-8')
    json.dump(list_date, file_date)
    json.dump(list_content, file_content)
    file_date.close()
    file_content.close()
    print("儲存")


def crawl_index(start_index, end_index):
    list_date = []
    list_content = []

    for index in range(start_index, end_index):
        my_headers = {'cookie': 'over18=1;'}
        resp = requests.get('https://www.ptt.cc/bbs/Gossiping/index' + str(index) + '.html', headers=my_headers)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        index_article_urls = soup.find_all('a', href=re.compile("/bbs/Gossiping/M"))

        for article_url in index_article_urls:
            date, content = crawl_article("https://www.ptt.cc" + article_url['href'])
            if date != "":
                time.sleep(0.1)
                list_date.append(date)
                list_content.append(content)

        print("第 " + str(index) + " 頁完成，目前共 " + str(index + 1 - start_index) + " 頁完成，還剩 " + str(
            end_index - index - 1) + " 頁，文章數： " + str(len(list_date)))

        if index % 50 == 0:
            save(list_date, list_content)

    save(list_date, list_content)
    print("完成")


def parse_time(file):
    date_list = json.load(file)
    for i in range(len(date_list)):
        date_list[i] = date_list[i][11:19]

    data = pd.DataFrame(date_list, columns=["time"])
    data = pd.to_datetime(data['time'], format="%H:%M:%S", errors='ignore')

    frequency = []
    for i in range(24):
        time1 = str(i) + ":00:00"
        time2 = str(i) + ":59:59"
        if i < 10:
            time1 = "0" + time1
            time2 = "0" + time2

        tmp = data[time1 < data]
        tmp = tmp[tmp < time2]
        frequency.append(len(tmp))

    return frequency


def draw_table(frequency):
    tmp = []
    tmp.extend(frequency[6:24])
    tmp.extend(frequency[0:6])

    x1 = [i for i in range(6, 24)]
    x2 = [i for i in range(0, 6)]
    x1.extend(x2)

    x = [i for i in range(24)]

    plt.bar(x, tmp)
    plt.xticks(x, x1)
    plt.xlabel("time")
    plt.ylabel("frequency")
    plt.title("PTT")
    plt.show()


if __name__ == '__main__':
    if not os.path.exists('ptt/date.txt'):
        crawl_index(29056, 31212)

    ptt_time = open("ptt/date.txt", mode='r', encoding='utf-8')
    frequency = parse_time(ptt_time)
    draw_table(frequency)
