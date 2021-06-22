import pandas as pd
import json

data = pd.read_csv('static/景點.csv')
point_intro = pd.read_csv('static/景點統整.csv')
position = data['地點']


def get_HTML():
    for i in range(len(position)):
        print("<button onclick=\"getTouristData(this.value)\" title=" + position[i] + " id=" + position[i] + " value=" +
              position[i] + " class=tourist><i class=\"map marker alternate icon\"></i></button>")


def get_point_css():
    for i in range(len(position)):
        print("#" + position[i] + " {")
        print("    left: " + str(i) + "%;")
        print("    top: " + str(i) + "%;")
        print("}")
        print()


def get_point_intro():
    intro_dict = {}
    for i, intro in enumerate(point_intro['介紹']):
        intro_dict[point_intro['名稱'][i]] = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + intro
    print(intro_dict)


def get_lat_and_log():
    latlog_dict = {}
    for i, point in enumerate(point_intro['名稱']):
        latlog = [point_intro['緯度'][i], point_intro['經度'][i]]
        latlog_dict[point] = latlog
    print(latlog_dict)


def get_type():
    for i, point in enumerate(point_intro['名稱']):
        print("touristType[\"" + point + "\"] = ", end="")
        print("\"", end="")
        for j in point_intro['類別'][i].split('、'):
            print("<div class=\\\"ui basic teal label\\\">", end="")
            print(j, end="")
            print("</div>", end="")
        print("\"", end="")
        print()


if __name__ == '__main__':
    get_type()