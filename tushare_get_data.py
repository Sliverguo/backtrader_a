import tushare as ts


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


if __name__ == '__main__':
    data = tushare_data('test','token')
    data.get_all_data()
    data.get_data_by_code('600089.SH')

