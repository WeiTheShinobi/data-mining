import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def myPCA(file, index):
    df = pd.read_excel("選舉/" + file)

    X = df.iloc[:, 2:index]

    scaler = StandardScaler()
    Z = scaler.fit_transform(X)

    n_components = 2
    random_state = 9527
    pca = PCA(n_components=n_components, random_state=random_state)
    L = pca.fit_transform(Z)

    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False

    PCA1 = L[:, 1]
    PCA2 = L[:, 0]

    PCA1_max = 1 / PCA1.max()
    PCA2_max = 1 / PCA2.max()

    PCA1 = list(map(lambda x: x * PCA1_max, PCA1))
    PCA2 = list(map(lambda x: x * PCA2_max, PCA2))

    plt.scatter(PCA1, PCA2)

    plt.xticks([-1.0, -0.5, -0.3, 0, 0.3, 0.5, 1])
    plt.yticks([-1.0, -0.5, -0.3, 0, 0.3, 0.5, 1])
    plt.grid()
    plt.axis([-1, 1, -1, 1])

    for i, _ in enumerate(L):
        plt.annotate(df['姓名'][i], xy=(PCA1[i], PCA2[i]), xytext=(PCA1[i] + 0.1, PCA2[i] + 0.1))
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    myPCA("台中第三選區.xlsx", 6)
    myPCA("台北第七選區.xls", 4)
    myPCA("新竹第二選區.xls", 9)
