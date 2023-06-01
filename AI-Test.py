import tushare as ts

# 设置tushare接口的token
ts.set_token('your_token')

# 初始化tushare接口
pro = ts.pro_api()

# 获取A股所有股票代码
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code')

# 遍历股票代码，获取当天股价突破200天的股票
for i, row in data.iterrows():
    try:
        # 获取股票行情数据
        df = pro.daily(ts_code=row['ts_code'], start_date='20220101', end_date='20220401')

        # 判断是否满足条件
        if df.iloc[-1]['close'] > df['close'].rolling(window=200).max().iloc[-1]:
            print(row['ts_code'], row['name'])
    except Exception as e:
        print(row['ts_code'], '查询失败', e)