#收集数据
import pandas as pd
import tushare as ts

token = 'c3a77cb99733084fb6d9bfd7a7fb416b2155b7bdade46c78e752e730' 
ts.set_token(token)

pro = ts.pro_api()

df1 = ts.get_hist_data('600000', ktype='5')
df0=df1[['open','close','high','low','volume']]
df0.head(10)
print(df0)
df0.to_csv('data2.csv')

df = pro.daily(ts_code='600000.SH, 600010.SH, 600015.SH', start_date='20200301', end_date='20200801')
df.head(10)

df.to_csv('data.csv')
#数据处理：
sh0 = df[::3].set_index('trade_date')
sh1 = df[1::3].set_index('trade_date')
sh2 = df[2::3].set_index('trade_date')

sh0.head()

#开始画图：
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
sh0.plot(ax=ax, y='close', label='600000')
sh1.plot(ax=ax, y='close', label='600010')
sh2.plot(ax=ax, y='close', label='600015')

plt.legend(loc='upper left')
plt.show()


mean_share_list = [sh0['close'].mean(), sh1['close'].mean(), sh2['close'].mean()]
mean_share_series = pd.Series(mean_share_list, index=['600000', '600010', '600015'])
mean_share_series.plot(kind='bar')
plt.xticks(rotation=360)
plt.show()
