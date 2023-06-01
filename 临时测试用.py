import  akshare as ak

#df=ak.stock_tfp_em(date="20211026")
#df=df[df['停牌期限'].str.contains('复牌')]
#print(df.head(40))

file = open('E:\\量化投资\\Stocks_Pool\\tscodes.txt', 'a')
a= list(ak.stock_zh_a_spot_em()['代码'])
for cd in a:
    #print(cd)
    file.write(cd+'\n')
file.close
