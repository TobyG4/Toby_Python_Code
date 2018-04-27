import json
import os
import sys

import pandas.io.sql as psql
import requests

crypto_tools_dir = os.getcwd().split('/scripts/')[0] + '/scripts/'
sys.path.append(crypto_tools_dir)

from crypto_tools import *


class PopulateKraken(object):
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
        self.get_kraken_exchange_id()
        self.crypto_currency_dict()

    def get_kraken_exchange_id(self):
        """
        """
        sql_str = """SELECT id FROM crypto_test.exchange
                    WHERE name = 'kraken' """
        
        results = psql.read_sql(sql_str,con = self.database.mydb)
        self.exchange_id = results['id'].loc[0]
        
        
    def crypto_currency_dict(self):
        """
        """
        sql_str = """SELECT id,altname FROM crypto_test.crypto_currency"""
        
        results = psql.read_sql(sql_str,con = self.database.mydb)
        crypto_db_dict = {}
        
        for ind,row in results.T.iteritems():
            altname = row['altname']
            crypto_db_dict[altname] = row['id']
        
        self.crypto_db_dict = crypto_db_dict
    
    def asset_pairs_dict(self):
        """
        """
        sql_str = """SELECT id,name FROM crypto_test.asset_pairs"""
        
        results = psql.read_sql(sql_str,con = self.database.mydb)
        asset_pairs_db_dict = {}
        
        for ind,row in results.T.iteritems():
            name = row['name']
            asset_pairs_db_dict[name] = row['id']
        
        print (asset_pairs_db_dict)
        self.asset_pairs_db_dict = asset_pairs_db_dict
            

    def get_kraken_lookup_cryptos(self):
        """
        """
        #asset_pairs_json = requests.get("https://api.kraken.com/0/public/AssetPairs")
        
        crypto_json = requests.get("https://api.kraken.com/0/public/Assets")
        crypto_json_string = crypto_json.text
        crypto_json_dictionary = json.loads(crypto_json_string)
        result = crypto_json_dictionary['result']
        
        for i in result:
            
            name = result[i]['altname']
            exchange_id = 1
            ut = datetime.now()
            
            try:
                crypto_currency_id = self.crypto_db_dict[i]
                
            except:
                crypto_currency_id ='NULL'
            
            sql_str = """INSERT INTO crypto_test.crypto_currency_lookup(name,crypto_currency_id,exchange_id,ut)
                                    VALUES('%s',%s,%s,"%s")
                                    """%(name,crypto_currency_id,exchange_id,ut)
            

            self.database.cursor.execute(sql_str)
            try:
                self.database.mydb.commit()
            except:
                self.database.mydb.rollback()
    
    
    
    def get_kraken_tradeable_assets(self):
        """
        """
        self.asset_pairs_dict()
        print (self.asset_pairs_dict)
        
        asset_pairs_json = requests.get("https://api.kraken.com/0/public/AssetPairs")
        
        asset_pairs_json_string = asset_pairs_json.text
        
        asset_pairs_json_dictionary = json.loads(asset_pairs_json_string)
        
        result = asset_pairs_json_dictionary['result']
        
        x = 0 
        for i in result:
            
            new_name = i.replace('.d','')
            
            ut = datetime.now()
            sql_str = """INSERT IGNORE INTO crypto_test.asset_pairs_lookup(name,asset_pairs_id,exchange_id,tradeable,ut)
                                    VALUES('%s',%s,1,1,"%s")
                                    """%(new_name,'NULL',ut)
                                                
            self.database.cursor.execute(sql_str)
            try:
                self.database.mydb.commit()
            except:
                self.database.mydb.rollback()
            
            x = x + 1
        
    
    def populate_asset_pairs(self):
        """
        """
        asset_pairs_list = ["BTCCAD","XMRUSD","BTCEUR","ETHBTC","BTCGBP","ETHEUR","XMRBTC","MLNETH","ETHJPY","ZECEUR","REPBTC","GNOBTC","BTCJPY","XRPUSD","LTCUSD",
"REPETH","BTCGBP","ETHZUSD","EOSBTC","ETHJPY","ETHCAD","ETCBTC","ZECUSD","ETHGBP","BCHEUR","XDGBTC","BTCEUR","LTCEUR","ETCETH","ETHGBP","REPEUR","BTCCAD","LTCBTC","BTCJPY",
"XMREUR","BTCUSD","GNOETH","ETHCAD","DASHBTC","XLMBTC","ETCEUR","MLNBTC","BCHUSD","ICNETH","ETHBTC","XRPBTC","ETHUSD","XRPEUR","EOSETH","DASHEUR",
"ICNBTC","ETCUSD","ETHEUR","ZECBTC","DASHUSD","BTCUSD","BCHBTC","USDTUSD"]
        
        for asset_pair in asset_pairs_list:
            
            if 'DASH' in asset_pair:
                asset1 = 'DASH'
                asset2 = asset_pair[-3:]
            else:
                asset1 = asset_pair[:3]
                asset2 = asset_pair[-3:]
            
            try:
                cryptoid1 = self.crypto_db_dict[asset1]
                cryptoid2 = self.crypto_db_dict[asset2]
            except:
                print (asset_pair, 'not in crypto_crrency table')
                continue
            
            ut = datetime.now()
            sql_str = """INSERT IGNORE INTO crypto_test.asset_pairs(name,crypto_currency_id,crypto_currency_id2,ut)
                                    VALUES('%s',%s,%s,"%s")
                                    """%(asset_pair,cryptoid1,cryptoid2,ut)
            
            print (sql_str)
                                    
            self.database.cursor.execute(sql_str)
            try:
                self.database.mydb.commit()
            except:
                self.database.mydb.rollback()
            
    
    def get_kraken_asset_pairs_lookup(self):
        """
        """
        sql_str = """SELECT apl.name,apl.id AS asset_pairs_lookup_id 
                    FROM crypto_test.asset_pairs_lookup apl
                    INNER JOIN crypto_test.exchange e ON e.id = apl.exchange_id
                    WHERE e.name = 'kraken'"""
        
        results = psql.read_sql(sql_str,con = self.database.mydb)
        asset_pairs_lookup_dict = {}
        self.asset_pairs_list = results['name'].tolist()
        self.asset_pairs_str = ','.join(self.asset_pairs_list)
        print (self.asset_pairs_str)
        
        for ind,row in results.T.iteritems():
            name = row['name']
            asset_pairs_lookup_dict[name] = row['asset_pairs_lookup_id']
    
        self.asset_pairs_lookup_dict = asset_pairs_lookup_dict
    
    
    def get_server_time(self):
        """get kraken sever time
        """
        url = "https://api.kraken.com/0/public/Time"
        server_time_request = requests.get(url)
        server_time_text = server_time_request.text
        server_time_json = json.loads(server_time_text)
        result = server_time_json['result']
        server_time_unixtime = result['unixtime']
        server_time = datetime.fromtimestamp(int(server_time_unixtime)).strftime('%Y-%m-%d %H:%M:%S')
        self.server_time = server_time
        
    def populate_order_book(self):
        """
        """
        self.get_server_time()
        self.get_kraken_asset_pairs_lookup()
        
        for kraken_asset_pair in self.asset_pairs_list:
            
            print (kraken_asset_pair)
            url = "https://api.kraken.com/0/public/Depth?pair=%s"%(kraken_asset_pair)
        
            try:
                order_book_json = requests.get(url)
            except:
                print (i, 'no order book')
        
            #order_book = open('/Users/toby/git/toby_test/crypto_arbing/crypto_db/populate_db/kraken_order_book.json')
            order_book = order_book_json.text
            
            order_book_json = json.loads(order_book)
            result = order_book_json['result']
            
            bids = result[kraken_asset_pair]['bids']
            asks = result[kraken_asset_pair]['asks']
            
            asset_pairs_lookup_id = self.asset_pairs_lookup_dict[kraken_asset_pair]
            bid_ask_list = [[1,bids],[2,asks]]
            
            for order_type in bid_ask_list:
                
                order_type_id = order_type[0]
                                
                for order in order_type[1]:
                                        
                    price = order[0]
                    quantity = order[1]
                    order_time = datetime.fromtimestamp(int(order[2])).strftime('%Y-%m-%d %H:%M:%S')
                                    
                    #need to remove trailing zeros before and after decimal
                    new_price = '{0:g}'.format(float(price))
                    new_quantity = '{0:g}'.format(float(quantity))
                    
                    ut = datetime.now()
                                           
                    sql_str = """INSERT IGNORE INTO crypto_test.order_book(asset_pairs_lookup_id,order_type_id,price,quantity,order_time,server_time,ut)
                                            VALUES(%s,%s,%s,%s,"%s","%s","%s")
                                            """%(asset_pairs_lookup_id,order_type_id,float(new_price),float(quantity),order_time,self.server_time,ut)
                    
                    self.database.cursor.execute(sql_str)
                    try:
                        self.database.mydb.commit()
                    except:
                        self.database.mydb.rollback()
                     
            
def main():
    """
    """
    
    PC = PopulateKraken()
    #PC.get_kraken_tradeable_assets()
    #PC.get_kraken_lookup_cryptos()
    #PC.populate_asset_pairs()
    PC.populate_order_book()
    
if __name__=="__main__":
    main()