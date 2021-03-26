# 作業五
import os


def articleLoader(article):
    f1r = open("input_files/" + article, mode='r', encoding='utf-8')
    article = f1r.read()
    f1r.close()
    return article


# 算出文章中文數
# 總長 - 空格 - 換行 - 符號 = 中文數
def chineseCounter(article, func):
    funcDict = {}
    for i in func:
        funcDict[i] = i

    count = 0
    for i in article:
        if i == " ":
            count += 1
        if i == "\n":
            count += 1
        if i == funcDict.get(i):
            count += 1

    return len(article) - count


# 找出檔案的標點符號
def funcCounter(article):
    func = "，。、？！：；"
    wordDict = {}
    count = 0

    for i in func:
        wordDict[i] = i

    for i in range(len(article)):
        # 刪節號額外處理
        if article[i] == "…" and i+1 < len(article):
            if article[i+1] == "…":
                count += 1
        elif article[i] == wordDict.get(article[i]):
            count += 1

    return count


if __name__ == '__main__':
    articleList = os.listdir("input_files")

    # 將文章列表一一讀取
    for title in articleList:
        article = articleLoader(title)

        # 為了將兩個刪節號視為一個標點符號。
        func = "，。、？！：；…"

        articleChineseCount = chineseCounter(article, func)
        articleFuncCount = funcCounter(article)

        articleAvgSentence = articleChineseCount / articleFuncCount

        articleChineseCount = str(articleChineseCount)
        articleAvgSentence = str(round(articleAvgSentence, 1))

        print("輸出" + title + " 的中文字數統計是 " + articleChineseCount + "，平均句長是 " + articleAvgSentence + " 字")
