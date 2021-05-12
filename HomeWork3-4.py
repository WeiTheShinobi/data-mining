import requests
import pandas as pd
import json
import bs4
import time


def seven_11():
    print("7-11 開始下載")
    url = 'https://emap.pcsc.com.tw/EMapSDK.aspx'
    post = list(pd.read_csv('post_url.csv')['行政區名'])
    store_detail_list = []

    for i in range(len(post)):
        print("7-11進度： " + str(i + 1) + " / " + str(len(post)))
        form_data = {
            'commandid': 'SearchStore',
            'city': post[i][0:3],
            'town': post[i][3:7]
        }
        resp = requests.post(url, form_data)
        soup = bs4.BeautifulSoup(resp.text, "html5lib")
        if soup.find('poiid') is not None:
            for j in range(len(soup.find('poiid'))):
                store_detail = [
                    soup.findAll('poiid')[j].text, soup.findAll('poiname')[j].text,
                    soup.findAll('telno')[j].text, soup.findAll('address')[j].text
                ]
                store_detail = list(map(lambda x: x.strip(), store_detail))
                store_detail_list.append(store_detail)
        time.sleep(0.2)

    print("7-11 結束下載")
    return store_detail_list


def family_mart():
    print("全家 開始下載")
    headers = {'Referer': 'https://www.family.com.tw/marketing/inquiry.aspx'}

    url = 'https://www.family.com.tw/marketing/inquiry.aspx#'
    url2 = 'https://api.map.com.tw/net/familyShop.aspx?'

    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html5lib")

    view_state = soup.find(id='__VIEWSTATE')['value']
    viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']

    post = list(pd.read_csv('post_url.csv')['行政區名'])
    store_detail_list = []

    for i in range(len(post)):
        print("全家進度： " + str(i + 1) + " / " + str(len(post)))
        form_data = {
            '__VIEWSTATE': view_state,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            'searchType': 'ShopList',
            'type': '',
            'city': post[i][0:3],
            'area': post[i][3:7],
            'road': '',
            'fun': 'showStoreList',
            'key': '6F30E8BF706D653965BDE302661D1241F8BE9EBC'
        }

        resp = requests.post(url2, data=form_data, headers=headers)
        soup = bs4.BeautifulSoup(resp.text, "html5lib").find('body').text[14:-1]

        store_detail = json.loads(soup)
        for detail in store_detail:
            store_detail_list.append([detail['pkey'], detail['NAME'], detail['TEL'], detail['addr']])
        time.sleep(0.2)

    print("全家 下載結束")
    return store_detail_list


def hi_life():
    print("萊爾富 開始下載")
    url = 'https://www.hilife.com.tw/storeInquiry_street.aspx'
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html5lib")

    view_state = soup.find(id='__VIEWSTATE')['value']
    viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
    event_validation = soup.find(id='__EVENTVALIDATION')['value']

    city_list = list(map(lambda x: x.text, soup.find(id='CITY').find_all()))

    for city in city_list:

    form_data = {
        '__EVENTTARGET': 'AREA',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': viewstate_generator,
        '__EVENTVALIDATION': event_validation,
        'CITY': '台北市',
        'AREA': '大同區'
    }

    resp = requests.post(url, data=form_data)
    soup = bs4.BeautifulSoup(resp.text, "html5lib")

    print("萊爾富 結束下載")


def ok_mark():
    print("OK超商 開始下載")
    print("OK超商 結束下載")


if __name__ == '__main__':
    # seven_11()
    # family_mart()
    hi_life()
