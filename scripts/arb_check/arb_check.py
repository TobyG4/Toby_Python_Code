import pandas.io.sql as psql
import sys

import pandas.io.sql as psql

crypto_arbing_dir = os.getcwd().split('/crypto_db')[0] 
sys.path.append(crypto_arbing_dir)


class ArbCheck(object):
    """
    """
    def __init__(self):
        """
        """
        self.port = 3306
        self.host = "127.0.0.1"
        self.database_name = 'Crypto_Test'
        self.user = 'root'
        self.password = 'Crypto'
        self.database = DatabaseConnect(self.host, self.database_name, self.user, self.password, self.port)
        self.database.database_connect()
#         self.get_coinone_exchange_id()
#         self.crypto_currency_dict()

    def get_latest_exchange_rates(self):
        """
        """
        sql_str = """SELECT fer.crypto_currency_id AS exchange_currency_id,fer.crypto_currency_id2 AS base_currency_id,fer.exchange_rate,fer.server_time,fer.ut  
                    FROM Crypto_Test.fiat_exchange_rates fer
                    JOIN (SELECT crypto_currency_id,crypto_currency_id2,source_id,MAX(server_time) AS server_time
				        FROM Crypto_Test.fiat_exchange_rates 
				        GROUP BY crypto_currency_id,crypto_currency_id2,source_id) AS fer1
                    ON fer1.crypto_currency_id = fer.crypto_currency_id AND
                        fer1.crypto_currency_id2 = fer.crypto_currency_id2 AND
                        fer.source_id = fer1.source_id AND
                        fer.server_time = fer1.server_time"""

        results = psql.read_sql(sql_str, con=self.database.mydb)
        latest_exchange_rates = results
        self.latest_exchange_rates = latest_exchange_rates.drop_duplicates(['exchange_rate', 'server_time', 'exchange_currency_id'])

    
    def get_latest_order_book(self):
        """
        """
        #get min sell price
        sql_str = """SELECT MIN(price) AS min_sell_price,asset_pairs_lookup_id,server_time
                    FROM crypto_test.order_book ob
                    INNER JOIN crypto_test.asset_pairs_lookup apl ON apl.id = ob.asset_pairs_lookup_id
                    WHERE order_type_id = 2 AND tradeable = 1
                    GROUP BY asset_pairs_lookup_id,server_time
                    """
                        
        ask_results = psql.read_sql(sql_str,con = self.database.mydb)
        #get most recent order_time
        #get index of rows with max server time, i.e most recent data
        idx = ask_results.groupby(['asset_pairs_lookup_id'])['server_time'].transform(max) == ask_results['server_time']
        #get df of all max server time
        grouped_ask = ask_results[idx]
        
        #get max buy price
        sql_str = """SELECT MAX(price) AS max_buy_price,asset_pairs_lookup_id,server_time
                        FROM crypto_test.order_book ob
                        INNER JOIN crypto_test.asset_pairs_lookup apl ON apl.id = ob.asset_pairs_lookup_id
                        WHERE order_type_id = 1 AND tradeable = 1
                        GROUP BY asset_pairs_lookup_id,server_time"""
        
        bid_results = psql.read_sql(sql_str,con = self.database.mydb)
        idx = ask_results.groupby(['asset_pairs_lookup_id'])['server_time'].transform(max) == ask_results['server_time']
        grouped_bid = bid_results[idx]
        #merge together to get one df with sell and buy price
        merged_bid_ask = grouped_ask.merge(grouped_bid,on = ['asset_pairs_lookup_id','server_time'],how = 'inner')
        self.recent_data = merged_bid_ask

    
    def select_asset_pairs_lookup(self):
        """code to determine all the possible tradeable asset_pairs, and test whether there is a price difference
        i.e usdbtc -> btceth -> ethusd
        """
        sql_str = """SELECT apl.id AS asset_pairs_lookup_id, ap.name AS pair,asset_pairs_id,e.name AS exchange,crypto_currency_id,crypto_currency_id2,cc.fiat AS ccid2_fiat
                     FROM crypto_test.asset_pairs_lookup apl
                    INNER JOIN crypto_test.asset_pairs ap On ap.id = apl.asset_pairs_id
                    INNER JOIN crypto_test.crypto_currency cc ON cc.id = ap.crypto_currency_id2
                    INNER JOIN crypto_test.exchange e ON e.id = apl.exchange_id
                    WHERE tradeable = 1 """
        
        asset_pairs_info = psql.read_sql(sql_str,con = self.database.mydb)
        crypto_links = {}
        for ind,row in asset_pairs_info.T.iteritems():

            asset_pairs_lookup_id, crypto_currency_id, crypto_currency_id2 = row['asset_pairs_lookup_id'],row['crypto_currency_id'],row['crypto_currency_id2']

            if not crypto_currency_id in crypto_links:
                crypto_links[crypto_currency_id] = {crypto_currency_id2:asset_pairs_lookup_id}
            else:
                crypto_links[crypto_currency_id][crypto_currency_id2] = asset_pairs_lookup_id

            if not crypto_currency_id2 in crypto_links:
                crypto_links[crypto_currency_id2] = {crypto_currency_id:asset_pairs_lookup_id}
            else:
                crypto_links[crypto_currency_id2][crypto_currency_id] = asset_pairs_lookup_id

        self.crypto_links = crypto_links
        #merge data buy/sell price, with asset_pairs_info
        order_book_merged = self.recent_data.merge(asset_pairs_info[['asset_pairs_lookup_id','pair','exchange','crypto_currency_id','crypto_currency_id2','ccid2_fiat']],on = 'asset_pairs_lookup_id',how ='inner' )
        self.order_book_merged = order_book_merged
            
    def arb_check(self):
        """
        """
        #1) start with asset_lookup_pairs xrpusd kraken = 14
        #base_lapc_id = 14
        #base_crypto1_id = 19
        #base_crpyto2_id = 25
        #2)Find asset pairs with, crypto1 (first crypto) = ripple_id = 19
        #lookup_asset_pairs_crypto1 = [46,48,62]
        #3) lapc1 = lookup_asset_pairs_crypto1
        #3.1) is crypto2 of these asset_pairs FIAT i.e USD,KRW etc. xrpusd -> xrpkrw
        #3.2) crypto non fiat ex. xrpusd -> xrpbtc -> btckrw
        #3.3) xrpusd -> xrpbtc -> btceth -> ethusd


        self.get_latest_exchange_rates()
        # merge order book with exchange rates
        merged_orderbook_exchange_rates = self.order_book_merged.merge(self.latest_exchange_rates[['exchange_currency_id', 'exchange_rate']],
                                                                left_on=['crypto_currency_id2'], right_on=['exchange_currency_id'], how='left')

        merged_orderbook_exchange_rates['min_sell_price_usd'] = merged_orderbook_exchange_rates['min_sell_price']/merged_orderbook_exchange_rates['exchange_rate']
        merged_orderbook_exchange_rates['max_buy_price_usd'] = merged_orderbook_exchange_rates['max_buy_price']/merged_orderbook_exchange_rates['exchange_rate']
        #create a dict to store all the min and mac arbs i.e x = {'MAX':{'bchusd':2.2},'MIN':{'ddddd':3.3}}

        # arb_perc_diff_dict={'max_diff':{},'min_diff':{}}
        arb_perc_diff_dict = {}

        asset_pairs_dict = dict(zip(self.order_book_merged.asset_pairs_lookup_id, self.order_book_merged.pair))

        for asset_pairs_lookup_id in asset_pairs_dict:
            pair_name = asset_pairs_dict[asset_pairs_lookup_id]
            # print '------------------------------------------------------------------------------------------'

            base_lapc_id = asset_pairs_lookup_id

            moer = merged_orderbook_exchange_rates.copy()
            base_crypto1_id = moer['crypto_currency_id'][moer['asset_pairs_lookup_id'] == base_lapc_id].iloc[0]
            base_crypto2_id = moer['crypto_currency_id2'][moer['asset_pairs_lookup_id'] == base_lapc_id].iloc[0]

            #If the pair is non fiat i.e ETHBTC then we don't want to convert the price to usd
            if moer['ccid2_fiat'][moer['asset_pairs_lookup_id'] == base_lapc_id].iloc[0] == 1:
                base_lapc_buy_price = moer['max_buy_price_usd'][moer['asset_pairs_lookup_id'] == base_lapc_id].iloc[0]
                base_lapc_buy_price_list = [[base_lapc_buy_price,'']]
            else:
                lapc_buy_price = moer['max_buy_price'][moer['asset_pairs_lookup_id'] == base_lapc_id].iloc[0]
                # i.e ETHBTC base_lapc_buy_price = 0.04. Then compare sell price for all BTC,and use that to compare with
                base_crypto2_fiat_sell_price = moer[['pair','min_sell_price_usd']][(moer['crypto_currency_id']==base_crypto2_id)&(moer['ccid2_fiat']==1)]

                #need to choose max and min values, because could be big differnce. i.e xrpeth , eth price could be between 280-299, change the diff_per greatly
                max_value_df = base_crypto2_fiat_sell_price.loc[base_crypto2_fiat_sell_price['min_sell_price_usd'].idxmax()]
                max_value,max_sell_pair = max_value_df['min_sell_price_usd'],max_value_df['pair']
                min_value_df = base_crypto2_fiat_sell_price.loc[base_crypto2_fiat_sell_price['min_sell_price_usd'].idxmin()]
                min_value, min_sell_pair = min_value_df['min_sell_price_usd'], min_value_df['pair']

                base_lapc_buy_price_max = lapc_buy_price*max_value
                base_lapc_buy_price_min = lapc_buy_price*min_value
                base_lapc_buy_price_list = [[base_lapc_buy_price_max,max_sell_pair],[base_lapc_buy_price_min,min_sell_pair]]


            # print asset_pairs_lookup_id, pair_name, base_lapc_buy_price
            for base_lapc_buy_price_info in base_lapc_buy_price_list:
                base_lapc_buy_price = base_lapc_buy_price_info[0]
                base_fiat_for_alt_pairs = base_lapc_buy_price_info[1]


                moer[pair_name] = base_lapc_buy_price
                # find other asset_pairs with base_crypto_id1 = crypto_id1, not including our base_lapc_id
                lapc_linked = moer[['asset_pairs_lookup_id','ccid2_fiat']][((moer['crypto_currency_id']==base_crypto1_id)|(moer['crypto_currency_id2']==base_crypto1_id))
                                                                           &(moer['asset_pairs_lookup_id'] != base_lapc_id)]

                # 3.1) compare lapc_fiat sell price (converted to USD) against original price. i.e xrpusd ad xrpkrw are fiat pairs
                lapc_fiat = lapc_linked['asset_pairs_lookup_id'][lapc_linked['ccid2_fiat']==1]

                if not lapc_fiat.empty:
                    lapc_fiat_list = lapc_fiat.tolist()
                    fiat_compare = moer[moer['asset_pairs_lookup_id'].isin(lapc_fiat_list)]
                    fiat_compare.loc[:,'diff'] = fiat_compare.loc[:,'max_buy_price_usd'] - base_lapc_buy_price
                    fiat_compare.loc[:, 'diff_per'] = fiat_compare.loc[:, 'diff']/base_lapc_buy_price

                    for ind,row in fiat_compare.T.iteritems():
                        arb_perc_diff_dict[(base_lapc_id, row['asset_pairs_lookup_id'])] = [((
                                    pair_name, base_crypto1_id,base_crypto2_id), (row['pair'],row['crypto_currency_id'],row['crypto_currency_id2'])),row['diff_per']]

                lapc_non_fiat = lapc_linked['asset_pairs_lookup_id'][lapc_linked['ccid2_fiat'] != 1]
                if not lapc_non_fiat.empty:
                    lapc_non_fiat_list = lapc_non_fiat.tolist()
                    #look at lapc_non_fiat i.e xrpbtc 46
                    order_book_copy = self.order_book_merged.copy()
                    for lapc_non_fiat_id in lapc_non_fiat_list:

                        #asset_pairs_info = api
                        asset_pair_info = order_book_copy[order_book_copy['asset_pairs_lookup_id']==lapc_non_fiat_id]
                        new_asset_pair_name = asset_pair_info['pair'].iloc[0]
                        # print pair_name, new_asset_pair_name

                        lapc_crypto_id,lapc_crypto2_id =  asset_pair_info['crypto_currency_id'].iloc[0],asset_pair_info['crypto_currency_id2'].iloc[0]
                        lapc_id_2_sell_price = asset_pair_info['min_sell_price'].iloc[0]

                        #now search for lookup_asset_pairs with crypto_currency_id = crypto_currency_id2(of asset pars in non_fiat_compare)
                        if base_crypto1_id == lapc_crypto_id:
                            asset_pairs_btc_fiat = moer[(moer['crypto_currency_id'] == lapc_crypto2_id) & (moer['ccid2_fiat'] == 1)]
                        else:
                            asset_pairs_btc_fiat = moer[(moer['crypto_currency_id'] == lapc_crypto_id) & (moer['ccid2_fiat'] == 1)]

                        if asset_pairs_btc_fiat.empty:
                            #need more work here
                            continue

                        asset_pairs_btc_fiat.loc[:,new_asset_pair_name] = lapc_id_2_sell_price

                        # two examples 1) EOSETH EOSBTC BTCUSD  2)
                        if base_crypto1_id == lapc_crypto_id:
                            asset_pairs_btc_fiat.loc[:,'sold_fiat'] = asset_pairs_btc_fiat.loc[:,'min_sell_price_usd']*asset_pairs_btc_fiat.loc[:,new_asset_pair_name]
                        else:
                            asset_pairs_btc_fiat.loc[:,'sold_fiat'] = asset_pairs_btc_fiat.loc[:,'min_sell_price_usd']/asset_pairs_btc_fiat.loc[:,new_asset_pair_name]

                        asset_pairs_btc_fiat.loc[:,'diff'] = asset_pairs_btc_fiat.loc[:,'sold_fiat'] - base_lapc_buy_price
                        asset_pairs_btc_fiat.loc[:, 'diff_per'] = asset_pairs_btc_fiat.loc[:, 'diff'] / base_lapc_buy_price

                        #If length of rows is greater than 1
                        # if asset_pairs_btc_fiat.shape[0] > 1:
                        #     max_diff_per1 = asset_pairs_btc_fiat.loc[asset_pairs_btc_fiat['diff_per'].idxmax()]
                        #     min_diff_per1 = asset_pairs_btc_fiat.loc[asset_pairs_btc_fiat['diff_per'].idxmin()]

                        for ind, row in asset_pairs_btc_fiat.T.iteritems():
                            arb_perc_diff_dict[(base_lapc_id,lapc_non_fiat_id,row['asset_pairs_lookup_id'])]  =   [((pair_name, base_crypto1_id, base_crypto2_id, base_fiat_for_alt_pairs),(new_asset_pair_name,lapc_crypto_id,lapc_crypto2_id),
                                                (row['pair'], row['crypto_currency_id'], row['crypto_currency_id2'])),row['diff_per']]


                            # arb_perc_diff_dict['max_diff'][(pair_name,new_asset_pair_name,max_diff_per1['pair'])] = max_diff_per1['diff_per']
                        # arb_perc_diff_dict['min_diff'][(pair_name,new_asset_pair_name,min_diff_per1['pair'])] = min_diff_per1['diff_per']

        print '************************************************************************************'
        print 'diff sorted'

        full_circle_arb = {}

        for key, value in sorted(arb_perc_diff_dict.iteritems(), key=lambda (k, v): (v, k)):
            #can we get from end crypto to start crypto i.e (u'BTCJPY', u'ETHBTC', u'ETHCAD') can we go from CAD -> JPY
            end_crypto, start_crypto = value[0][0][2],value[0][-1][2]
            possible_routes = []
            link_list = self.crypto_links[start_crypto]
            if end_crypto in link_list:

                #needs more work in her as well, have to compare this to original comparison above

                possible_routes.append([link_list[end_crypto]])

            for i in link_list:

                asset_pair_id = link_list[i]
                link_list2 = self.crypto_links[i]
                for j in link_list2:
                    if j == end_crypto:
                        #success we've found a route from start_crypto to end_crypto
                        if (asset_pair_id,link_list2[j]) in arb_perc_diff_dict:
                            return_diff_per = arb_perc_diff_dict[(59, 6)][-1]
                            # get total percentage of whole trade, start to finish
                            total_arb_perc = return_diff_per+value[-1]
                            possible_routes.append([(asset_pair_id,link_list2[j]),return_diff_per,total_arb_perc])
                            full_circle_tuple = key + (asset_pair_id,link_list2[j])
                            full_circle_arb[full_circle_tuple] = total_arb_perc

                        else:
                            possible_routes.append([(asset_pair_id, link_list2[j]),'Havent calculated $'])


            #print "%s: %s" % (key, value), possible_routes
        eth_xrp = [14, 46, 48, 62, 4, 6, 8, 9, 16, 18, 21, 24, 29, 37, 44, 49, 59]
        for key, value in sorted(full_circle_arb.iteritems(), key=lambda (k, v): (v, k)):

            # if len(set(key)&set(eth_xrp))==len(key):
            print """%s: %s""" % (key, value),"\n"

    def xrp_arbs(self):
        """Just shows xrp arbs
        1) Simple one way between excnhages
            - What is liquidity? i.e it reads balance 10,000 euro, and analyses order book to see what price you could get it on at
            - Is price free falling?
        2) Can we get back somehow, links into code above
        3) Writes into a signal group,through api
        """


def main():
    """
    """
    AC = ArbCheck()
    AC.get_latest_order_book()
    AC.select_asset_pairs_lookup()
    AC.arb_check()
    
if __name__=="__main__":
    main()