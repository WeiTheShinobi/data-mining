# 河內塔 遞迴解

def hanoi(n, A, B, C):
    if n == 1:
        print(f"{A}->{C}")
    else:
        hanoi(n-1, A, C, B)
        hanoi(1, A, B, C)
        hanoi(n-1, B, A, C)

if __name__ == '__main__':
    n = int(input())
    hanoi(int(n), 'A', 'B', 'C')