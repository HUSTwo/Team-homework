# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 23:34:29 2020

@author: U201812776
"""

"""将数据从.scv文件中读取出来"""

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

"""将数据进行可视化处理"""

from matplotlib import pyplot as plt
import seaborn as sns

# 折线图：股票走势
plt.plot(raw_time, df['close'])
plt.xlabel('Time')
plt.ylabel('Share Price')
plt.title('Trend')
plt.show()

# 散点图：成交量和股价

plt.scatter(df['volume'], df['close'])
plt.xlabel('Volume')
plt.ylabel('Share Price')
plt.title('Volume & Share Price')
plt.show()

#切片取前300组数据
plt.scatter(df['volume'][:300], df['close'][:300]) 
plt.xlabel('Volume')
plt.ylabel('Share Price')
plt.title('Volume & Share Price')
plt.show()

# 涨跌幅度
daily_return = df['close'][0::240].pct_change().dropna()
plt.plot(raw_time[0::240][:40], daily_return[:40])
plt.xlabel('Time')
plt.ylabel('Rise and Fall')
plt.show()

# 直方图
plt.hist(daily_return)

# 核密度估计
sns.kdeplot(daily_return)

# 相关系数矩阵
correlation = df.corr()
print(correlation)

sns.heatmap(correlation, annot=True)







