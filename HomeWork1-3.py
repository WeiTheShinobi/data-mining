# 設定一個合法的密碼
# 使用鍵值對搜尋

def puncChecker(pswdInput):
    punc = "!”#$%&’()*+,-./:;<=>?@[\]^_|̀{}"
    puncDict = {}
    for i in punc:
        puncDict[i] = i
    for i in pswdInput:
        if i == puncDict.get(i):
            return True
    return False


def numberChecker(pswdInput):
    number = "0123456789"
    numberDict = {}
    for i in number:
        numberDict[i] = i
    for i in pswdInput:
        if i == numberDict.get(i):
            return True
    return False


def lowerEngChecker(pswdInput):
    lowerEng = "abcdefghijklmnopqrstuvwxyz"
    lowerEngDict = {}
    for i in lowerEng:
        lowerEngDict[i] = i
    for i in pswdInput:
        if i == lowerEngDict.get(i):
            return True
    return False


def upperEngChecker(pswdInput):
    upperEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    upperEngDict = {}
    for i in upperEng:
        upperEngDict[i] = i
    for i in pswdInput:
        if i == upperEngDict.get(i):
            return True
    return False


def passwordChecker(pswdInput):
    if len(pswdInput) < 7:
        return False

    if len(pswdInput) > 12:
        return False

    # 以下四個方法使用鍵值對搜尋，如果密碼有需要的數值就可以通過驗證。
    if not upperEngChecker(pswdInput):
        return False

    if not lowerEngChecker(pswdInput):
        return False

    if not puncChecker(pswdInput):
        return False

    if not numberChecker(pswdInput):
        return False

    return True


def setPassword():
    pswd = ""

    while(pswd == ""):
        # 輸入流程
        pswdInput = str(input("請設定密碼（密碼必須是 7 到 12 個字元，必須包含大寫英文字母、"
                             "小寫英文字母、數字、特殊符號），或者直接按下 Enter 跳出："))

        # 驗證密碼是否符合條件
        if not passwordChecker(pswdInput):
            continue

        # 驗證密碼流程
        pswdInputAgain = str(input("請再輸入剛才設定的密碼： "))

        if pswdInput == pswdInputAgain:
            print("密碼設定完成。")
            pswd = pswdInput
        else:
            print("兩次輸入不一致，請重新設定密碼。")


if __name__ == '__main__':
    setPassword()