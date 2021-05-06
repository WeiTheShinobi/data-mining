import requests
import bs4
import re
import json
import time


def article_crawler(url):
    my_headers = {'cookie': 'over18=1;'}
    response = requests.get(url, headers=my_headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    header = soup.find_all('span', 'article-meta-value')
    author = header[0].text
    board = header[1].text
    title = header[2].text
    date = header[3].text

    main_container = soup.find(id='main-container')
    all_text = main_container.text
    pre_text = all_text.split('--')[0]

    texts = pre_text.split('\n')
    contents = texts[2:]
    content = '\n'.join(contents)

    return date, content


def save(list_date, list_content):
    file_date = open("ptt/date.txt", mode='w', encoding='utf-8')
    file_content = open("ptt/content.txt", mode='w', encoding='utf-8')
    json.dump(list_date, file_date)
    json.dump(list_content, file_content)
    file_date.close()
    file_content.close()


def index_crawler(start_index, end_index):
    list_date = []
    list_content = []

    for index in range(start_index, end_index):
        my_headers = {'cookie': 'over18=1;'}
        resp = requests.get('https://www.ptt.cc/bbs/Gossiping/index' + str(index) + '.html', headers=my_headers)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        index_article_urls = soup.find_all('a', href=re.compile("/bbs/Gossiping/M"))

        for article_url in index_article_urls:
            date, content = article_crawler("https://www.ptt.cc" + article_url['href'])
            time.sleep(0.1)
            list_date.append(date)
            list_content.append(content)
        print("第 " + str(index) + " 頁完成，目前共 " + str(index + 1 - start_index) + " 頁完成，還剩 " + str(
            end_index - index - 1) + " 頁，文章數： " + str(len(list_date)))

        if index % 20 == 0:
            save(list_date, list_content)
            print("儲存")

    print("完成")


index_crawler(29056, 31212)
