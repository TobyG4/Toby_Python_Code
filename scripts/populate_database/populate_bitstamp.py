import json
import os
import sys

import pandas.io.sql as psql
import requests

crypto_tools_dir = os.getcwd().split('/scripts/')[0] + '/scripts/'
sys.path.append(crypto_tools_dir)

from crypto_tools import *


class PopulateCryptoBitstamp(object):
    """
    """

    def __init__(self):
        """
        """
        self.port = 3306
        self.host = "159.89.20.249"
        self.database_name = 'crypto_test'
        self.user = 'toby'
        self.password = 'R1i9p1p1l9e0$'
        self.database = DatabaseConnect(self.host, self.database_name, self.user, self.password, self.port)
        self.database.database_connect()
        self.get_bitstamp_exchange_id()

    def get_bitstamp_exchange_id(self):
        """
        """
        sql_str = """SELECT id FROM crypto_test.exchange
                    WHERE name = 'bitstamp' """

        results = psql.read_sql(sql_str, con=self.database.mydb)
        self.exchange_id = results['id'].loc[0]

    def get_bitstamp_asset_pairs_lookup(self):
        """
        """
        sql_str = """SELECT apl.name,apl.id AS asset_pairs_lookup_id 
                    FROM crypto_test.asset_pairs_lookup apl
                    INNER JOIN crypto_test.exchange e ON e.id = apl.exchange_id
                    WHERE e.name = 'bitstamp'"""

        results = psql.read_sql(sql_str, con=self.database.mydb)
        asset_pairs_lookup_dict = {}
        self.asset_pairs_list = results['name'].tolist()
        self.asset_pairs_str = ','.join(self.asset_pairs_list)
        print (self.asset_pairs_str)

        for ind, row in results.T.iteritems():
            name = row['name']
            asset_pairs_lookup_dict[name] = row['asset_pairs_lookup_id']

        self.asset_pairs_lookup_dict = asset_pairs_lookup_dict

    def populate_bitstamp_data(self):
        """

        """
        self.get_bitstamp_asset_pairs_lookup()

        for bitstamp_asset_pair in self.asset_pairs_list:

            #print (bitstamp_asset_pair)

            url = """https://www.bitstamp.net/api/v2/order_book/%s/""" % (bitstamp_asset_pair)
            all_response = requests.get(url)

            all_json = all_response.text
            all_json_dict = json.loads(all_json)

            timestamp = all_json_dict['timestamp']
            # bitstamp timestamp, no order time of order
            order_time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

            bids = all_json_dict['bids']
            asks = all_json_dict['asks']

            asset_pairs_lookup_id = self.asset_pairs_lookup_dict[bitstamp_asset_pair]
            bid_ask_list = [[1, bids], [2, asks]]

            for order_type in bid_ask_list:
                order_type_id = order_type[0]

                x = 0

                for order in order_type[1]:
                    x = x +1
                    price = order[0]
                    quantity = order[1]
                    # need to remove trailing zeros before and after decimal
                    new_price = '{0:g}'.format(float(price))
                    new_quantity = '{0:g}'.format(float(quantity))

                    ut = datetime.now()
                    sql_str = """INSERT IGNORE INTO crypto_test.order_book(asset_pairs_lookup_id,order_type_id,price,quantity,order_time,server_time,ut)
                                            VALUES(%s,%s,%s,%s,"%s","%s","%s")
                                            """ % (
                    asset_pairs_lookup_id, order_type_id, float(new_price), float(quantity), order_time, order_time, ut)

                    self.database.cursor.execute(sql_str)
                    try:
                        self.database.mydb.commit()
                    except:
                        self.database.mydb.rollback()

                    #If first 5 rows of datframe we want to insert into live.
                    if x < 6:
                        ut = datetime.now()
                        ob_last_row_id = self.database.cursor.lastrowid
                        sql_str = """INSERT IGNORE INTO crypto_test.order_book_live(order_book_id,ut)
                                    VALUES(%s,"%s")
                                    """%(ob_last_row_id,ut)

                        self.database.cursor.execute(sql_str)
                        try:
                            self.database.mydb.commit()
                        except:
                            self.database.mydb.rollback()



def main():
    """
    """

    PC = PopulateCryptoBitstamp()
    PC.populate_bitstamp_data()


if __name__ == "__main__":
    main()