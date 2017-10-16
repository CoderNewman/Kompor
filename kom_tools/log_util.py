#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : log_util.py
# @Brief   : 
# @Author  : chunsong@kavout.com
# @Time    : 2017/7/3 下午5:35

import os
import logging
from cloghandler import ConcurrentRotatingFileHandler


logger_dict = {}


def get_logger(logger_name, log_level=logging.INFO):
    if logger_name in logger_dict:
        return logger_dict[logger_name]

    # 修改为可以多进程写入的日志系统
    logger = create_concurrent_logger(logger_name, log_level)
    logger_dict[logger_name] = logger

    return logger


def create_concurrent_logger(logger_name, level):
    """
    创建一个多进程使用的日志
    @author: liqing@kavout.com
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir,"logs")
    if not os.path.exists(log_path):
            os.makedirs(log_path)    
    logfile = os.path.join(log_path, logger_name + ".log")
    filesize = 800*1024*1024
    log = logging.getLogger(logger_name)
    rotate_handler = ConcurrentRotatingFileHandler(logfile, "a", filesize, 5,encoding="utf-8")
    rotate_handler.setLevel(level)
    fmt = "[%(asctime)-15s %(levelname)s %(filename)s:%(lineno)d] [%(process)s] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    rotate_handler.setFormatter(formatter)
    log.addHandler(rotate_handler)
    log.setLevel(level)
    return log
    

def create_logger(logger_name, level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler

    if not os.path.isdir('./logs'):
        os.mkdir('./logs')
    log_path = "./logs/" + logger_name + ".log"

    fh = logging.FileHandler(log_path, mode='w')
    # fh = handlers.TimedRotatingFileHandler(filename=log_path, when='midnight', backupCount=7)
    fh.setLevel(level)

    # create formatter
    fmt = "[%(asctime)-15s %(levelname)s %(filename)s:%(lineno)d %(funcName)s] [%(process)s %(thread)s] %(message)s"
    fmt = "[%(asctime)-15s %(levelname)s %(filename)s:%(lineno)d] [%(process)s] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
