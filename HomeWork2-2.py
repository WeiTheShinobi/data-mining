import pandas as pd

file = pd.read_csv('midterm2.csv')

# （1）全體學生編號應是 0 到 117 號，但有些不在上傳紀錄中。假設這些學生退選，請回報退選的學生編號。
studentID = file["StudentID"].to_dict()
Drop_ID = {}
for i in range(118):
    if i not in studentID.values():
        Drop_ID[i] = None

# （2）有參加考試的學生各得多少分？若某生在某題曾數次上傳，則他在此題的得分記為最後上傳的一次。

Student_Score = {}
for i in range(1, 5):
    file2 = file[file['Problem'] == i] \
        .groupby('StudentID') \
        .Score
    for Name, Score in file2:
        Score = Score.max()
        if Student_Score.get(Name) is not None:
            Score += Student_Score.get(Name)
        Student_Score[Name] = Score

# （3）各題被接受（Accepted）次數。注意：有的學生就算某題被接受，仍會重新上傳，這不能重複計算！3

Prob_Accept = {}
for i in range(1, 5):
    file3 = file[(file['Status'] == 'Accepted') &
                 (file['Problem'] == i)]
    file3_dict = file3.to_dict()

    no_dup_file3 = {}
    for j in file3_dict['StudentID'].values():
        no_dup_file3[j] = None
    Prob_Accept[i] = len(no_dup_file3)

# （4）各題得分率，以百分比（四捨五入到小數第一位）表示。已知各題配分依序為 30、40、30、30 分。4假如
# 有 100 位學生參加考試（有上傳紀錄），在第一題共拿 2700 分，則第一題得分率是 2700/(30*100)=90.0%。

Prob_Score_Percentage = {}
students = 118 - len(Drop_ID)
total_score = [students * 30, students * 40, students * 30, students * 30]

for i in range(1, 5):
    file2 = file[file['Problem'] == i] \
        .groupby('StudentID') \
        .Score
    for Name, Score in file2:
        Score = Score.max()
        if Prob_Score_Percentage.get(i) is not None:
            Score += Prob_Score_Percentage.get(i)
        Prob_Score_Percentage[i] = Score
for i in range(4):
    Prob_Score_Percentage[i + 1] = round(Prob_Score_Percentage[i + 1] / total_score[i], 2)

print(Drop_ID)
print(Student_Score)
print(Prob_Accept)
print(Prob_Score_Percentage)
