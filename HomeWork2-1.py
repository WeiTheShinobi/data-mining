import numpy as np

"""
我們用模擬的方式來仲裁。我們只看「蔡韓柯」這組對比民調。假設三人支持度如同民進黨中央給的
(v1, v2, v3) = (0.357, 0.245, 0.227)。1問題：三人在五個民調機構的最高最低差異皆不到 2.4% 的可能性？
首先，定義一次試驗為: 考慮參數為 (v1, v2, v3, 1− v1 − v2 − v3) 的多項分布 (multinomial distribution)，2以
此隨機抽出「出像」(outcome)，若各候選人在 5 機構各 3000 樣本獲得的最高與最低支持度差距皆 < 2.4%，
稱為此試驗結果為 True。注意：每次試驗每個機構都會得到 4 個支持率數值，但是我們不關心第 4 個數。
接著定義可能性: 進行一百萬次試驗 (想像成一百萬個平行世界線)，則可能性 = True 的次數/1000000.

模型 1：對稱考量
五項民調皆介於 (v1 −0.012, v2 −0.012, v3 −0.012) 與 (v1 + 0.012, v2 + 0.012, v3 + 0.012) 之間，可能性為何？
模型 2: 不對稱考量
放鬆考量，五項民調的上下差距不超過 2.4%，不用拘泥於以 (v1, v2, v3) 為中心，可能性為何？


numpy.random.multinomial(n, pvals, size=None)
n: 民調人數
pvals: 機率，和為1
size: 次數


ptp 最大值與最小值差
greater(a,b) a>b
all 全

 
"""



def problem1():
    pvalsUpper = (0.357 + 0.012, 0.245 + 0.012, 0.227 + 0.012)
    pvalsLower = (0.357 - 0.012, 0.245 - 0.012, 0.227 - 0.012)
    res = 0

    for i in range(1000000):
        test = np.random.multinomial(3000, (0.357, 0.245, 0.227,0), 5) / 3000
        test = test[:,:-1]
        resTest = np.all(np.all(np.greater_equal(pvalsUpper,test)) * np.all(np.greater_equal(test,pvalsLower)))
        res += resTest
    res = res / 1000000
    return res

def problem2():
    res = 0
    for i in range(1000000):
        test = np.random.multinomial(3000, (0.357, 0.245, 0.227,0), 5) / 3000
        test = test[:,:-1]
        resTest = np.all((np.ptp(test,0)) < 0.024)
        res += resTest
    res = res / 1000000
    return res

def confirm1():
    for j in range(0,1001,5):
        print("最高與最低支持度差距： " + str(j/10) + "%")
        variable = (j/1000)
        pvalsUpper = (0.357 + variable, 0.245 + variable, 0.227 + variable)
        pvalsLower = (0.357 - variable, 0.245 - variable, 0.227 - variable)
        res = 0
        for i in range(10000):
            test = np.random.multinomial(3000, (0.357, 0.245, 0.227,0), 5) / 3000
            test = test[:,:-1]
            resTest = np.all(np.all(np.greater_equal(pvalsUpper,test)) * np.all(np.greater_equal(test,pvalsLower)))
            res += resTest
        res = res / 10000
        print(res)

def confirm2():
    for j in range(0,1001,5):
        print("最高與最低支持度差距： " + str(j/10) + "%")
        res = 0
        for i in range(10000):
            test = np.random.multinomial(3000, (0.357, 0.245, 0.227,0), 5) / 3000
            test = test[:,:-1]
            resTest = np.all((np.ptp(test,0)) < (j / 1000))
            res += resTest
        res = res / 10000
        print(res)

# print(problem1())
# print(problem2())
# confirm1()
confirm2()