# 驗證密碼

def login():
    try:
        f1r = open("password.txt", mode='r', encoding='utf-8')
        password = f1r.read()
        f1r.close()
    except:
        print("請先設定密碼。")
        exit()

    count = 0
    while count < 4:
        pswdInput = str(input("奉召前來，你是我的 Master 嗎？請下指令："))
        if pswdInput == password:
            print("吾劍將隨汝同在，汝之命運將與吾共存，於此，契約完成。")
            break
        elif count < 3:
            print("指令無效，請重下指令：")
            count += 1
        else:
            count += 1
    if count == 4:
        print("指令多次無效， 你已經被 Saber 清除！ ")

if __name__ == '__main__':
    login()