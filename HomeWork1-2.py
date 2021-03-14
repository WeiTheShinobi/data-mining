# 河內塔 遞迴解

def hanoi(n, A, B, C):
    if n == 1:
        print(f"{n} 號圓盤： ", end="")
        print(f"{A}->{C}")
    else:
        hanoi(n-1, A, C, B)
        print(f"{n} 號圓盤： ", end="")
        print(A+"->"+C)
        hanoi(n-1, B, A, C)

if __name__ == '__main__':
    n = int(input("請輸入數字： "))
    hanoi(n, 'A', 'B', 'C')