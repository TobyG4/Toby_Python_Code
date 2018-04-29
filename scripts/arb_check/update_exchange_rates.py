import json
from datetime import datetime

import pandas.io.sql as psql
import requests
import os
import sys


crypto_tools_dir = os.getcwd().split('/scripts/')[0] + '/scripts/'
sys.path.append(crypto_tools_dir)

from crypto_tools import *

class FiatExchangeRates(object):
    """
    """

    def __init__(self):
        """
        """

        self.port = 3306
        self.host = "159.89.20.249"
        self.database_name = 'crypto_test'
        self.user = 'toby'
        self.password = '*'
        self.database = DatabaseConnect(self.host, self.database_name, self.user, self.password, self.port)
        self.database.database_connect()
        self.get_crypto_currency_id()

    def get_crypto_currency_id(self):
        """
        """

        sql_str = """ SELECT ccl.name,cc.id AS id,exchange_id FROM crypto_test.crypto_currency cc
                        INNER JOIN crypto_test.crypto_currency_lookup ccl ON ccl.crypto_currency_id = cc.id
                        INNER JOIN crypto_test.exchange e ON ccl.exchange_id = e.id
                        WHERE e.name = "http://api.fixer.io/"
                    """

        results = psql.read_sql(sql_str, con=self.database.mydb)
        #id of api.ficer.io
        self.source_id = results['exchange_id'].iloc[0]
        crypto_dict = {}
        for ind, row in results.T.iteritems():
            name = row['name']
            crypto_dict[name] = row['id']

        self.crypto_dict = crypto_dict

    def get_exchange_rate(self):
        """
        """
        #print "Getting exchnage rates from  http://api.fixer.io/latest?base=USD..."
        exchange_rate = requests.get("http://api.fixer.io/latest?base=USD")
        #print "Finished."
        exchange_rate =  exchange_rate.text
        exchange_rate_dict = json.loads(exchange_rate)
        self.exchange_rate_dict = exchange_rate_dict
        #print self.exchange_rate_dict

        base_crypto = exchange_rate_dict['base']
        base_crypto_id = self.crypto_dict[base_crypto]
        server_time = self.exchange_rate_dict['date']

        for i in self.exchange_rate_dict['rates']:


            rate = self.exchange_rate_dict['rates'][i]
            try:
                crypto_id2 = self.crypto_dict[i]
            except:
                #print "need lookup for ",i
                continue

            #print base_crypto_id, crypto_id2

            ut = datetime.now()
            sql_str = """INSERT IGNORE INTO crypto_test.fiat_exchange_rates(crypto_currency_id,crypto_currency_id2,source_id,exchange_rate,server_time,ut)
                                                        VALUES(%s,%s,%s,%s,"%s","%s")
                                                        """ %(crypto_id2,base_crypto_id,self.source_id,rate,server_time,ut)
            self.database.cursor.execute(sql_str)
            try:
                self.database.mydb.commit()
            except:
                self.database.mydb.rollback()



def main():
    """
    """

    FER = FiatExchangeRates()
    FER.get_exchange_rate()


if __name__ == "__main__":
    main()
