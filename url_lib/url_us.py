'''
Created on Oct 12, 2017

@author: Coder_J
'''
from configure.common_config import LINE
from configure.area_config import AREA_KEY
"""
url example
http://q.10jqka.com.cn/usa/detail/board/all/field/zdf/order/desc/page/1/ajax/1/      涨跌幅排序
http://q.10jqka.com.cn/usa/detail/board/all/field/stockcode/order/asc/page/1/ajax/1/ 号码排序
http://d.10jqka.com.cn/v6/line/usa_A/01/all.js
"""

_code_url  = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/%s/ajax/1/"
_code_url  = "http://q.10jqka.com.cn/usa/detail/board/all/field/stockcode/order/asc/page/%s/ajax/1/"
# _share_url = "http://d.10jqka.com.cn/v2/%s/%s_%s/%s%s/%s.js"
_share_url = "http://d.10jqka.com.cn/v6/%s/%s_%s/%s%s/%s.js"

_token     = "6fab4b8e8bd63ccd37d1a5130a32659e"


def get_code_url(page = 1):
    ''' 获取所有股票代码的路径 '''
    page = str(page)
    return _code_url %(page)


def get_share_url(cycle_cycle      = LINE    , \
                  area             = AREA_KEY, \
                  symbol           = None    , \
                  share_type       = None    , \
                  transaction_cyle = None    , \
                  year             = None
                  ):
    area   = str(area.name)
    symbol = str(symbol)
    year   = str(year)
    
    if symbol and share_type and transaction_cyle and year :
        return _share_url % (cycle_cycle, area, symbol, share_type, transaction_cyle, year)
    else:        
        print("get_share_url args error ,disable value None !")
        print("args ->", (symbol , share_type , transaction_cyle , year))
        return None
    
    
def get_quote_symbols_nyseandnasdaq():
    _host = "http://172.22.193.235:16001"
    _host = "http://121.43.168.179:8087"
    _url  = _host + "/quote/symbols/nyseandnasdaq?token=%s" % (_token)
    return _url


