'''
Created on Sep 18, 2017

@author: Coder_J
'''
import enum

# cycle type
LINE = "line"
TIME = "time"

# share type
OFF_SHARE = "0"  # 不复权
ADJ_SHARE = "1"  # 前复权
POS_SHARE = "2"  # 后复权

# transaction cycle
DAY    = "0"     # 日线
WEEK   = "1"     # 周线
MONTH  = "2"     # 月线

CRAWL_PAGE_TYPE = enum.Enum("CRAWL_PAGE_TYPE", 
                            (
                                'json',
                                'text',
                                'html',
                                )
                            )

# print or log level
PRINT_TYPE = enum.Enum("PRINT_TYPE",
                       (
                           'command',
                           'log',
                           'all',
                           )
                       )

PRINT_KEY = PRINT_TYPE.all