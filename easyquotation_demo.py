#引入:
import matplotlib.pyplot as plt
import easyquotation
import pandas as pd
import akshare as ak

#选择 源头
quotation = easyquotation.use('jsl')  # ['jsl'] # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

#获取所有股票行情
#quotation.market_snapshot(prefix=True)  # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀

#单只股票 实时行情
#sdata = quotation.real('301011')  # 支持直接指定前缀，如 'sh000001'
#df = pd.DataFrame(data = sdata)
#print(df)

#取得某个数据
#print(float(df.loc['now']))
#print(float(df.loc['涨跌(%)']),'%')


#多只股票行情数据
# quotation = easyquotation.use('qq')  # ['jsl'] # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
# sdata = quotation.stocks(['sh000001'])  # 支持直接指定前缀，如 'sh000001'
# #sdata = quotation.stocks(['000001', '300311'], prefix=True)  # 支持直接指定前缀，如 'sh000001' prefix=True sh, sz
# df = pd.DataFrame(data = sdata)
# print(df)

#同时获取指数和行情
#quotation.stocks(['sh000001', 'sz000001'], prefix=True)

#更新股票代码
#easyquotation.update_stock_codes()


#获取分级基金信息
#quotation.funda()  # 参数可选择利率、折价率、交易量、有无下折、是否永续来过滤
#quotation.fundb()  # 参数如上

#分级基金套利接口
#quotation.fundarb(jsl_username, jsl_password, avolume=100, bvolume=100, ptype='price')

#指数ETF查询接口  # ['jsl']
# etf = quotation.etfindex(index_id="", min_volume=0, max_discount=None, min_discount=None)
# df_etf = pd.DataFrame(data = etf)
# print(df_etf)

#返回值
# {
#     "510050": {
#         "fund_id": "510050",                # 代码
#         "fund_nm": "50ETF",                 # 名称
#         "price": "2.066",                   # 现价
#         "increase_rt": "0.34%",             # 涨幅
#         "volume": "71290.96",               # 成交额(万元)
#         "index_nm": "上证50",                # 指数
#         "pe": "9.038",                      # 指数PE
#         "pb": "1.151",                      # 指数PB
#         "index_increase_rt": "0.45%",       # 指数涨幅
#         "estimate_value": "2.0733",         # 估值
#         "fund_nav": "2.0730",               # 净值
#         "nav_dt": "2016-03-11",             # 净值日期
#         "discount_rt": "-0.34%",            # 溢价率
#         "creation_unit": "90",              # 最小申赎单位(万份)
#         "amount": "1315800",                # 份额
#         "unit_total": "271.84",             # 规模(亿元)
#         "index_id": "000016",               # 指数代码
#         "last_time": "15:00:00",            # 价格最后时间(未确定)
#         "last_est_time": "23:50:02",        # 估值最后时间(未确定)
#     }
# }

#分时图 特别注意 日线分时图行情不准确
# quotation = easyquotation.use("timekline")
# data = quotation.real(['sz300001'])
# print(data)
# #
# print(data['sz300001.js']['date'])
# tldata = data['sz300001.js']['time_data']
# df_tl = pd.DataFrame(data = tldata, columns=['timeline','price','volume'])
# #df_tl.reindex(['timeline'])
# print(df_tl)
# print('---------------')
#var_data = df_tl.var(numeric_only=None)
#print(var_data)

#取得指定日期的分时图
stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="300640", period='1', adjust='', start_date="2021-12-16 09:30:00", end_date="2021-12-16 15:00:00")
print(stock_zh_a_hist_min_em_df)



#df_tl = pd.to_numeric(df_tl['price'], errors='coerce')
#df_tl.plot()
#plt.show()


#返回值
# {
#    'sh603828': {
#         'date': '170721',  #日期
#         'time_data': {
#             '201707210930': ['0930', '19.42', '61'], # [时间, 当前价, 上一分钟到这一分钟之间的成交数量]
#             '201707210931': ['0931', '19.42','122'],
#             '201707210932': ['0932', '19.43', '123'],
#             '201707210933': ['0933', '19.48', '125'],
#             '201707210934': ['0934', '19.49', '133'],
#             '201707210935': ['0935', '19.48', '161'],
#             ...
#     }
# }

#HK股市的日k线图
# quotation = easyquotation.use("daykline")
# data = quotation.real('sz300311')
# print(data)
#
# dkdata = data['300311']
# df_dk = pd.DataFrame(data = dkdata, columns=['日期', '今开', '今收', '最高', '最低', '成交量','col1','col2','col3','col4','col5'])
# df_dk.reindex(['日期'])
#
# print(df_dk)
# df_dk = pd.to_numeric(df_dk['今收'], errors='coerce')
# #print(df_dk)
#
# df_dk.plot()
# plt.show()
#
#返回值
# {
#     '00001': [
#         ['2017-10-09', '352.00', '349.00', '353.00', '348.60', '13455864.00'],  # [日期, 今开, 今收, 最高, 最低, 成交量 ]
#         ['2017-10-10', '350.80', '351.20', '352.60', '349.80', '10088970.00'],
#     ]
#     '00700': [
#
#     ]
# }
# }

#港股行情
#quotation = easyquotation.use("hkquote")
#data = quotation.real(['00001', '00700'])
#print(data)
#返回值
# {
# '00001':
# {
#     'stock_code': '00001',  # 股票代码
#     'lotSize': '"100',  # 每手数量
#     'name': '长和',  # 股票名称
#     'price': '97.20',  # 股票当前价格
#     'lastPrice': '97.75',  # 股票昨天收盘价格
#     'openPrice': '97.75',  # 股票今天开盘价格
#     'amount': '1641463.0',  # 股票成交量
#     'time': '2017/11/29 15:38:58',  # 当前时间
#     'high': '98.05',  # 当天最高价格
#     'low': '97.15'  # 当天最低价格
# },
# '00700':
# {
#     'stock_code': '00700',
#     'lotSize': '"100',
#     'name': '腾讯控股',
#     'price': '413.20',
#     'lastPrice': '419.20',
#     'openPrice': '422.20',
#     'amount': '21351010.0',
#     'time': '2017/11/29 15:39:01',
#     'high': '422.80',
#     'low': '412.40'
# }
# }
