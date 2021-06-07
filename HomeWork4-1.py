import jieba
import re
import csv
from wordcloud import WordCloud as wc
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from PIL import Image

strChineseFont = 'file4-1/msj.ttf'
jieba.set_dictionary('file4-1/dict.txt.big.txt')
singers = ['五月天', '方大同', '林夕', '李宗盛']

with open('file4-1/stopwords.txt', 'r', encoding='UTF-8') as f:
    stopWords = [word.strip() for word in f.readlines()]
stopWords += [' ', '\t', '\n']

with open('file4-1/myStopWords.txt', 'r', encoding='UTF-8') as f:
    stopWords += [word.strip() for word in f.readlines()]

for singer in singers:
    lyrics = open("file4-1/" + singer + ".txt", "r", encoding='UTF-8').read()

    news_no_number = re.sub('[0-9]', '', lyrics)
    seg_list_0 = jieba.cut(news_no_number)

    remainderWords = list(filter(lambda a: a not in stopWords, seg_list_0))
    seg_dict = Counter(remainderWords)
    seg_list = sorted(seg_dict.items(), key=lambda item: item[1], reverse=True)

    # 產生文字檔
    with open('file4-1/' + singer + '文字.txt', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(seg_list)

    mask = np.array(Image.open("file4-1/duck.png"))
    result = wc(background_color='white', mask=mask, font_path=strChineseFont, width=2000, height=2000)
    result.generate_from_frequencies(frequencies=seg_dict)

    plt.figure(figsize=(10, 5), facecolor='k')
    plt.imshow(result, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

    result.to_file('file4-1/output/' + singer + '.png')
