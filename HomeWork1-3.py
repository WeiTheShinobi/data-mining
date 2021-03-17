# 設定一個合法的密碼 以及 登入 （與第四題合併）

# 驗證器
# 使用鍵值對來進行驗證
# 密碼當鍵檢查
# 檢查到就回傳true 反之
def wordChecker(pswdInput,checkword):
    wordDict = {}
    for i in checkword:
        wordDict[i] = i
    for i in pswdInput:
        if i == wordDict.get(i):
            return True
    return False

# 驗證密碼的數字英文和特殊符號
def passwordChecker(pswdInput):
    if len(pswdInput) < 7:
        return False

    if len(pswdInput) > 12:
        return False

    upperEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowerEng = "abcdefghijklmnopqrstuvwxyz"
    number = "0123456789"
    punc = "!”#$%&’()*+,-./:;<=>?@[\]^_|̀{}"

    # 呼叫驗證器傳入要驗證的參數
    if not wordChecker(pswdInput,upperEng):
        return False

    if not wordChecker(pswdInput,lowerEng):
        return False

    if not wordChecker(pswdInput,number):
        return False

    if not wordChecker(pswdInput,punc):
        return False

    return True

# 設定密碼
def setPassword():
    pswd = ""

    while(pswd == ""):
        # 輸入流程
        pswdInput = str(input("請設定密碼（密碼必須是 7 到 12 個字元，必須包含大寫英文字母、"
                             "小寫英文字母、數字、特殊符號），或者直接按下 Enter 跳出："))

        # 按下Enter退出
        if pswdInput == "":
            exit()

        # 驗證密碼是否符合條件
        if not passwordChecker(pswdInput):
            print("請符合密碼設定格式。")
            continue

        # 確認密碼
        pswdInputAgain = str(input("請再輸入剛才設定的密碼： "))

        if pswdInput == pswdInputAgain:
            print("密碼設定完成。")
            pswd = pswdInput
            f1w = open("password.txt", mode='w', encoding='utf-8')
            f1w.write(pswd)
            f1w.close()
            return pswd
        else:
            print("兩次輸入不一致，請重新設定密碼。")

# 登入的環節
def loginChecker(password):
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


def login():
    # 讀取密碼檔案，如果失敗進入設定密碼
    try:
        f1r = open("password.txt", mode='r', encoding='utf-8')
        password = f1r.read()
        f1r.close()
    except:
        # 設定密碼
        password = setPassword()

    # 登入驗證
    loginChecker(password)


if __name__ == '__main__':
    login()