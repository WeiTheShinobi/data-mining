from math import *
import pandas as pd
import numpy as np


def create_nearest_site_csv():
    points = pd.read_csv('static/景點.csv')
    points_name = points['地點'].tolist()
    points_lat = points['經度'].tolist()
    points_lng = points['緯度'].tolist()

    csv_data = []
    for i, point_name in enumerate(points_name):
        tmp = [point_name]
        tmp.extend(__get_distance_point_to_site(points_lat[i], points_lng[i]))
        csv_data.append(tmp)
    header = ["景點", "最近觀測站", "距離(km)"]
    pd.DataFrame(csv_data).to_csv('output/site_distance.csv', header=header, index=0)

    print("檔案 site_distance.csv 已創建")


def __get_distance_point_to_site(point_lat, point_lng):
    sites = pd.read_csv('static/觀測站.csv')
    sites_name = sites['站名'].tolist()
    sites_lat = sites['經度'].tolist()
    sites_lng = sites['緯度'].tolist()

    tmp_for_search_name = {}
    tmp_distance = []
    for i, site_name in enumerate(sites_name):
        distance = __compute_distance(point_lat, point_lng, sites_lat[i], sites_lng[i])
        tmp_for_search_name[distance] = site_name
        tmp_distance.append(distance)
    nearest_site_distance = np.min(tmp_distance)
    nearest_site_name = tmp_for_search_name[nearest_site_distance]

    return [nearest_site_name, round(nearest_site_distance, 3)]


"""
傳入兩點的座標得到距離
得到的距離單位為公里km
"""


def __compute_distance(lat1, lng1, lat2, lng2):
    radlat1 = radians(lat1)
    radlat2 = radians(lat2)
    a = radlat1 - radlat2
    b = radians(lng1) - radians(lng2)
    s = 2 * asin(sqrt(pow(sin(a / 2), 2) + cos(radlat1) * cos(radlat2) * pow(sin(b / 2), 2)))
    earth_radius = 6378.137
    s = s * earth_radius
    if s < 0:
        return -s
    else:
        return s
