'''
Created on Sep 18, 2017

@author: Coder_J
'''
import os
import sys
import json
import datetime
from time import sleep
from kom_tools import notice


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from configure.setting import DAY, LINE, OFF_SHARE, ADJ_SHARE, MONITOR_MAILS
from crawl_lib.crawl import crawl
from url_lib import url_us
from configure.area_config import AREA_DICTS_KEY, AREA_KEY
from dao.casd_dao import CassandraDao
from configure.setting_us import US_CASSANDRA_HOSTS, US_CASSANDRA_PASSWD,\
    US_CASSANDRA_PORT, US_CASSANDRA_USER, US_CASSANDRA_KEYSPACE,\
    US_TABLES_STOCK_DAILY_OFF_SHARE_FROM_10JQKA,\
    US_TABLES_STOCK_DAILY_ADJ_SHARE_FROM_10JQKA
from kom_tools.format_print import jprint as print

crawl = crawl()

class sam(object):
    '''
    从同花顺获取日交易数据
    '''


    def __init__(self, area = None):
        '''
        Constructor
        '''
        self.cassandra_dao = None
        self.keyspace      = None
        self.area          = area
        print('sam area', area)
        
        if self.area is AREA_DICTS_KEY.usa:
            self.cassandra_dao = CassandraDao(US_CASSANDRA_USER, US_CASSANDRA_PASSWD, US_CASSANDRA_HOSTS, US_CASSANDRA_PORT)
            self.keyspace      = US_CASSANDRA_KEYSPACE

    
    def crawl_daily(self, symbols):
        print('crawl symbols length is', len(symbols))
        
        if self.area is AREA_DICTS_KEY.usa:
            return self.crawl_daily_us(symbols)
            
            
    def insert_to_db(self, table_name, elements):
                
        sql = "UPDATE " + table_name + " SET " + \
            "name     = ?, " + \
            "open     = ?, " + \
            "high     = ?, " + \
            "low      = ?, " + \
            "close    = ?, " + \
            "volumn   = ?  " + \
            "where " + \
            "symbol = ? and " + \
            "date   = ? "
        
        if elements:
            self.cassandra_dao.batch_execute_prepared_one_sql(sql, elements, keyspace=self.keyspace ,slice_length=100)
            print('insert to db completed !')
    
    
    def crawl_daily_us(self, symbols):
        error_symbols = []
        headers = {}
        headers['Referer'] = "http://stockpage.10jqka.com.cn/HQ_v4.html"
        error_syms = self._crawl_daily_us(symbols, headers, OFF_SHARE, US_TABLES_STOCK_DAILY_OFF_SHARE_FROM_10JQKA)
        error_symbols.append(['OFF_SHARE', error_syms])
        error_syms = self._crawl_daily_us(symbols, headers, ADJ_SHARE, US_TABLES_STOCK_DAILY_ADJ_SHARE_FROM_10JQKA)
        error_symbols.append(['ADJ_SHARE', error_syms])
        
        print(error_symbols)
        return error_symbols
        
    def _crawl_daily_us(self, symbols, headers, share_type, table_name):
        error_symbols = []
        
        for symbol in symbols:
            try:
                print('crawling symbol', symbol, share_type)
                url = url_us.get_share_url(LINE, AREA_KEY, symbol, share_type, DAY, "all")
                stock = crawl.craw_to_json(url, headers)
                stock['url'] = url
                elements = self.analysis_prices_us(symbol, stock)
                self.insert_to_db(table_name, elements)
            except Exception as e:
                print(e)
                error_symbols.append([symbol, e])
                pass
            
#             print('sleeping 5 senconds')
#             sleep(5)
            
            
    def analysis_prices_us(self, symbol, stock_value):
        
        url         = stock_value['url']
        total       = stock_value['total']
        start       = stock_value['start']
        name        = stock_value['name']
        sortYear    = stock_value['sortYear']
        priceFactor = stock_value['priceFactor']
        title       = stock_value['title']
        dates       = stock_value['dates']
        volumn      = stock_value['volumn']
        price       = stock_value['price']
        
        dates    = dates.split(",")
        volumn   = volumn.split(",")
        price    = price.split(",")
        
        id_date   = 0
        id_volumn = 0
        id_price  = 0
        
        YEAR      = 0
        COUNT     = 1
        
        elements  = []
        
        for i_year in sortYear:
            year  = i_year[YEAR]
            count = i_year[COUNT]
            
            print('analysis', symbol, year)
            
            for i in range(count):
                
                try:
                    date  =       str(year) + dates[id_date]
                    date  = datetime.datetime.strptime(date,'%Y%m%d')
                    
                    low   = float (price[id_price + 0])
                    open  = float (price[id_price + 1])  + low  # @ReservedAssignment
                    high  = float (price[id_price + 2])  + low
                    close = float (price[id_price + 3])  + low
                    vol   = float (volumn[id_volumn])
                    
                    element = [name, open, high, low, close, vol, symbol, date]
                    elements.append(element)
                
                except Exception as e:
                    print(e)
                    pass
                
                id_date   += 1
                id_volumn += 1
                id_price  += 4
                
        return elements
    
    def get_symbols(self):
        if self.area is AREA_DICTS_KEY.usa:
            url = url_us.get_quote_symbols_nyseandnasdaq()
            print(url)
            symbols = crawl.craw_to_string(url)
            symbols = json.loads(symbols)['data']['symbols']
            return symbols
            
        
        
def main():
    print('start daily_10jqka worker !')
    newman  = sam(AREA_KEY)
    symbols = newman.get_symbols()
    symbols.sort()
    error_symbols = newman.crawl_daily(symbols)
    
    msg = 'daily_10jqka worker has Completed !\n' +\
        'error symbols: \n' +\
        str(error_symbols)
    
    notice.send_email(MONITOR_MAILS, 'daily_10jqka has finished !' ,msg)
    print('email has sent.')
    print('daily_10jqka worker has Completed !')

if __name__ == "__main__":
    main()
    
    
    