from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


strChineseFont='msj.ttf'
myFont=FontProperties(fname=strChineseFont)

def compute_model(ylist, sdate, mktret):
    xlist = []
    mktret = mktret.set_index('MDATE')
    for i in range(0, len(sdate)):
        xlist.append(mktret.loc[sdate[i], 'ROI'])
    if len(xlist) != len(ylist):
        raise Exception("Data lenght Error!")
    return simple_reg(xlist, ylist)


def simple_reg(xlist, ylist):
    df = pd.DataFrame({'X': xlist, 'y': ylist})
    n = np.size(xlist)

    xmean = np.mean(xlist)
    ymean = np.mean(ylist)

    df['xycov'] = (df['X'] - xmean) * (df['y'] - ymean)
    df['xvar'] = (df['X'] - xmean) ** 2
    df['yvar'] = (df['y'] - ymean) ** 2

    # Calculate beta, alpha, s, R2
    beta = df['xycov'].sum() / df['xvar'].sum()
    alpha = ymean - (beta * xmean)
    df['e2'] = df['y'] - alpha - beta * df['X']
    e2 = (df['e2'] ** 2).sum()
    s = np.sqrt(e2 / (n - 2))
    R2 = 1 - e2 / df['yvar'].sum()
    return [alpha, beta, s, R2]



def compute_and_plot(df_stk, df_mkt,year):
    # get list of stock names
    stock_COID = df_stk['COID'].unique()
    stock_COID = list(stock_COID)

    df_stk = df_stk.groupby('COID', axis=0)

    # apply `compute_model` on each stock
    stock_names = []
    alphalist = []
    betalist = []

    for COID in stock_COID:
        cur_data = df_stk.get_group(COID)

        if len(cur_data['COID'].unique()) == 1:
            stock_names.append(cur_data.iloc[0, 1])
            cur_COID = cur_data.iloc[0, 0]
            cur_name = cur_data.iloc[0, 1]
            sret = cur_data['ROI']
            sret = list(sret)
            sdate = cur_data['MDATE']
            sdate = list(sdate)
            (alpha, beta, slist, r2list) = compute_model(sret, sdate, df_mkt)
            alphalist.append(alpha)
            betalist.append(beta)
        else:
            print("More than 1 stock exists in cur_data. Process halts.")
            break

    # plot
    fig, ax = plt.subplots(figsize=(15, 12))
    xlower, xupper, ylower, yupper = -1, 3, -1, 2.5
    ax.scatter(betalist, alphalist)


    for i, stock_name in enumerate(stock_names):
        if xlower < betalist[i] < xupper and ylower < alphalist[i] < yupper:
            ax.set_title('Result' + str(year))
            ax.annotate(stock_name, (betalist[i], alphalist[i]),fontproperties=myFont)
            ax.set_xbound(xlower, xupper)
            ax.set_ybound(ylower, yupper)
            ax.set_xlabel('beta')
            ax.set_ylabel('alpha')
    plt.show()


stock = pd.read_csv('stock.csv', sep=",", header=0, encoding='cp950')
market = pd.read_csv('market.csv', sep=",", header=0, encoding='cp950')


def split_to_year(df):
    df["date_dt"] = pd.to_datetime(df["MDATE"], format="%Y%m%d")
    df["year"] = pd.DatetimeIndex(df["date_dt"]).year
    df_g = df.groupby(["year"])
    for name, group in df_g:
        if name == 2017:
            df_17 = group
        elif name == 2018:
            df_18 = group
        elif name == 2019:
            df_19 = group
        elif name == 2020:
            df_20 = group

    return df_17, df_18, df_19, df_20

stock17,stock18,stock19,stock20 = split_to_year(stock)
market17,market18,market19,market20 = split_to_year(market)


compute_and_plot(stock17, market17,2017)
compute_and_plot(stock18, market18,2018)
compute_and_plot(stock19, market19,2019)
compute_and_plot(stock20, market20,2020)


"""
temperatures = np.array([29, 28, 34, 31, 25, 29, 32, 31, 24, 33, 25, 31, 26, 30])
iced_tea_sales = np.array([77, 62, 93, 84, 59, 64, 80, 75, 58, 91, 51, 73, 65, 84])

lm = LinearRegression()
lm.fit(np.reshape(temperatures, (len(temperatures), 1)), np.reshape(iced_tea_sales, (len(iced_tea_sales), 1)))


to_be_predicted = np.array([30])
predicted_sales = lm.predict(np.reshape(to_be_predicted, (len(to_be_predicted), 1)))

print(predicted_sales)

"""
