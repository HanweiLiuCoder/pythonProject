import numpy as np

def has_high_volatility(arr):
    std = np.std(arr)
    if std > threshold:  # 这里可以根据需要设置一个阈值来定义什么程度的波动算是剧烈
        return True
    else:
        return False

# 示例用法
data = [100, 120, 103, 140, 150, 210, 210, 120, 130, 240, 150, 110]
threshold = 4  # 根据具体情况设置阈值
if has_high_volatility(data):
    print("该数组有过剧烈的波动")
else:
    print("该数组没有过剧烈的波动")