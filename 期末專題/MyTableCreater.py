import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties


def create_one_tourist_table_or_all():
    file = pd.read_csv('static/遊客人數/2019/10801.csv')
    areas = file['觀光遊憩區別'].to_dict()

    for i, _ in enumerate(areas):
        print(i, end=" ")
        print(areas[i])

    number = int(input("輸入你想查看的地區（不輸入則為全部）： "))
    __create_tourist_table(number)


def __create_tourist_table(number=None):
    file_directory_path = "static/遊客人數/"
    years = ['2018', '2019', '2020', '2021']

    file = pd.read_csv('static/遊客人數/2019/10801.csv')
    areas = file['觀光遊憩區別'].tolist()

    if number is not None:
        areas = [areas[number]]

    for year in years:
        file_list = os.listdir(file_directory_path + year)
        file_nums = len(file_list)

        for area in areas:
            tourist_count_ticket = []
            tourist_count = []

            for file_name in file_list:
                file = pd.read_csv(file_directory_path + year + '/' + file_name)
                file = file[file['觀光遊憩區別'] == area]
                try:
                    tourist_count_ticket.append(int(file['遊客人次有門票_需購票'].values[0].replace(',', '')))
                except:
                    tourist_count_ticket.append(0)
                try:
                    tourist_count.append(int(file['遊客人次無門票_免費'].values[0].replace(',', '')))
                except:
                    tourist_count.append(0)

            __draw_table(tourist_count, tourist_count_ticket, area, year, file_nums)


def __draw_table(tourist_count, tourist_count_ticket, area, year, file_nums):
    strChineseFont = 'msj.ttf'
    myFont = FontProperties(fname=strChineseFont)

    mouth = np.arange(1, file_nums + 1)
    y = np.arange(1, len(mouth) + 1)
    width = 0.3
    plt.bar(y, tourist_count, label="Free", width=width)
    plt.bar(y + width, tourist_count_ticket, label="Ticket", width=width)

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.7))
    plt.xticks(y, mouth)
    plt.xlabel("月份", fontproperties=myFont)
    plt.ylabel("遊客數", fontproperties=myFont)
    plt.title(year + " " + area, fontproperties=myFont)
    plt.savefig('output/遊客/' + area + "_" + year)
    plt.show()
