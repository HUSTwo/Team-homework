# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 23:34:29 2020

@author: U201812776
"""

"""
将数据从.scv文件中读取出来
"""

# 导入数据分析库pandas
import pandas as pd

# 从本地导入数据，这里用的是相对路径，如果你的程序和文件不在同一个文件夹里请用绝对路径
df = pd.read_csv('lq_test.csv')
# 查看数据
df.head()

# 剔除缺失数据
df = df.dropna()
df.head()

#重置索引编码
df = df.reset_index().drop(columns='index')
df.head()

# 取出时间
raw_time = pd.to_datetime(df.pop('Unnamed: 0'), format='%Y/%m/%d %H:%M')



