'''
Created on Sep 1, 2017

@author: Coder_J
'''
import requests
import json

from requests.models import Response
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter


class crawl(object):
    '''
    crawl_lib
    '''

    def craw_to_string(self, url, headers=None):
        '''  爬出文本数据  '''
        
        result = ''
        r= Response()
        
        _headers = {}
        _headers['Accept-Encoding'] = 'gzip, deflate'
        _headers['User-agent']      = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        _headers['Accept']          = '*/*'
#         _headers['Referer']         = 'http://stockpage.10jqka.com.cn/HQ_v4.html'
        
        if headers is not None:
            for head in headers:
                _headers[head] = headers[head]
        
        try:
#             r = requests.get(headers, verify=False)
            r = requests.get(url, headers = _headers, verify=False)
        except:
            pass

        index = 0
        while r.status_code != 200:
            try:
                r = requests.get(url, headers = _headers, verify=False)
            except:
                pass
                
            if index >= 5:
                break
            index += 1
            
        if r.status_code == 200:
            result = str(r.text)
        else:
            print('crawl response error', r.status_code)
            
        return result
            
    def craw_to_json(self, url, headers=None):
        '''  爬出json数据  '''
        result = ''
        text = self.craw_to_string(url, headers)
        
        index = text.find("(");
        title = text[0:index]
        text = text[index + 1:-1]
        if len(text) != 0:
            json_value = json.loads(text)
            json_value['title'] = title
            result = json_value
        
        return result
    
    def craw_to_list(self, url, headers=None):
        '''  爬出数据数组  '''
        
        data = []
        try:
            for d in str(self.craw_to_json(url, headers)['data']).split(';'):
                data.append(d)
        except:
            pass
        return data
    
    def craw_to_bs4(self, url, headers=None):
        html = self.craw_to_string(url, headers)
        soup = BeautifulSoup(html)
        return soup