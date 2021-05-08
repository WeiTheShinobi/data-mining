import googlemaps
from googlemaps import client
import time
import json


def google_map_search(lat, lng, search_radius, search_keyword, page_token=None, store_amount=0, detail=[]):
    search_result = client.places_nearby(user, location=(float(lat), float(lng)), radius=search_radius,
                                         keyword=search_keyword, page_token=page_token)
    store_amount += len(search_result['results'])
    detail.extend(search_result['results'])
    if search_result.get('next_page_token') is None:
        return store_amount, detail
    else:
        time.sleep(2)
        return google_map_search(lat, lng, search_radius, search_keyword, search_result.get('next_page_token'),
                                 store_amount,
                                 detail)


if __name__ == '__main__':
    GOOGLE_API_KEY = '輸入API KEY'
    user = googlemaps.Client(key=GOOGLE_API_KEY)
    school = client.places(user, '逢甲大學')
    lat = school['results'][0]["geometry"]["location"]["lat"]
    lng = school['results'][0]["geometry"]["location"]["lng"]

    print("逢甲大學")
    print("地址： ", end="")
    print(school['results'][0]["formatted_address"])
    print("座標： ", end="")
    print(lat, end=", ")
    print(lng)
    print()

    print("搜尋逢甲大學附近的店家數")
    search_radius = input("請輸入搜尋半徑(公尺) ：")
    search_keyword = str(input("請輸入關鍵字 ："))

    with open(search_radius + "_" + search_keyword + ".json", mode='w', encoding='utf-8') as file:
        store_amount, detail = google_map_search(lat, lng, search_radius, search_keyword)
        json.dump(detail, file)

        print(str(store_amount) + " 家")
        print("檔案已生成")
