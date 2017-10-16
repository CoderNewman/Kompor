'''
Created on Sep 13, 2017

@author: Coder_J
'''
import os
import sys

import datetime

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from configure.common_config import CRAWL_PAGE_TYPE
from configure.area_config import AREA_DICTS_KEY, AREA_KEY
from configure.setting import LINE, OFF_SHARE, DAY
from configure.setting_cn import CN_CASSANDRA_KEYSPACE,\
    CN_CASSANDRA_HOSTS, CN_CASSANDRA_PASSWD, CN_CASSANDRA_PORT,\
    CN_CASSANDRA_USER, CN_TABLES_STOCK_RATIO_FROM_10JQKA,\
    CN_TABLES_STOCK_BASIC_FROM_10JQKA    
from configure.setting_us import US_CASSANDRA_KEYSPACE,\
    US_TABLES_STOCK_RATIO_FROM_10JQKA, US_CASSANDRA_HOSTS, US_CASSANDRA_PASSWD,\
    US_CASSANDRA_PORT, US_CASSANDRA_USER,\
    US_TABLES_STOCK_DAILY_SYMBOLS_FROM_10JQKA

from crawl_lib.crawl import crawl
from url_lib import url_cn, url_us
from dao.casd_dao import CassandraDao
from tools.format_print import jprint as print

import warnings
warnings.filterwarnings("ignore")

crawler = crawl()

class flush(object):
    '''

    '''


    def __init__(self, area = None):
        '''
        Constructor
        '''
        self.cassandra_dao = None
        self.area = None
        self.keyspace = None
        
        if area in AREA_DICTS_KEY:
            self.area = area
            print('flush area', area)
            
        if area is AREA_DICTS_KEY.hs:  # @UndefinedVariable
            self.cassandra_dao = CassandraDao(CN_CASSANDRA_USER, CN_CASSANDRA_PASSWD, CN_CASSANDRA_HOSTS, CN_CASSANDRA_PORT)
            self.keyspace      = CN_CASSANDRA_KEYSPACE
        elif area is AREA_DICTS_KEY.usa:
            self.cassandra_dao = CassandraDao(US_CASSANDRA_USER, US_CASSANDRA_PASSWD, US_CASSANDRA_HOSTS, US_CASSANDRA_PORT)
            self.keyspace      = US_CASSANDRA_KEYSPACE
    
    def craw_ratio(self):
        print('crawl symbols :')
        
        if self.area is AREA_DICTS_KEY.hs:  # @UndefinedVariable
            return self._craw_ratio_hs()
        
        elif self.area is AREA_DICTS_KEY.usa:
            return self._craw_ratio_usa()
            
    def _craw_ratio_hs(self):
            
        url = "http://d.10jqka.com.cn/v6/time/hs_1A0001/last.js"
        json = crawler.craw_to_json(url)
        last_date = json['hs_1A0001']['date']
        
        stocks = [last_date, ]
        page_number = 1
        while(True):
            url = url_cn.get_code_url(page_number)
            page_stock, is_tail = self.crawl_hs(url, CRAWL_PAGE_TYPE.html)  # @UndefinedVariable
            stocks.append(page_stock)
            if is_tail:
                break
            else:
                page_number += 1
        print('crawl hs symbols completed !')
        return stocks
    
    def _craw_ratio_usa(self):
            
        url = "http://d.10jqka.com.cn/v6/time/gzs_SPX/last.js"
        headers = {
            "Referer":"http://stockpage.10jqka.com.cn/HQ_v4.html",
            }
        json_val = crawler.craw_to_json(url, headers = headers)
        
        last_date = json_val['gzs_SPX']['date']
        
        stocks = [last_date, ]
        page_number = 1
        while(True):
            url = url_us.get_code_url(page_number)
            page_stock, is_tail = self.crawl_table(url, CRAWL_PAGE_TYPE.html)  # @UndefinedVariable
            stocks.append(page_stock)
            if is_tail:
                break
            else:
                page_number += 1
        print('crawl us symbols completed !')
        return stocks

    def crawl_table(self, url, crawl_page_type):
        if crawl_page_type is CRAWL_PAGE_TYPE.html:  # @UndefinedVariable
            soup = crawler.craw_to_bs4(url)
            tbody = soup.table.tbody
            trs = tbody.findAll("tr")
            _page = []            
            for tr in trs:
                _row = []
                for td in tr.findChildren():
                    _row.append(td.get_text())
                _page.append(_row)

            count = soup.div.span.get_text() or None
            cmp_count = str(count).split("/")
            is_tail = cmp_count[0] == cmp_count[1]
            print('The progress of stock crawl', count)

            return _page, is_tail


    def insert_ratio_to_db(self, stocks):
        if self.area is AREA_DICTS_KEY.hs:  # @UndefinedVariable
            return self._insert_ratio_to_db_hs(stocks)
        
        elif self.area is AREA_DICTS_KEY.usa:
            return self._insert_ratio_to_db_usa(stocks)
        
    def _insert_ratio_to_db_usa(self, stocks):
        sql = "UPDATE " + US_TABLES_STOCK_RATIO_FROM_10JQKA + " SET \
                name                  = ?, \
                price                 = ?, \
                size_ratio            = ?, \
                rise_fall             = ?, \
                changed_hands_ratio   = ?, \
                volume                = ?, \
                pe_ratio              = ?, \
                turnover              = ?, \
                week_high_52          = ?, \
                weeks_minimum_52      = ?  \
            where \
                symbol = ? and \
                date = ? "

        _date = stocks[0]
        date = datetime.datetime.strptime(_date,'%Y%m%d')
        elements = []
        del stocks[0]
        for page in stocks:
            for row in page:
                try:
                    symbol                = row[1]
                    name                  = row[3]
                    price                 = row[5]
                    size_ratio            = row[6]
                    rise_fall             = row[7]
                    pe_ratio              = row[8]
                    changed_hands_ratio   = row[9]
                    volume                = row[10]
                    turnover              = row[11]
                    week_high_52          = row[12]
                    weeks_minimum_52      = row[13]
                    
                    elements.append(
                        [name, price, size_ratio, rise_fall, changed_hands_ratio, \
                         volume, pe_ratio, turnover, week_high_52, \
                         weeks_minimum_52, symbol, date])
                except Exception as e:
                    print(e)
                    pass
                
        stocks.insert(0, _date)
        
        if elements:
            self.cassandra_dao.batch_execute_prepared_one_sql(sql, elements, keyspace=self.keyspace ,slice_length=100)
            print('insert to db completed !')
        
    def _insert_ratio_to_db_hs(self, stocks):
        sql = "UPDATE " + CN_TABLES_STOCK_RATIO_FROM_10JQKA + " SET \
                name                  = ?, \
                price                 = ?, \
                size_ratio            = ?, \
                rise_fall             = ?, \
                pace_ratio            = ?, \
                changed_hands_ratio   = ?, \
                than                  = ?, \
                amplitude_ratio       = ?, \
                turnover              = ?, \
                shares_outstanding    = ?, \
                current_market        = ?, \
                pe_ratio              = ?  \
            where \
                symbol = ? and \
                date = ? "

        _date = stocks[0]
        date = datetime.datetime.strptime(_date,'%Y%m%d')
        elements = []
        del stocks[0]
        for page in stocks:
            for row in page:
                try:
                    symbol                = row[1]
                    name                  = row[3]
                    price                 = row[5]
                    size_ratio            = row[6]
                    rise_fall             = row[7]
                    pace_ratio            = row[8]
                    changed_hands_ratio   = row[9]
                    than                  = row[10]
                    amplitude_ratio       = row[11]
                    turnover              = row[12]
                    shares_outstanding    = row[13]
                    current_market        = row[14]
                    pe_ratio              = row[15]
                    
                    elements.append(
                        [name, price, size_ratio, rise_fall, pace_ratio, \
                         changed_hands_ratio, than, amplitude_ratio, turnover, \
                         shares_outstanding, current_market, pe_ratio, symbol, date])
                except Exception as e:
                    print(e)
                    pass
                
        stocks.insert(0, _date)
        
        if elements:
            self.cassandra_dao.batch_execute_prepared_one_sql(sql, elements, keyspace=self.keyspace ,slice_length=100)
            print('insert to db completed !')


    def get_db_symbols(self):
        symbols = []
        sql = ""
        if self.area is AREA_DICTS_KEY.hs:  # @UndefinedVariable
            sql = "SELECT DISTINCT SYMBOL FROM " + CN_TABLES_STOCK_RATIO_FROM_10JQKA
        elif self.area is AREA_DICTS_KEY.usa:  # @UndefinedVariable
            sql = "SELECT DISTINCT SYMBOL FROM " + US_TABLES_STOCK_RATIO_FROM_10JQKA
            
        result_set = self.cassandra_dao.execute_sql(sql, keyspace=self.keyspace)
        for result in result_set:
            symbols.append(result.symbol)
        return symbols;    


    def crawl_quote(self):
        symbols = self.get_db_symbols()
        if self.area is AREA_DICTS_KEY.hs:  # @UndefinedVariable            
            self.crawl_cn_basic_from_10jqka(symbols, AREA_DICTS_KEY.hs)  # @UndefinedVariable
        
#         elif self.area is AREA_DICTS_KEY.usa:  # @UndefinedVariable
#             self.crawl_us_basic_from_10jqka(symbols, AREA_DICTS_KEY.usa)  # @UndefinedVariable


    def crawl_cn_basic_from_10jqka(self, symbols, area):
        sql = "UPDATE " + CN_TABLES_STOCK_BASIC_FROM_10JQKA + " SET \
                rt       = ?, \
                total    = ?, \
                start    = ?, \
                year     = ? \
            where \
                symbol = ? and \
                name = ? "
        elements = []
        
        for symbol in symbols:
            url = url_cn.get_share_url(LINE, area, symbol, OFF_SHARE, DAY, 'last')
            data = crawler.craw_to_json(url)
            try:                    
                del data["data"]
                elements.append([
                    str(data["rt"]),
                    str(data["total"]),
                    datetime.datetime.strptime(data["start"],'%Y%m%d'),                        
                    str(data["year"]),
                    str(symbol),
                    str(data["name"]).replace(" ", ""),
                    ])
                print("crawling :", symbol, data["name"])
            except:
                print("Exception", )
                print(sys.exc_info())
                pass

        print("inserting to db.")
        if elements:
            self.cassandra_dao.batch_execute_prepared_one_sql(sql, elements, keyspace=self.keyspace ,slice_length=100)
            print('insert to db completed !')
    
    def insert_symbols_to_db(self, stocks):
        if self.area is AREA_DICTS_KEY.usa:  # @UndefinedVariable
            sql = "UPDATE " + US_TABLES_STOCK_DAILY_SYMBOLS_FROM_10JQKA + " SET \
                    symbols = ?  \
                where \
                    trading_date = ? "
    
            _date = stocks[0]
            date = datetime.datetime.strptime(_date,'%Y%m%d')
            elements = []
            symbols  = []
            del stocks[0]
            for page in stocks:
                for row in page:
                    symbol = row[1]
                    symbols.append(symbol)
            
            symbols = str(symbols)
            elements.append([symbols, date])                    
            stocks.insert(0, _date)            
            if elements:
                self.cassandra_dao.batch_execute_prepared_one_sql(sql, elements, keyspace=self.keyspace ,slice_length=100)
                print('insert to db completed !')
            
            
            
            
    
def main():
    print('start 10jqka worker !')
    crawl = flush(AREA_KEY)
    stocks = crawl.craw_ratio()
    crawl.insert_ratio_to_db(stocks)
    crawl.insert_symbols_to_db(stocks)
    crawl.crawl_quote()
    print('crawl 10jqka has Completed !')

if __name__ == "__main__":
    main()