import tushare as ts
import pandas as pd

class tushare_data:
    pro = None
    def __init__(self,name,token):
        self.name = name
        ts.set_token(token)

    def get_data_by_code(self,code):
        data = ts.pro_bar(code,adj='hfq',start_date='20200101',end_date='20200828')
        print(data)

    def get_all_data(self):
        pro = ts.pro_api()
        data = pro.query('stock_basic', list_status='L',
                         fields='ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_date')
        print(data)

    def get_data_for_bt(self,code,start_date):
        data = ts.pro_bar(ts_code=code, adj='hfq', start_date=start_date)
        data.index = pd.to_datetime(data.trade_date)
        data = data.sort_index()
        data['volume'] = data.vol
        data['openinterest'] = 0
        data['datetime'] = pd.to_datetime(data.trade_date)
        data = data[['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest']]
        data = data.fillna(0)
        print(data)
        return data

if __name__ == '__main__':
    data = tushare_data('test','token')
    data.get_all_data()
    data.get_data_by_code('600089.SH')
    data.get_data_for_bt('600089.SH','20220530')

