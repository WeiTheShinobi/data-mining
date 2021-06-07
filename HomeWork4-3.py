import pandas as pd
import numpy as np


# 下面函式：轉換成績
def compute_std_and_mean(data):
    return np.std(data, ddof=1), np.mean(data)


def compute_t_score(origin_score, std_and_mean):
    return (10 * ((origin_score - std_and_mean[1]) / std_and_mean[0])) + 50


def convert_to_t_score(data):
    return list(map(lambda x: round(compute_t_score(x, compute_std_and_mean(data)), 2), data))


def convert_many_to_t_score(data, headers_need_convert):
    for i in headers_need_convert:
        data[i] = convert_to_t_score(data[i])
    return data


# 下面函式：考生排名
def compute_total_t_score(data, headers_to_compute):
    data = data.reset_index(drop=True)
    total_score = []
    for i, _ in enumerate(data.index):
        tmp = 0
        for j in headers_to_compute:
            tmp += data[j][i]
        total_score.append(tmp)

    data = data.drop(columns=headers_to_compute)
    data['成績'] = total_score
    return data


#  處理同樣分數需要同名次問題
def compute_rank(data):
    rank = []
    data = list(map(lambda x: int(x * 100), data))
    for i in range(len(data)):
        if i != 0:
            if data[i] == data[i - 1]:
                rank.append(i - 1)
                continue
        rank.append(i)

    return list(map(lambda x: x + 1, rank))


if __name__ == '__main__':
    groupA = pd.read_excel('prob2_files/A組.xlsx')
    groupB = pd.read_excel('prob2_files/B組.xlsx')
    groupC = pd.read_excel('prob2_files/C組.xlsx')

    # 換算成T分數
    headers_convert = ['評分一', '評分二', '評分三']

    groupA_new = convert_many_to_t_score(groupA, headers_convert)
    groupB_new = convert_many_to_t_score(groupB, headers_convert)
    groupC_new = convert_many_to_t_score(groupC, headers_convert)

    groupA_new.to_excel('prob2_files/A組new.xlsx', index=0)
    groupB_new.to_excel('prob2_files/B組new.xlsx', index=0)
    groupC_new.to_excel('prob2_files/C組new.xlsx', index=0)
    print("轉換分數的檔案已生成")

    # 考生排名
    all_data = groupA_new.append(groupB_new).append(groupC_new)

    all_data = compute_total_t_score(all_data, headers_convert)
    all_data = all_data.sort_values(['成績', '組別'], ascending=False)

    all_data['名次'] = compute_rank(all_data['成績'])

    headers = ['考生組別', '組內順序', '成績', '名次']
    all_data.to_excel('prob2_files/成績排序.xlsx', index=0, header=headers)
    print("檔案 成績排序.xlsx 已生成")

"""
加分項：
觀點1:
此假設認同,由中央極限定理解,不論母體分配為何,只要樣本為隨機樣本,且樣本數n夠大的情況下,由樣本線性下統計量的抽樣分配會逼近於常態分配。

觀點2:
由問題三中(ii)可得知每組學生為隨機樣本
每位學生分組都是獨立的,不會互相影響,因此我們認為每組同學為相同分配。

"""
