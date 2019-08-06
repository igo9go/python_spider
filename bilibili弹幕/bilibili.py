#!/usr/bin/env python
# -*- coding: utf-8 -*-


''''
 B 站的弹幕是在 XML 文件里，每个视频都有其对应的 cid 和 aid，我们取到 cid 中的数字放入 http://comment.bilibili.com/+cid+.xml，
 即可得到该视频对应的弹幕 XML 文件。

aid 对应的 cid 可以再网页源代码中找到 也可以通过heartbeat 请求查看到
视频地址   https://www.bilibili.com/video/av62026826/
弹幕地址   http://comment.bilibili.com/107835490.xml
https://i.loli.net/2019/08/05/cwWCVkx1lQXNfet.png
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
#
url = 'http://comment.bilibili.com/107835490.xml'
req = requests.get(url)
html = req.content
html_doc = str(html, 'utf-8')
# 解析
soup = BeautifulSoup(html_doc, 'lxml')
results = soup.find_all('d')
contents = [x.text for x in results]
# 保存结果
table_dict = {"contents": contents}
df = pd.DataFrame(table_dict)
df.to_csv('bibi.csv', encoding='utf-8')
