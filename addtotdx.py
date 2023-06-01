from pytdx.hq import TdxHq_API

# 连接通达信软件
api = TdxHq_API()
api.connect(ip='127.0.0.1', port=7709)

# 获取自选股代码列表
count = api.get_security_count(0)
stocks = api.get_security_list(0, count)

# 添加自选股
block_name = "tmp"
stock_codes = ['000001', '600000', '300001']  # 股票代码列表
api.add_to_block(block_name, stock_codes)

# 断开连接
api.disconnect()
