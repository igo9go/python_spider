# 引入所需要的包
import os
import jieba
import pandas as pd
import numpy as np
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

# 定义文件路径
dir = "/Users/zhouqiang/PycharmProjects/spider_demo/bilibili弹幕"
# 定义语料文件路径
file = os.path.join("bibi.csv")
# 定义停用词文件路径
stop_words = os.path.join("stopwords.txt")
# 定义wordcloud中字体文件的路径
simhei = os.path.join("simhei.ttf")
# 读取语料
df = pd.read_csv(file, encoding='utf-8')
df.head()
# 如果存在nan，删除
df.dropna(inplace=True)
# 将content一列转为list
content = df.contents.values.tolist()
# 用jieba进行分词操作
segment = []
for line in content:
    try:
        segs = jieba.cut_for_search(line)
        segs = [v for v in segs if not str(v).isdigit()]  # 去数字
        segs = list(filter(lambda x: x.strip(), segs))  # 去左右空格
        # segs = list(filter(lambda x:len(x)>1, segs)) #长度为1的字符
        for seg in segs:
            if len(seg) > 1 and seg != '\r\n':
                segment.append(seg)
    except:
        print(line)
        continue
# 分词后加入一个新的DataFrame
words_df = pd.DataFrame({'segment': segment})
# 加载停用词
stopwords = pd.read_csv(stop_words, index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='utf-8')
# 安装关键字groupby分组统计词频，并按照计数降序排序

#words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": np.size})

words_stat = words_df.groupby(by=['segment'])['segment'].agg(np.size)
words_stat = words_stat.to_frame()
words_stat.columns = ['计数']

words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
# 分组之后去掉停用词
words_stat = words_stat[~words_stat.segment.isin(stopwords.stopword)]

# 第一种是默认的样式
wordcloud = WordCloud(font_path=simhei, background_color="white", max_font_size=80)
word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
wordcloud = wordcloud.fit_words(word_frequence)
plt.imshow(wordcloud)
plt.show()
wordcloud.to_file(r'wordcloud_1.jpg')  # 保存结果

print(words_stat.head(10).segment.values.tolist())

#第二种是自定义图片
text = " ".join(words_stat['segment'].head(100).astype(str))
abel_mask = imread(r"year2019.jpg")  #这里设置了一张自定义图片
wordcloud2 = WordCloud(background_color='white',  # 设置背景颜色
                     mask = abel_mask,  # 设置背景图片
                     max_words = 3000,  # 设置最大现实的字数
                     font_path = simhei,  # 设置字体格式
                     width=2048,
                     height=1024,
                     scale=4.0,
                     max_font_size= 300,  # 字体最大值
                     random_state=42).generate(text)

# 根据图片生成词云颜色
image_colors = ImageColorGenerator(abel_mask)
wordcloud2.recolor(color_func=image_colors)
# 以下代码显示图片
plt.imshow(wordcloud2)
#plt.axis("off")
plt.show()
wordcloud2.to_file(r'wordcloud_2.jpg') #保存结果