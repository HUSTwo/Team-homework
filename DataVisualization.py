# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 23:34:29 2020

@author: U201812776
"""


"""
数据可视化第一部分：将数据从.scv文件中读取出来
"""


# 导入数据分析库pandas
import pandas as pd

# 从本地导入测试数据文件data2.csv，该文件由tushare库编程产生，这里用的是相对路径，如果你的程序和文件不在同一个文件夹里请用绝对路径
df = pd.read_csv('data2.csv')
# 查看数据
df.head()

# 剔除缺失数据，实际上data2.csv文件中数据在产生时已经得到了处理
df = df.dropna()
df.head()

#重置索引编码
df = df.reset_index().drop(columns='index')
df.head()

# 取出时间
raw_time = pd.to_datetime(df.pop('date'), format='%Y/%m/%d %H:%M')






"""
数据可视化第二部分：将数据进行可视化处理
"""

from matplotlib import pyplot as plt
import seaborn as sns

##绘制如下曲线图和表格

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

#切片取前300组数据（实际上tushare输出只有350组数据）
plt.scatter(df['volume'][:300], df['close'][:300]) 
plt.xlabel('Volume')
plt.ylabel('Share Price')
plt.title('Volume & Share Price')
plt.show()

# 涨跌幅度
daily_return= df['close'].pct_change().dropna()
plt.plot(raw_time[1:], daily_return)   
plt.xlabel('Time')
plt.ylabel('Rise and Fall')
plt.show()

# 直方图
plt.hist(daily_return)
plt.show()

# 核密度估计
sns.kdeplot(daily_return)
plt.show()

# 相关系数矩阵
correlation = df.corr()
print(correlation)

sns.heatmap(correlation, annot=True)


# 注意：tushare需要注册方可使用，注册后初始积分100分，完善个人信息后共120分，才能使用daily()这个api。
# 尽管tushare的绝大多数api我们都没有使用权限，但daily()和cctv_news()应当可以满足本次训练营的使用。
# 初次使用需要初始化一次
"""此处token码由助教Sensei赞助"""

import tushare as ts

token = 'c3a77cb99733084fb6d9bfd7a7fb416b2155b7bdade46c78e752e730'  # token码
ts.set_token(token)  # 初始化，只需要使用一次

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






"""
数据可视化处理第三部分：进阶处理-绘制K线图
"""
# 导入必要库
import pandas as pd  # 数据处理
import datetime  # 时间格式处理
from matplotlib.pylab import date2num  # 时间格式处理
from matplotlib import pyplot as plt  # 绘图
from mplfinance.original_flavor import candlestick_ochl  # 绘制k线图
from matplotlib import ticker as mticker  # 刻度处理
from matplotlib import dates as mdates  # 时间格式处理

data = pd.read_csv('data2.csv')
data = data.dropna().reset_index().drop(columns='index')
raw_time = data.pop('date')

#把日期和时间分割开来，把时间格式改成方便比较的格式
date_times = []
dates = []
times = []
date_time_format = '%Y-%m-%d %H:%M:%S'  # 原str中的日期-时间格式
date_format = '%Y-%m-%d'  # 待转日期格式
time_format = '%H:%M:%S'  # 待转时间格式

# 将str转为datetime.datetime
for i in raw_time:
    date_times.append(datetime.datetime.strptime(i, date_time_format))

# 将日期与时间拆开，且此时的日期与时间的类型又变成str
for date_time in date_times:
    dates.append(date_time.strftime(date_format))
    times.append(date_time.strftime(time_format))

# 把分离并调整格式的日期和时间储存在data中
data['date'] = dates
data['time'] = times
data_ = data.copy()  # 为避免污染源数据，将数据拷贝至新的DataFrame中进行处理，copy()方法默认深拷贝，之后我们还会提到这个概念，太强了Sensei！

#把非开盘时间（上午9：30-下午15：00之外的时间）剔除掉，但实际上tushare输出的数据data2.csv已经剔除掉了非开盘时间的数据
data_.drop(data_[(data_.time < '09:31:00') | (data_.time > '15:00:00')].index, inplace=True)  # 把非开盘时间通过字符串比较大小去除
data_ = data_.reset_index().drop(columns='index')
data_.head()

#把数据提取出来
#每天开盘240分钟，每5分钟记录一次数据，设置步长为48
Open = data_['open'][1::48].reset_index().drop(columns='index')
Close = data_['close'][47::48].reset_index().drop(columns='index')


#将数据分类，取出最大值、最小值
High = data_[['high', 'date']].groupby('date').max().reset_index()
Low = data_[['low', 'date']].groupby('date').min().reset_index()
Dates = High['date']


#对时间格式进行转换以满足candlestick_ochl()要求
plot_dates = []
for Date in Dates:
    plot_date = datetime.datetime.strptime(Date, date_format)  # 先把日期格式转回datetime.datetime以满足date2num()的类型要求
    plot_dates.append(date2num(plot_date))
    
plot_mat = pd.DataFrame()
plot_mat['time'] = plot_dates
plot_mat['open'] = Open
plot_mat['close'] = Close
plot_mat['high'] = High['high']
plot_mat['low'] = Low['low']
plot_mat.head()

#开始画图
fig, ax = plt.subplots()
candlestick_ochl(ax, plot_mat.values)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.show()

##图像细节处理
fig = plt.figure(facecolor='#07000d', figsize=(15, 10))  # 设置画布背景颜色与画布大小
ax = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, facecolor='#07000d')  


#绘制均值，形成MA
mov_avg_ten = plot_mat['close'].rolling(window=1).mean() # 计算每10天收盘价的均值，每次向下滚动1天
mov_avg_thirty = plot_mat['close'].rolling(window=3).mean()  # 计算每30天收盘价的均值，每次向下滚动1天

#绘制10日与30日均线
ax.plot(plot_mat.time[0:48].values, mov_avg_ten[0:48], '#e1edf9', label='10days', linewidth=1.5)  
ax.plot(plot_mat.time[0:48].values, mov_avg_thirty[0:48], '#4ee6fd', label='10days', linewidth=1.5)


'''
参数分别为：shape，location，rowspan，colspan

shape设置网格布局，(6, 4)即6行4列，location设置起始画图位置，rowspan与colspan分别代表图形在行列上的跨度

这里k线图从第2行，第1列起画，占4行4列

之所以设置6行，是因为还有两个子图RSI曲线和MACD曲线分别在上下(第1行和第6行)

'''
candlestick_ochl(ax, plot_mat[0:48].values, width=0.6, colorup='#ff1717', colordown='#53c156')  # 设置线宽与涨跌颜色
ax.grid(True, color='w')  # 设置网格及其颜色(白色)
ax.xaxis.set_major_locator(mticker.MaxNLocator(10))  # 设置横轴刻度，MaxNLocator确定最多显示多少个刻度
ax.yaxis.set_major_locator(mticker.MaxNLocator())  # 设置纵轴刻度，不填参数则MaxNLocator自动
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 设置横轴显示为时间
ax.yaxis.label.set_color('w')  # 设置y轴标签的颜色(白色)
ax.spines['bottom'].set_color('#5998ff')  # 设置底部轴颜色
ax.spines['top'].set_color('#5998ff')  # 设置顶部轴颜色
ax.spines['left'].set_color('#5998ff')  # 设置左轴颜色
ax.spines['right'].set_color('#5998ff')  # 设置右轴颜色
ax.tick_params(axis='y', colors='w')  # 设置y轴刻度颜色
ax.tick_params(axis='x', colors='w')  # 设置x轴刻度颜色
plt.ylabel('Stock Price and Volume', color='w')  # y轴标签


#绘制蓝色的成交量线
Volume = data_[['date', 'volume']].groupby(by='date').sum().reset_index()
print(Volume)

##绘制成交量图
ax_ = ax.twinx()  # 共享绘图区域
ax_.fill_between(plot_mat.time[0:48].values, 0, Volume.volume[0:48].values,
                facecolor='#00ffe8', alpha=0.4)  # 把[0, volume]之间空白填充颜色，alpha设置透明度
ax_.grid(False)  # 不显示成交量的网格
ax_.set_ylim(0, 4*Volume.volume.values[0:48].max())  # 成交量的y轴范围，为使成交量线处在较下方，设置刻度最大值为成交量最大值的四倍
ax_.spines['bottom'].set_color('#5998ff')
ax_.spines['top'].set_color('#5998ff')
ax_.spines['left'].set_color('#5998ff')
ax_.spines['right'].set_color('#5998ff')
ax_.tick_params(axis='y', colors='w')
ax_.tick_params(axis='x', colors='w')

#绘制RSI曲线
def cal_rsi(df0, period=2):  # 默认周期为2日（随意设置）
    df0['diff'] = df0['close'] - df0['close'].shift(1)  # 用diff储存两天收盘价的差
    df0['diff'].fillna(0, inplace=True)  # 空值填充为0
    df0['up'] = df0['diff']  # diff赋值给up
    df0['down'] = df0['diff']  # diff赋值给down
    df0['up'][df0['up'] < 0] = 0  # 把up中小于0的置零
    df0['down'][df0['down'] > 0] = 0  # 把down中大于0的置零
    df0['avg_up'] = df0['up'].rolling(period).sum() / period  # 计算period天内平均上涨点数
    df0['avg_down'] = abs(df0['down'].rolling(period).sum() / period)  # 计算period天内评价下跌点数
    df0['avg_up'].fillna(0, inplace=True)  # 空值填充为0
    df0['avg_down'].fillna(0, inplace=True)  # 空值填充为0
    df0['rsi'] = 100 - 100 / (1 + (df0['avg_up'] / df0['avg_down']))  # 计算RSI
    return df0  # 返回原DataFrame

plot_mat = cal_rsi(plot_mat)

##绘制RSI曲线
ax0 = plt.subplot2grid((6, 4), (0, 0), sharex=ax, rowspan=1, colspan=4, facecolor='#07000d')  # 第1行第1列起画，占1行4列
col_rsi = '#c1f9f7'  # RSI曲线的颜色
col_pos = '#8f2020'  # 上辅助线及其填充色
col_neg = '#386d13'  # 下辅助线及其填充色
ax0.plot(plot_mat.time[0:48].values, plot_mat.rsi[0:48].values, col_rsi, linewidth=1.5)  # RSI曲线及其颜色，线宽
ax0.axhline(70, color=col_pos)  # 上辅助线及其颜色
ax0.axhline(30, color=col_neg)  # 下辅助线及其颜色
ax0.fill_between(plot_mat.time[0:48].values, plot_mat.rsi[0:48].values, 70, where=(plot_mat.rsi.values[0:48] >= 70),
                 facecolors=col_pos)  # 把RSI曲线大于等于70的部分填充为红色（有可能有一部分不显示，属正常现象）
ax0.fill_between(plot_mat.time[0:48].values, plot_mat.rsi[0:48].values, 30, where=(plot_mat.rsi.values[0:48] <= 30),
                 facecolors=col_neg)  # 把RSI曲线小于等于30的部分填充为绿色（有可能有一部分不显示，属正常现象）
ax0.set_yticks([30, 70])  # 设置辅助线的刻度
ax0.spines['bottom'].set_color("#5998ff")
ax0.spines['top'].set_color("#5998ff")
ax0.spines['left'].set_color("#5998ff")
ax0.spines['right'].set_color("#5998ff")
ax0.tick_params(axis='x', colors='w')
ax0.tick_params(axis='y', colors='w')
plt.ylabel('RSI', color='w')


#绘制MACD曲线
def cal_ema(df0, period, is_dea=False):  # DEA与EMA的计算方式相同，封装在同一个函数中，用is_dea来确认是否是DEA
    for i in range(len(df0)):
        if not is_dea:
            if i == 0:
                df0.loc[i, 'ema'+str(period)] = df0.loc[i, 'close']  # EMA初始值为当天收盘价
            else:
                df0.loc[i, 'ema'+str(period)] = (2*df0.loc[i, 'close']+(period-1)*df0.loc[i-1, 'ema'+str(period)])/(period+1)  # 按公式计算
            ema = df0['ema'+str(period)]
        else:
            if i == 0:
                df0.loc[i, 'dea'+str(period)] = df0.loc[i, 'dif']
            else:
                df0.loc[i, 'dea'+str(period)] = ((period-1)*df0.loc[i-1, 'dea'+str(period)]+2*df0.loc[i, 'dif']) / (period+1)
            ema = df0['dea'+str(period)]
    return ema


def cal_macd(df0, short=12, long=26, m=9):
    short_ema = cal_ema(df0, short)  # 计算12日EMA
    long_ema = cal_ema(df0, long)  # 计算26日EMA
    df0['dif'] = short_ema - long_ema  # 计算DIF
    dea = cal_ema(df0, m, is_dea=True)  # 计算DEA
    df0['macd'] = 2 * (df0['dif'] - df0['dea'+str(m)])  # 计算MACD
    return df0


plot_mat = cal_macd(plot_mat)


##绘制MACD曲线
ax1 = plt.subplot2grid((6, 4), (5, 0), sharex=ax, rowspan=1, colspan=4, facecolor='#07000d') # 第6行第1列起，占1行4列
ax1.plot(plot_mat.time[0:48].values, plot_mat.macd[0:48].values, color='#4ee6fd', linewidth=2)  # MACD线
ax1.plot(plot_mat.time[0:48].values, plot_mat.dea9[0:48].values, color='#e1edf9', linewidth=1)  # DEA线
ax1.fill_between(plot_mat.time[0:48].values, plot_mat.macd[0:48].values-plot_mat.dea9[0:48].values, 0,
                 alpha=0.5, facecolors='#00ffe8')  # 填充差值
ax1.yaxis.set_major_locator(mticker.MaxNLocator())  # 设置纵坐标
ax1.spines['bottom'].set_color('#5998ff')
ax1.spines['top'].set_color('#5998ff')
ax1.spines['left'].set_color('#5998ff')
ax1.spines['right'].set_color('#5998ff')
ax1.tick_params(axis='y', colors='w')
ax1.tick_params(axis='x', colors='w')
plt.ylabel('MACD', color='w')


#隐藏一些坐标轴
plt.setp(ax.get_xticklabels(), visible=False)  # 隐藏ax的x轴
plt.setp(ax0.get_xticklabels(), visible=False)  # 隐藏ax0的x轴
plt.suptitle('K lines', color='w')  # 绘制标题


plt.plot()
