'''
Created on Oct 13, 2017

@author: Coder_J
'''
from configure.area_config import AREA_KEY, AREA_DICTS_KEY
from dao.casd_dao import CassandraDao
from configure.setting_us import US_CASSANDRA_HOSTS, US_CASSANDRA_PASSWD,\
    US_CASSANDRA_PORT, US_CASSANDRA_USER, US_CASSANDRA_KEYSPACE


class sy_list(object):
    
    def __init__(self, area = None):
        self.cassandra_dao = None
        self.keyspace      = None
        
        if area is AREA_DICTS_KEY.usa:
            self.cassandra_dao = CassandraDao(US_CASSANDRA_USER, US_CASSANDRA_PASSWD, US_CASSANDRA_HOSTS, US_CASSANDRA_PORT)
            self.keyspace      = US_CASSANDRA_KEYSPACE
    
        

def main():
    print('start calculate symbol list worker !')
    calcor = sy_list(AREA_KEY)
    
    
    print('start calculate symbol list worker has Completed !')

if __name__ == "__main__":
    main()