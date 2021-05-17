import os
import requests
import pandas as pd
import json
import bs4

"""
需要注意的是
不論是請求或響應
都要注意'台'和'臺'的差別

全家回傳的資料中
'台'和'臺'並不一致
要手動處理
"""


def seven_11():
    print("7-11 開始下載")
    url = 'https://emap.pcsc.com.tw/EMapSDK.aspx'
    post = list(pd.read_csv('post_url.csv')['行政區名'])
    store_detail_list = []

    for i in range(len(post)):
        print("7-11進度： " + str(i + 1) + " / " + str(len(post)))
        form_data = {
            'commandid': 'SearchStore',
            'city': post[i][0:3].replace('臺', '台'),
            'town': post[i][3:]
        }
        resp = requests.post(url, form_data)
        soup = bs4.BeautifulSoup(resp.text, "html5lib")

        for j in range(len(soup.find_all('poiid'))):
            store_detail = [
                soup.findAll('poiid')[j].text, soup.findAll('poiname')[j].text,
                soup.findAll('telno')[j].text, soup.findAll('address')[j].text
            ]
            store_detail = list(map(lambda x: x.strip(), store_detail))
            store_detail_list.append(store_detail)

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
            'city': post[i][0:3].replace('臺', '台'),
            'area': post[i][3:],
            'road': '',
            'fun': 'showStoreList',
            'key': '6F30E8BF706D653965BDE302661D1241F8BE9EBC'
        }

        resp = requests.post(url2, data=form_data, headers=headers)
        soup = bs4.BeautifulSoup(resp.text, "html5lib").find('body').text[14:-1]

        store_detail = json.loads(soup)
        for detail in store_detail:
            addr = detail['addr'].replace('臺北', '台北')
            addr = addr.replace('臺中', '台中')
            addr = addr.replace('臺南', '台南')
            store_detail_list.append([detail['pkey'], detail['NAME'], detail['TEL'], addr])

    print("全家 下載結束")
    return store_detail_list


"""

萊爾富的API有一套複雜的使用規則，
在請求時有點麻煩。

1. 要先取得token
2. 切換 CITY 需要重新取得token
3. form_data 裡的 '__EVENTTARGET' 有兩種參數 AREA 和 CITY，切換哪個就用哪個
4. 錯誤的表單會讓連線中斷
5. CITY改變時，AREA不變，反之 (所以每個城市的第一次特別處理)
6. 如果從該網頁取得 CITY 和 AREA 的 list，需要改變並請求不同的 CITY，AREA 才會刷新，否則只會有每個 CITY 的第一個 AREA。

這個method照著規則

也許有其他更簡單的方法

"""


def hi_life():
    print("萊爾富 開始下載")
    url = 'https://www.hilife.com.tw/storeInquiry_street.aspx'
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html5lib")

    view_state = soup.find(id='__VIEWSTATE')['value']
    viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
    event_validation = soup.find(id='__EVENTVALIDATION')['value']

    city_list = list(map(lambda x: x.text, soup.find(id='CITY').find_all()))

    target = 'AREA'
    area_tmp = '中正區'
    store_detail_list = []

    for city in city_list:

        form_data = {
            '__EVENTTARGET': target,
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': view_state,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            'CITY': city,
            'AREA': area_tmp
        }

        resp = requests.post(url, data=form_data)
        soup = bs4.BeautifulSoup(resp.text, "html5lib")
        area_list = list(map(lambda x: x.text, soup.find(id='AREA').find_all()))

        area_store_list = soup.find('tbody').find_all('tr')
        for store in area_store_list:
            store_detail_list.append([
                store.find_all('th')[0].text,
                store.find_all('th')[1].text,
                store.find_all('td')[1].text,
                store.find('a').text
            ])

        view_state = soup.find(id='__VIEWSTATE')['value']
        viewstate_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
        event_validation = soup.find(id='__EVENTVALIDATION')['value']

        for area in area_list:
            if area == area_list[0]:
                target = 'AREA'
                continue

            form_data = {
                '__EVENTTARGET': target,
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': viewstate_generator,
                '__EVENTVALIDATION': event_validation,
                'CITY': city,
                'AREA': area
            }

            resp = requests.post(url, data=form_data)
            soup = bs4.BeautifulSoup(resp.text, "html5lib")
            area_tmp = area

            area_store_list = soup.find('tbody').find_all('tr')
            for store in area_store_list:
                store_detail_list.append([
                    store.find_all('th')[0].text,
                    store.find_all('th')[1].text,
                    store.find_all('td')[1].text,
                    store.find('a').text
                ])

        target = 'CITY'
    print("萊爾富 結束下載")
    return store_detail_list


def ok_mark():
    print("OK超商 開始下載")
    store_detail_list = []
    url = 'https://www.okmart.com.tw/convenient_shopSearch_Result.aspx?key='
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html5lib")
    all_store_id = list(map(lambda x: str(x)[30:34], soup.find_all('a')))
    for i in all_store_id:
        url = 'https://www.okmart.com.tw/convenient_shopSearch_ShopResult.aspx?id=' + str(i)
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.text, "html5lib")

        name = soup.find('h1').text[0:-3].strip()
        tel = soup.find_all('li')[1].text[5:].strip()
        addr = soup.find_all('li')[0].text[5:].strip()

        store_detail_list.append([i, name, tel, addr])

    print("OK超商 結束下載")
    return store_detail_list


def download_store_data():
    s1 = pd.DataFrame(seven_11())
    s2 = pd.DataFrame(family_mart())
    s3 = pd.DataFrame(hi_life())
    s4 = pd.DataFrame(ok_mark())
    writer = pd.ExcelWriter('四大超商.xlsx')
    s1.to_excel(writer, index=None, header=["店號", "店名", "電話", "地址"], sheet_name="7-11")
    s2.to_excel(writer, index=None, header=["店號", "店名", "電話", "地址"], sheet_name="全家")
    s3.to_excel(writer, index=None, header=["店號", "店名", "電話", "地址"], sheet_name="萊爾富")
    s4.to_excel(writer, index=None, header=["店號", "店名", "電話", "地址"], sheet_name="OK")
    writer.save()
    print("下載完成")


def get_store(s_dict, data, name=""):
    for i in s_dict:
        for j in data.keys():
            if i in j:
                s_dict[i].append(name + data[j])
    return s_dict


def create_json():
    print("開始創建 行政區與便利商店.json")
    store_dict = {}
    post = list(map(lambda x: x.replace('臺', '台'), list(pd.read_csv('post_url.csv')['行政區名'])))
    seven = pd.read_excel('四大超商.xlsx', sheet_name="7-11", index_col='地址').to_dict()['店名']
    family = pd.read_excel('四大超商.xlsx', sheet_name="全家", index_col='地址').to_dict()['店名']
    hi = pd.read_excel('四大超商.xlsx', sheet_name="萊爾富", index_col='地址').to_dict()['店名']
    okm = pd.read_excel('四大超商.xlsx', sheet_name="OK", index_col='地址').to_dict()['店名']

    for i in post:
        store_dict[i] = []

    store_dict = get_store(store_dict, seven, '7-11 ')
    store_dict = get_store(store_dict, family)
    store_dict = get_store(store_dict, hi, '萊爾富 ')
    store_dict = get_store(store_dict, okm, 'OK ')

    with open('行政區與便利商店.json', mode='w', encoding='utf-8') as file:
        json.dump(store_dict, file)
    print("創建完成 行政區與便利商店.json")


if __name__ == '__main__':
    if not os.path.exists('四大超商.xlsx'):
        download_store_data()
    if not os.path.exists('行政區與便利商店.json'):
        create_json()
    else:
        print("檔案已經被創建")
