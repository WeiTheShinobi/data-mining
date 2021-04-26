from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

"""
y指數
x個股

回歸每天的


"""

def simple_reg(xlist, ylist):
    xlist = np.reshape(xlist, (len(xlist), 1))
    ylist = np.reshape(ylist, (len(ylist), 1))
    lr = LinearRegression()
    lr.fit(xlist, ylist)
    plt.scatter(xlist, ylist)
    plt.show()
    # print(lr)
    # return [alpha, beta, s, r2]


# xlist = [0.4825, 1.0491, 1.7312, 0.5337, 1.3371, 0.2564, 0.7229, 1.0445, 0.2471]
# ylist = [0.9560, 1.3258, 4.9904, 1.2797, 3.7037, 0.3846, 2.4904, 0.0000, 0.5607]

# simple_reg(xlist, ylist)

xlist = np.array([29, 28, 34, 31, 25, 29])
ylist = np.array([77, 62, 93, 84, 59, 64])
xlist = np.reshape(xlist, (len(xlist), 1))
ylist = np.reshape(ylist, (len(ylist), 1))

simple_reg(xlist, ylist)


"""
temperatures = np.array([29, 28, 34, 31, 25, 29, 32, 31, 24, 33, 25, 31, 26, 30])
iced_tea_sales = np.array([77, 62, 93, 84, 59, 64, 80, 75, 58, 91, 51, 73, 65, 84])

lm = LinearRegression()
lm.fit(np.reshape(temperatures, (len(temperatures), 1)), np.reshape(iced_tea_sales, (len(iced_tea_sales), 1)))

# 新的氣溫
to_be_predicted = np.array([30])
predicted_sales = lm.predict(np.reshape(to_be_predicted, (len(to_be_predicted), 1)))

# 預測的冰紅茶銷量
print(predicted_sales)

"""

# [0.33336979748359297,0.016504474005063087,2.6334217234108612, 3.363998221928011e-05]
