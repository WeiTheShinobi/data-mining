import googlemaps
import time
import json

"""
取得googlemaps.Client物件並傳入key參數
使用googlemaps.client時放入即可使用
"""


def google_map_search(user, lat, lng, radius, keyword, page_token=None, store_amount=0, detail=[]):
    result = googlemaps.client.places_nearby(user,
                                             location=(float(lat), float(lng)),
                                             radius=radius,
                                             keyword=keyword,
                                             page_token=page_token)
    store_amount += len(result['results'])
    detail.extend(result['results'])
    if result.get('next_page_token') is None:
        return store_amount, detail
    else:
        time.sleep(2)
        return google_map_search(user, lat, lng, radius, keyword,
                                 result.get('next_page_token'),
                                 store_amount,
                                 detail)


if __name__ == '__main__':
    GOOGLE_API_KEY = '輸入API KEY'
    user = googlemaps.Client(key=GOOGLE_API_KEY)
    school = googlemaps.client.places(user, '逢甲大學')
    lat = school['results'][0]["geometry"]["location"]["lat"]
    lng = school['results'][0]["geometry"]["location"]["lng"]

    print("逢甲大學")
    print("地址： " + school['results'][0]["formatted_address"])
    print("座標： " + str(lat) + ", " + str(lng))

    print("搜尋逢甲大學附近的店家數")
    radius = input("請輸入搜尋半徑(公尺) ：")
    keyword = str(input("請輸入關鍵字 ："))

    with open(radius + "_" + keyword + ".json", mode='w', encoding='utf-8') as file:
        store_amount, detail = google_map_search(user, lat, lng, radius, keyword)
        json.dump(detail, file, indent=2, sort_keys=True, ensure_ascii=False)
        print(str(store_amount) + " 家")
        print("檔案 " + radius + "_" + keyword + ".json 已生成")
