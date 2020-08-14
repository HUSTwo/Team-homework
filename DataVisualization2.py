import tushare as ts
token = 'c3a77cb99733084fb6d9bfd7a7fb416b2155b7bdade46c78e752e730' 
ts.set_token(token)
pro = ts.pro_api()
#df = ts.get_h_data('600000', start='2018-08-01', end='2020-08-01')
#ts.get_h_data('600000', index=True)

df = ts.get_hist_data('600000', ktype='5')
df0=df[['open','close','high','low','volume']]
df0.head(10)
print(df0)

