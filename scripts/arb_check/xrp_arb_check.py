import os
import sys
import pdb

import pandas.io.sql as psql

crypto_tools_dir = os.getcwd().split('/scripts/')[0] + '/scripts/'
sys.path.append(crypto_tools_dir)

from crypto_tools import *
from update_exchange_rates import *

class ArbCheck(object):
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

        self.smtp = 'smtp.gmail.com'
        self.smtpport = 587
        self.emailuser = 'xrparb666@gmail.com'
        self.emailpassword = 'R1i9p1p1l9e0$'

        FER = FiatExchangeRates()
        FER.get_exchange_rate()

    def send_email(self,email_list):
        """
        """
        self.sendemail = SendEmail(self.smtp, self.smtpport, self.emailuser, self.emailpassword)

        exchange_rates_for_email = self.latest_exchange_rates[['currency_name','exchange_rate']]

        header = 'Xrp Arb Update'
        html_str = """  <style type="text/css">
        .tg  {border-collapse:collapse;border-spacing:0;border-color:#aabcfe;}
        .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#aabcfe;color:#669;background-color:#e8edff;}
        .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#aabcfe;color:#039;background-color:#b9c9fe;}
        .tg .tg-uliv{background-color:#81ff80;vertical-align:top}
        .tg .tg-yw4l{vertical-align:top}
        </style>
         <b>Hi All,e
         
         IMPORTANT: Check both server_time to see if recent (time is GMT).
                    Check exchange rates are correct
                    
        Feedback is encouraged, any ideas let me know, also if you want to add other exchanges/crypto etc </b> 
        <table class="tg">
          <tr>
            <th class="tg-uliv">Pair1</th>
            <th class="tg-uliv">Pair2</th>
            <th class="tg-uliv">E1</th>
            <th class="tg-uliv">E2</th>
            <th class="tg-uliv">E1Price<br></th>
            <th class="tg-uliv">E1Price$</th>
            <th class="tg-uliv">E2Price</th>
            <th class="tg-uliv">E2Price$</th>
            <th class="tg-uliv">%diff</th>
            <th class="tg-uliv">E1Server_Time</th>
            <th class="tg-uliv">E2Server_Time</th>
          </tr>"""

        for i in email_list:
            html_str = html_str + '<tr>'
            z = 0
            for x in i:
                if z == 8:
                    html_str = html_str + '<th class="tg-uliv">%s</th>'%(x)
                else:
                    html_str = html_str + '<th class="tg-yw4l">%s</th>' % (x)
                z = z + 1
            html_str = html_str + '</tr>'

        html_str = html_str + "</table>"

        #put exchange rate into html
        exchange_rates_for_email = self.latest_exchange_rates[['currency_name', 'exchange_rate']]

        html_str2 = """<table class="tg">
          <tr>
            <th class="tg-uliv">Currency</th>
            <th class="tg-uliv">Exchange_Rate USD</th>
          </tr>
        """

        for ind,row in exchange_rates_for_email.T.iteritems():
            html_str2 = html_str2 + """<tr>
            <th class="tg-uliv">%s</th>
            <th class="tg-uliv">%s</th>
          </tr>
            """%(row['currency_name'],row['exchange_rate'])

        html_str2 = html_str2 + "</table>"

        html_str_end = html_str + html_str2

        html_str_end.encode('utf-8')
        self.sendemail.send_html_email(['toby_green4@hotmail.co.uk','sophiehyeon@gmail.com','Nitas711@gmail.com','rory_green@hotmail.co.uk'], header, html_str_end)

        #'sophiehyeon@gmail.com','Nitas711@gmail.com','rory_green@hotmail.co.uk'
    def get_latest_exchange_rates(self):
        """
        """
        sql_str = """SELECT cc.name AS currency_name,fer.crypto_currency_id AS exchange_currency_id,fer.crypto_currency_id2 AS base_currency_id,fer.exchange_rate,fer.server_time,fer.ut  
                    FROM crypto_test.fiat_exchange_rates fer
                    INNER JOIN crypto_test.crypto_currency cc ON cc.id = fer.crypto_currency_id
                    JOIN (SELECT crypto_currency_id,crypto_currency_id2,source_id,MAX(server_time) AS server_time
				        FROM crypto_test.fiat_exchange_rates 
				        GROUP BY crypto_currency_id,crypto_currency_id2,source_id) AS fer1
                    ON fer1.crypto_currency_id = fer.crypto_currency_id AND
                        fer1.crypto_currency_id2 = fer.crypto_currency_id2 AND
                        fer.source_id = fer1.source_id AND
                        fer.server_time = fer1.server_time"""

        results = psql.read_sql(sql_str, con=self.database.mydb)
        latest_exchange_rates = results
        self.latest_exchange_rates = latest_exchange_rates.drop_duplicates(
            ['exchange_rate', 'server_time', 'exchange_currency_id'])


    def get_latest_order_book(self):
        """
        """
        xrp_pair_tuple = str(tuple(self.xrp_asset_pairs_lookup_id_list))
        pdb.set_trace()
        # get min sell price
        sql_str = """SELECT MIN(price) AS min_sell_price,asset_pairs_lookup_id,server_time
                    FROM crypto_test.order_book ob
                    INNER JOIN crypto_test.asset_pairs_lookup apl ON apl.id = ob.asset_pairs_lookup_id
                    WHERE order_type_id = 2 AND tradeable = 1 AND apl.id in %s
                    GROUP BY asset_pairs_lookup_id,server_time
                    """%(xrp_pair_tuple)

        print (sql_str)
        ask_results = psql.read_sql(sql_str, con=self.database.mydb)
        # get most recent order_time
        # get index of rows with max server time, i.e most recent data
        idx = ask_results.groupby(['asset_pairs_lookup_id'])['server_time'].transform(max) == ask_results['server_time']
        # get df of all max server time

        grouped_ask = ask_results[idx]

        # get max buy price
        sql_str = """SELECT MAX(price) AS max_buy_price,asset_pairs_lookup_id,server_time
                        FROM crypto_test.order_book ob
                        INNER JOIN crypto_test.asset_pairs_lookup apl ON apl.id = ob.asset_pairs_lookup_id
                        WHERE order_type_id = 1 AND tradeable = 1 AND apl.id in %s
                        GROUP BY asset_pairs_lookup_id,server_time"""%(xrp_pair_tuple)

        bid_results = psql.read_sql(sql_str, con=self.database.mydb)
        idx = bid_results.groupby(['asset_pairs_lookup_id'])['server_time'].transform(max) == bid_results['server_time']
        grouped_bid = bid_results[idx]
        # merge together to get one df with sell and buy price
        merged_bid_ask = grouped_ask.merge(grouped_bid, on=['asset_pairs_lookup_id', 'server_time'], how='inner')
        self.recent_data = merged_bid_ask

    def select_asset_pairs_lookup(self):
        """selct asset_pairs which have xrp in it
        """
        sql_str = """SELECT apl.id AS asset_pairs_lookup_id, ap.name AS pair,asset_pairs_id,e.name AS exchange,crypto_currency_id,crypto_currency_id2,cc.fiat AS ccid2_fiat
                     FROM crypto_test.asset_pairs_lookup apl
                    INNER JOIN crypto_test.asset_pairs ap On ap.id = apl.asset_pairs_id
                    INNER JOIN crypto_test.crypto_currency cc ON cc.id = ap.crypto_currency_id2
                    INNER JOIN crypto_test.exchange e ON e.id = apl.exchange_id
                    WHERE tradeable = 1 AND(ap.crypto_currency_id = 19 or ap.crypto_currency_id2 = 19)
                    """

        asset_pairs_info = psql.read_sql(sql_str, con=self.database.mydb)
        self.xrp_asset_pairs_lookup_id_list = asset_pairs_info['asset_pairs_lookup_id'].tolist()
        # crypto_links = {}
        # for ind, row in asset_pairs_info.T.iteritems():
        #
        #     asset_pairs_lookup_id, crypto_currency_id, crypto_currency_id2 = row['asset_pairs_lookup_id'], row[
        #         'crypto_currency_id'], row['crypto_currency_id2']
        #
        #     if not crypto_currency_id in crypto_links:
        #         crypto_links[crypto_currency_id] = {crypto_currency_id2: asset_pairs_lookup_id}
        #     else:
        #         crypto_links[crypto_currency_id][crypto_currency_id2] = asset_pairs_lookup_id
        #
        #     if not crypto_currency_id2 in crypto_links:
        #         crypto_links[crypto_currency_id2] = {crypto_currency_id: asset_pairs_lookup_id}
        #     else:
        #         crypto_links[crypto_currency_id2][crypto_currency_id] = asset_pairs_lookup_id
        #
        # self.crypto_links = crypto_links
        # merge data buy/sell price, with asset_pairs_info
        self.get_latest_order_book()

        order_book_merged = self.recent_data.merge(asset_pairs_info[['asset_pairs_lookup_id', 'pair', 'exchange',
                                                                     'crypto_currency_id', 'crypto_currency_id2',
                                                                     'ccid2_fiat']], on='asset_pairs_lookup_id',
                                                   how='inner')

        self.order_book_merged = order_book_merged


    def arb_check(self):
        """
        """
        self.get_latest_exchange_rates()
        # merge order book with exchange rates
        merged_orderbook_exchange_rates = self.order_book_merged.merge(self.latest_exchange_rates[['exchange_currency_id', 'exchange_rate']],
                                                                left_on=['crypto_currency_id2'], right_on=['exchange_currency_id'], how='left')


        merged_orderbook_exchange_rates['min_sell_price_usd'] = merged_orderbook_exchange_rates['min_sell_price']/merged_orderbook_exchange_rates['exchange_rate']
        merged_orderbook_exchange_rates['max_buy_price_usd'] = merged_orderbook_exchange_rates['max_buy_price']/merged_orderbook_exchange_rates['exchange_rate']

        #moer = merged_orderbook_exchange_rates
        moer = merged_orderbook_exchange_rates.copy()
        only_fiat_moer = moer[moer['ccid2_fiat']==1]
        arb_perc_email_dict = {}

        #need to include exchange_rates = only_fiat_moer[[,,'exchange_rate']]

        for ind, row in only_fiat_moer.T.iteritems():

            asset_pairs_lookup_id1, pair1,exchange1 = row['asset_pairs_lookup_id'],row['pair'],row['exchange']
            buy_price = row['max_buy_price_usd']


            to_compare = only_fiat_moer[only_fiat_moer['asset_pairs_lookup_id']!=asset_pairs_lookup_id1]


            for ind2,row2 in to_compare.T.iteritems():

                pair2,exchange2,sell_price = row2['pair'],row2['exchange'],row2['min_sell_price_usd']
                diff = float(buy_price) - float(sell_price)
                perc_diff = (diff/buy_price)*100

                #print ('Buy %s on %s and sell %s on %s = %s difference'%(pair1,exchange1,pair2,exchange2,perc_diff))
                arb_email_info = [pair1,pair2,exchange1,exchange2,"{0:.3f}".format(row['max_buy_price']),"{0:.3f}".format(row['max_buy_price_usd']),
                                   "{0:.3f}".format(row2['min_sell_price']),"{0:.3f}".format(row2['min_sell_price_usd']),"{0:.3f}".format(perc_diff),
                                   row['server_time'],row2['server_time']]

                #put in a dict to sort by percentage diff, for html in email. High to low.
                arb_perc_email_dict[tuple(arb_email_info)] = perc_diff

        #sort by perc_diff
        email_list = []
        for key, value in sorted(arb_perc_email_dict.items(), key=lambda kv: (-kv[1], kv[0])):
            email_list.append(key)

        self.send_email(email_list)

def main():
    """
    """
    AC = ArbCheck()
    AC.select_asset_pairs_lookup()
    AC.arb_check()


if __name__ == "__main__":
    main()