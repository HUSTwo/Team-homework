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


# 注意：tushare需要注册方可使用，注册后初始积分100分，完善个人信息后共120分，才能使用daily()这个api。
# 尽管tushare的绝大多数api我们都没有使用权限，但daily()和cctv_news()应当可以满足本次训练营的使用。
# 初次使用需要初始化一次
"""token码有待更新"""

import tushare as ts

token = 'c3a77cb99733084fb6d9bfd7a7fb416b2155b7bdade46c78e752e730'  # 我自己注册的token，大家最好还是自己注册一个，数据调用有上限
ts.set_token(token)  # 初始化，之后就不需要了

pro = ts.pro_api()

df = pro.daily(ts_code='000001.SZ, 000002.SZ, 000004.SZ, 000005.SZ, 000006.SZ', start_date='20200201', end_date='20200601') #  000003.SZ已经退市
df.head(10)

#对几只股票的时间和序号进行分类
sz1 = df[::5].set_index('trade_date')
sz2 = df[1::5].set_index('trade_date')
sz4 = df[2::5].set_index('trade_date')
sz5 = df[3::5].set_index('trade_date')
sz6 = df[4::5].set_index('trade_date')

sz1.head()

#把股票都分出来后开始画图
fig, ax = plt.subplots()

sz1.plot(ax=ax, y='close', label='000001')
sz2.plot(ax=ax, y='close', label='000002')
sz4.plot(ax=ax, y='close', label='000004')
sz5.plot(ax=ax, y='close', label='000005')
sz6.plot(ax=ax, y='close', label='000006')

plt.legend(loc='upper left')

#绘制柱状图查看平均股价
mean_share_list = [sz1['close'].mean(), sz2['close'].mean(), sz4['close'].mean(), sz5['close'].mean(), sz6['close'].mean()]
mean_share_series = pd.Series(mean_share_list, index=['000001', '000002', '000004', '000005', '000006'])
mean_share_series.plot(kind='bar')
plt.xticks(rotation=360)  # 这里如果不加rotation默认是90°

#绘制箱型图分析数据
closedf = pd.DataFrame()
closedf = pd.concat([closedf, sz1['close'], sz2['close'], sz4['close'], sz5['close'], sz6['close']], axis=1)  # 横向拼接数据(axis=1)
closedf.columns = ['000001', '000002', '000004', '000005', '000006']
closedf.plot(kind='box')

#使用describe()方法对数据均值、分位数、标准差、最值进行初步分析
sz4.describe()


