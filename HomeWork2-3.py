import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable as pt
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

# 初始化
file = pd.read_csv('midterm2.csv')
problem_status = {'Accepted': [], 'Compile Error': [], 'Runtime Error': [], 'Time Limit Exceed': [], 'Wrong Answer': []}

# 時間處理
time_start = input(' 查詢起始時間（格式為 hh:mm:ss）: ')
time_end = input(' 查詢結束時間（格式為 hh:mm:ss）: ')
file['SubmissionTime'] = pd.to_datetime(file['SubmissionTime'])
file = file.set_index('SubmissionTime')
file = file.between_time(time_start, time_end)

# 資料處理
for i in range(1, 5):
    file2 = file[file['Problem'] == i].groupby('Status')
    for Name, Problem in file2:
        problem_status[Name].append(len(Problem))
    for v in problem_status.values():
        if len(v) < i:
            v.append(0)

# 繪製長條圖
prob = ["Problem 1", "Problem 2", "Problem 3", "Problem 4"]
y = np.arange(1, len(prob) + 1)
plt.bar(y - 0.2, problem_status['Accepted'], label="Accepted", width=0.1)
plt.bar(y - 0.1, problem_status['Compile Error'], label="Compile Error", width=0.1)
plt.bar(y, problem_status['Runtime Error'], label="Runtime Error", width=0.1)
plt.bar(y + 0.1, problem_status['Time Limit Exceed'], label="Time Limit Exceed", width=0.1)
plt.bar(y + 0.2, problem_status['Wrong Answer'], label="Wrong Answer", width=0.1)
plt.title("Exam Uploading Status: " + time_start + "—" + time_end)
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.7))
plt.ylabel('Frequencies')
plt.xticks(y, prob)
plt.show()

# 繪製圖表
show_table = pt()
column_names = ['Problem', 'Accepted', 'Compile Error', 'Runtime Error', 'Time Limit Exceed', 'Wrong Answer']
show_table.add_column(column_names[0], ["Problem 1", "Problem 2", "Problem 3", "Problem 4"])
for i in range(1, 6):
    show_table.add_column(column_names[i], problem_status[column_names[i]])
print(show_table)
