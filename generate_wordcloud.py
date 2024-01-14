from config import *

from wordcloud import WordCloud
import pandas as pd
import jieba
import re
from collections import Counter
import matplotlib.pyplot as plt
import os
import time
from enum import Enum


IGNORE_HEADERS = ['<?xml version="1.0"?>', '<msg>']


class SendPrefix(Enum):
    together = -1
    received = 0
    sent = 1


def get_wordcloud(data_path, save_dir, is_send=SendPrefix.together, talker=''):
    """
    :param data_path: 聊天记录文件excel
    :param is_send:
    :param save_dir: 词云保存文件夹
    :param talker: 对话人微信号
    :return:
    """

    save_path = os.path.join(save_dir, f'{SendPrefix(is_send).name}_{int(time.time())}.png')
    df = pd.read_excel(data_path)
    if is_send != SendPrefix.together:
        df = df[df.isSend == is_send]
    if talker:
        df = df[df.talker == talker]

    texts = df['content'].to_list()

    with open('data/CNstopwords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        stopwords = [line.strip().replace("\ufeff", "") for line in lines]

    # 分词，去除停用词和表情（表情都是这样的格式：[xx]）
    norm_texts = []
    pattern = re.compile('(\[.+?\])')
    for text in texts:
        if not isinstance(text, str):
            text = str(text)
        ignore = False

        # wechat system msg
        if text.count(':') >= 5:
            continue
        if re.search(':[0-9]+:[0-9]+:?$', text):
            continue

        for ignore_header in IGNORE_HEADERS:
            if text.startswith(ignore_header):
                ignore = True
                break
        if ignore:
            continue
        text = pattern.sub('', text).replace('\n', '')  # 删除表情、换行符
        words = jieba.lcut(text)
        res = [word for word in words if word not in stopwords and word.replace(' ', '') != '' and len(word) > 1]
        if res:
            norm_texts.extend(res)

    count_dict = dict(Counter(norm_texts))
    wc = WordCloud(font_path='data/simhei.ttf', background_color='white', include_numbers=False,
                   random_state=0, width=1600, height=800)  # 如果不指定中文字体路径，词云会乱码
    wc = wc.fit_words(count_dict)
    plt.imshow(wc)
    plt.show()
    wc.to_file(save_path)


if __name__ == '__main__':
    # 示例：绘制 对方 发送的信息的词云图
    get_wordcloud(MSG_XLSX_PATH, save_dir=SAVE_DIR, is_send=SendPrefix.together, talker=TALKER)
