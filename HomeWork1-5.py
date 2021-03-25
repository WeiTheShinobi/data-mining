# 作業五
import os


def articleLoader(article):
    f1r = open("input_files/" + article, mode='r', encoding='utf-8')
    article = f1r.read()
    f1r.close()
    return article


# 找出檔案的標點符號
def wordChecker(article,checkword):
    wordDict = {}
    count = 0
    for i in checkword:
        wordDict[i] = i
    for i in article:
        if i == wordDict.get(i):
            count += 1
    return count


if __name__ == '__main__':
    articleList = os.listdir("input_files")

    # 將文章列表一一讀取
    for title in articleList:
        article = articleLoader(title)

        # 為了將兩個刪節號視為一個標點符號，使用list。
        checkWord = "，。、？！：；"
        checkWordList = list(checkWord)
        checkWordList.append("……")

        articleWordsAndFunc = len(article)
        articleFunc = wordChecker(article, checkWordList)

        articleWords = articleWordsAndFunc - articleFunc
        articleAvgWords = articleWords / articleFunc

        articleWords = str(articleWords)
        articleAvgWords = str(round(articleAvgWords, 1))

        print("輸出" + title + " 的中文字數統計是 " + articleWords + "，平均句長是 " + articleAvgWords + " 字")
