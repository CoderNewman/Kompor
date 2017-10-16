'''
Created on Sep 19, 2017

@author: Coder_J
'''

import time
import logging
from kom_tools import log_util
from configure.common_config import PRINT_KEY, PRINT_TYPE

logger = log_util.get_logger('debug', log_level=logging.INFO)

def jprint(*args, sep = '', end='\n'):  # @ReservedAssignment
    if PRINT_KEY is PRINT_TYPE.all or PRINT_KEY is PRINT_TYPE.command:  # @UndefinedVariable
    
        sys_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print('[' + sys_time + ']',end=' ')
        print(*args, sep = sep, end=end)
        
    if PRINT_KEY is PRINT_TYPE.all or PRINT_KEY is PRINT_TYPE.log:  # @UndefinedVariable
        if args:
            for arg in args:
                logger.info(str(arg))
        