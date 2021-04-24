import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""

Problem 3. 各題作答狀況查詢系統
承上題檔案。我們將製作資料查詢系統：輸入起始與結束時間，系統會統計這段時間各題上傳結果。
首先，系統將結果顯示為 6×5 的報表，首欄依序填入 Problem Status 和五種答題狀況：Accepted, Compile
Error, Runtime Error, Time Limit Exceed 與 Wrong Answer，第一列最左邊是 Problem Status，其餘依序
為 Problem 1 到 Problem 4。報表其他部分則填入對應的上傳結果的次數，例如第三欄、第四列的表格所填
數字為：查詢的起始時間到結束時間內，Problem 2 對應到的 Runtime Error 次數。
其次，由於資料視覺化正當紅，系統必須另外印出一張「並列長條圖」。6圖形標題顯示查詢的時間區段。
輸入輸出格式
輸入格式必須與下方程式碼有相同的效果：
time_start = input(' 查詢起始時間（格式為 hh:mm:ss）: ')
time_end = input(' 查詢結束時間（格式為 hh:mm:ss）: ')
輸出的表格可以參考這段程式碼，7而印出的圖形則必須類似本頁上圖。
"""

file = pd.read_csv('midterm2.csv')

tmp = {'Accepted': [], 'Compile Error': [], 'Runtime Error': [], 'Time Limit Exceed': [], 'Wrong Answer': []}

for i in range(1, 5):
    file2 = file[file['Problem'] == i].groupby('Status')
    for Name, Problem in file2:
        tmp[Name].append(len(Problem))
    for v in tmp.values():
        if len(v) < i:
            v.append(0)

prob = ["Problem 1", "Problem 2", "Problem 3", "Problem 4"]
y = np.arange(1, len(prob) + 1)

plt.bar(y - 0.2, tmp['Accepted'], label="Accepted", width=0.1)
plt.bar(y - 0.1, tmp['Compile Error'], label="Compile Error", width=0.1)
plt.bar(y, tmp['Runtime Error'], label="Runtime Error", width=0.1)
plt.bar(y + 0.1, tmp['Time Limit Exceed'], label="Time Limit Exceed", width=0.1)
plt.bar(y + 0.2, tmp['Wrong Answer'], label="Wrong Answer", width=0.1)

# for k in tmp:
#     plt.bar(y, tmp[k], label=k, width=0.2)


plt.legend(loc='BestOutside')
plt.ylabel('Frequencies')
plt.xticks(y, prob)
plt.show()

print(tmp)
print()
