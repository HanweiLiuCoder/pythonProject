#引入:
import matplotlib.pyplot as plt
import easyquotation
import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整
pd.set_option('display.max_rows', None)  # 显示所有的行

#选择 源头
quotation = easyquotation.use('tencent')  # ['jsl'] # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

#获取所有股票行情
market_dict = quotation.market_snapshot(prefix=True)  # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
#遍历
#for key in market_dict.keys():
#    print(key)
#for value in market_dict.values():
#    print(value)
#for key,value in market_dict.items():
#    print(key,value)
i= 1
#市场全量数据转换为pands的DataFrame
df = pd.DataFrame(market_dict.values())
#字段构成
# print(df.loc[1]) #显示字段构成
# name                               万  科Ａ
# code                            sz000002
# now                                19.79
# close                              19.61
# open                               19.51
# volume                        54643200.0
# bid_volume                      29768500
# ask_volume                    24874700.0
# bid1                                19.8
# bid1_volume                       730200
# bid2                                 0.0
# bid2_volume                            0
# bid3                                 0.0
# bid3_volume                            0
# bid4                                 0.0
# bid4_volume                            0
# bid5                                 0.0
# bid5_volume                            0
# ask1                                19.8
# ask1_volume                       730200
# ask2                                 0.0
# ask2_volume                       112600
# ask3                                 0.0
# ask3_volume                            0
# ask4                                 0.0
# ask4_volume                            0
# ask5                                 0.0
# ask5_volume                            0
# 最近逐笔成交
# datetime             2021-12-16 14:59:51
# 涨跌                                  0.18
# 涨跌(%)                               0.92
# high                               20.09
# low                                19.48
# 价格/成交量(手)/成交额    19.79/546432/1082043122
# 成交量(手)                          54643200
# 成交额(万)                      1082040000.0
# turnover                            0.56
# PE                                   6.0
# unknown
# high_2                             20.09
# low_2                              19.48
# 振幅                                  3.11
# 流通市值                              1923.1
# 总市值                              2300.66
# PB                                  1.01
# 涨停价                                21.57
# 跌停价                                17.65
# 量比                                  0.62
# 委差                               -1126.0
# 均价                                  19.8
# 市盈(动)                              10.34
# 市盈(静)                               5.54

#过滤条件
df = df[df['量比'] > 3.00]   #量比大于三倍
df = df[df['涨跌(%)'] < 5.00] #涨幅低于5%
df = df[df['涨跌(%)'] > -5.00] #涨幅低于5% 跌幅低于5%
df = df[df.code.str.contains('300|600|301|002|601|605|688')] #过滤掉基金，指数等数据

cd_list = list(df['code'])
print('过滤出来的股票一览： ',cd_list)

df = df.sort_values(by='涨跌(%)',ascending=False)
print(df[['code','now', '涨跌(%)', '量比', 'high', 'low','name']])

#df_vol = df.nlargest(50,'量比',keep='all')[['code','name', 'now', '涨跌(%)', '量比', 'high', 'low']]


#print(df)



#单只股票 实时行情
#sdata = quotation.real('301011')  # 支持直接指定前缀，如 'sh000001'
#df = pd.DataFrame(data = sdata)
#print(df)

#取得某个数据
#print(float(df.loc['now']))
#print(float(df.loc['涨跌(%)']),'%')


#多只股票行情数据
#sdata = quotation.stocks(['000001', '300311'])  # 支持直接指定前缀，如 'sh000001'
#sdata = quotation.stocks(['000001', '300311'], prefix=True)  # 支持直接指定前缀，如 'sh000001' prefix=True sh, sz
#df = pd.DataFrame(data = sdata)
#print(df)

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

#分时图
# quotation = easyquotation.use("timekline")
# data = quotation.real(['300311'], prefix=True)
#
# tldata = data['sz300311.js']['time_data']
# df_tl = pd.DataFrame(data = tldata, columns=['timeline','price','volume'])
# df_tl.reindex(['timeline'])
# df_tl = pd.to_numeric(df_tl['price'], errors='coerce')
# print(df_tl)
#
# df_tl.plot()
# plt.show()


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
