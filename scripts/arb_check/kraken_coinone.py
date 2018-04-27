#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Kraken Ticker
<pair_name> = pair name
    a = ask array(<price>, <whole lot volume>, <lot volume>),
    b = bid array(<price>, <whole lot volume>, <lot volume>),
    c = last trade closed array(<price>, <lot volume>),
    v = volume array(<today>, <last 24 hours>),
    p = volume weighted average price array(<today>, <last 24 hours>),
    t = number of trades array(<today>, <last 24 hours>),
    l = low array(<today>, <last 24 hours>),
    h = high array(<today>, <last 24 hours>),
    o = today's opening price"""

from datetime import datetime
from urllib2 import urlopen
import requests
import json
from pprint import pprint
import pdb
import pandas as pd
from datetime import datetime

class CryptoArbing(object):
    """
    """
    def __init__(self):
        """
        """
        
    def kraken_arbing_strategy(self):
        """
        """
        "1) buy coin and sell for other fiat currency"
        "2) buy coin,sell for other crypto"
        "3) buy coin,sell for other crypto, sell for fiat "
        
    def kraken_arbing_strategy2(self):
        """
        """
        eth_trading_list = [""]
        
        
    def get_kraken_tradeable_asset_pairs(self):
        """
        """
        asset_pairs_json = requests.get("https://api.kraken.com/0/public/AssetPairs")
        
        asset_pairs_json_string = asset_pairs_json.text
        
        asset_pairs_dictionary = json.loads(asset_pairs_json_string)
        
        result = asset_pairs_dictionary['result']
        
        asset_pairs_string = ""
        for i in result:
            pair = '%s,'%(i)
            asset_pairs_string = asset_pairs_string + pair
        
        'remove last comma from string'
        self.asset_pairs_string = asset_pairs_string[:-1]
        self.kraken_ripple_ticker()
        
        
        """XXBTZCAD,XXMRZUSD,XXBTZEUR.d,XETHXXBT,XXBTZGBP.d,XETHZEUR,XXMRXXBT,XMLNXETH,XETHZJPY,
        XZECZEUR,XREPXXBT,GNOXBT,XXBTZJPY.d,XXRPZUSD,XLTCZUSD,XREPXETH,XXBTZGBP,XETHZUSD,EOSXBT,
        XETHZJPY.d,XETHZCAD,XETCXXBT,XZECZUSD,XETHZGBP,BCHEUR,XXDGXXBT,XXBTZEUR,XLTCZEUR,XETCXETH,
        XETHZGBP.d,XREPZEUR,XXBTZCAD.d,XLTCXXBT,XXBTZJPY,XXMRZEUR,XXBTZUSD.d,GNOETH,XETHZCAD.d,
        DASHXBT,XXLMXXBT,XETCZEUR,XMLNXXBT,BCHUSD,XICNXETH,XETHXXBT.d,XXRPXXBT,XETHZUSD.d,XXRPZEUR,
        EOSETH,DASHEUR,XICNXXBT,XETCZUSD,XETHZEUR.d,XZECXXBT,DASHUSD,XXBTZUSD,BCHXBT,USDTZUSD
        """
        
        
        
    def kraken_btc_fiat_arb(self):
        """check to see if arbing opportunities with bitcoin and fiat
        <pair_name> = pair name
    a = ask array(<price>, <whole lot volume>, <lot volume>),
    b = bid array(<price>, <whole lot volume>, <lot volume>),
    c = last trade closed array(<price>, <lot volume>),
    v = volume array(<today>, <last 24 hours>),
    p = volume weighted average price array(<today>, <last 24 hours>),
    t = number of trades array(<today>, <last 24 hours>),
    l = low array(<today>, <last 24 hours>),
    h = high array(<today>, <last 24 hours>),
    o = today's opening price
    
        Code to chwck id thee is arb opportunity in Kraken, between BTC and fiat currencies.
        We use the order book to decide sell/buy opportunities for each tradeable pair.
        
        """
        print 'Check to see if there is arb opportunities within Kraken, between BTC and fiat curencies.'
        
        btc_fiat = "XXBTZEUR,XXBTZGBP,XXBTZJPY,XXBTZUSD"
        eth_fiat = "XETHZEUR,XETHZGBP,XETHZJPY,XETHZUSD"
        xrp_fiat = "XXRPZEUR,XXRPZUSD"
        
        btc_fiat_list = ['XXBTZEUR','XXBTZGBP','XXBTZJPY','XXBTZUSD']
        eth_fiat_list = ['XETHZEUR','XETHZGBP','XETHZJPY','XETHZUSD']
        xrp_fiat_list = ['XXRPZEUR','XXRPZUSD']
        
        
        eth_btc_list = [[btc_fiat,btc_fiat_list,'BTC'],[eth_fiat,eth_fiat_list,'ETH'],[xrp_fiat,xrp_fiat_list,'XRP']]
        
        for crpto_info in eth_btc_list:
            
            asset_str = crpto_info[0]
            asset_list = crpto_info[1]
            
            url_pairs = "https://api.kraken.com/0/public/Ticker?pair=%s"%(asset_str)
            ticker_info = requests.get(url_pairs)
            
            ticker_info_json = ticker_info.text
            
            ticker_info_dict = json.loads(ticker_info_json)
            
            result = ticker_info_dict['result']
                        
            self.get_exchange_rate()
            kraken_coin_lasttrade_price = {}
            for i in result:
                currency = i[-3:]
                
                if currency =='USD':
                    exchange_rate = 1
                else: 
                    exchange_rate = self.usd_exchange_rate_dict["rates"][currency]
                
                """look at order book, smallest sell order = buy_price, biggest buy order = sell_price"""
                local_price_buy = result[i]['a'][0]
                local_price_sell = result[i]['b'][0]
                
                buy_usd_convert = float(local_price_buy)/float(exchange_rate)
                sell_usd_convert = float(local_price_sell)/float(exchange_rate)
                
                kraken_coin_lasttrade_price[i] = local_price_buy,buy_usd_convert,local_price_sell,sell_usd_convert
#                 print currency,exchange_rate, local_price_buy,buy_usd_convert,local_price_sell,sell_usd_convert
            
            kraken_data = pd.DataFrame.from_dict(kraken_coin_lasttrade_price,orient = 'index')
            kraken_data = kraken_data.astype(float)
            kraken_data = kraken_data.round(3)
            kraken_data = kraken_data.rename(columns = {0:'local_price_buy',1:'buy_usd_convert',2:'local_price_sell',
                                                        3:'sell_usd_convert'})
            kraken_data_sort = kraken_data.sort_values('sell_usd_convert')
            print kraken_data_sort
            
            buy_list = kraken_data_sort['buy_usd_convert'].tolist()
            buy_list.sort()
            lowest_buy_price = buy_list[0]
            print 'lowest_buy_price',lowest_buy_price
            
            sell_list = kraken_data_sort['sell_usd_convert'].tolist()
            sell_list.sort()
            highest_sell_price = sell_list[-1]
            print 'highest_sell_price', highest_sell_price
            
            diff =  lowest_buy_price - highest_sell_price
            print 'difference between lowest buy price and highest sell price = ',diff
            perc_diff = (diff/lowest_buy_price)*100
            
            print 'percentage_diff = ',perc_diff
    
    def kraken_eth_btc_fiat_arb(self):
        """
        """
        
        
    def kraken_ripple_ticker(self):
        """
        """
        """https://api.kraken.com/0/public/Ticker?pair=XMLNXETH,XETHZGBP"""
        
        url_pairs = "https://api.kraken.com/0/public/Ticker?pair=%s"%(self.asset_pairs_string)
        ticker_info = requests.get(url_pairs)
        
        ticker_info_json = ticker_info.text
        
        ticker_info_dict = json.loads(ticker_info_json)
        
        result = ticker_info_dict['result']
                        
        'select the pairs that trade also on coinone'
        
        euro_pairs = ['XXBTZEUR','XETHZEUR','BCHEUR','XETCZEUR','XXRPZEUR','XLTCZEUR']
        
        usd_pairs = ['XXBTZUSD','XETHZUSD','BCHUSD','XETCZUSD','XXRPZUSD','XLTCZEUR']
        
        self.get_exchange_rate()
        exchange_rate = self.usd_exchange_rate_dict["rates"]['EUR']
        
        #for euro
        kraken_coin_lasttrade_price = {}
        for i in result:
            
            if i in euro_pairs:
                eur_price = float(result[i]['c'][0])
                kraken_coin_lasttrade_price[i] = eur_price,eur_price/exchange_rate
                        
        eur_kraken_data = pd.DataFrame.from_dict(kraken_coin_lasttrade_price,orient = 'index')
        eur_kraken_data = eur_kraken_data.rename(index={'XXBTZEUR': 'BTC','XETHZEUR':'ETH',
                                                    'BCHEUR':'BCH','XETCZEUR':'ETC','XXRPZEUR':'XRP',
                                                        'XLTCZEUR':'LTC'},
                                         columns = {0:'kraken_eur',1:'kraken_usd'})
        self.eur_kraken_data = eur_kraken_data
        
        #for usd
        
        kraken_coin_lasttrade_price = {}
        for i in result:
            
            if i in usd_pairs:
                usd_price = float(result[i]['c'][0])
                kraken_coin_lasttrade_price[i] = usd_price
                        
        usd_kraken_data = pd.DataFrame.from_dict(kraken_coin_lasttrade_price,orient = 'index')
        usd_kraken_data = usd_kraken_data.rename(index={'XXBTZUSD': 'BTC','XETHZUSD':'ETH',
                                                    'BCHUSD':'BCH','XETCZUSD':'ETC','XXRPZUSD':'XRP','XLTCZUSD':'LTC'},
                                         columns = {0:'kraken_usd'})
        self.usd_kraken_data = usd_kraken_data
        
    
    def get_exchange_rate(self):
        """
        """
        usd_exchange_rate = requests.get("http://api.fixer.io/latest?base=USD")
        usd_exchange_rate =  usd_exchange_rate.text
        usd_exchange_rate_dict = json.loads(usd_exchange_rate)
        self.usd_exchange_rate_dict = usd_exchange_rate_dict
        # print self.usd_exchange_rate_dict
        
    def coinone_ripple_ticker(self):
        """  
        """
                
        all_url = "https://api.coinone.co.kr/ticker?currency=all"
        xrp_url = "https://api.coinone.co.kr/ticker"
        eth_url = "https://api.coinone.co.kr/ticker/eth"
        btc_url = "https://api.coinone.co.kr/ticker/btc"
        
        all_response = requests.get(all_url)
        
        all_json = all_response.text
        "All prices in Korean, so need calculate to dollars"
    
        all_json_dict = json.loads(all_json)
        
        coin_usdprice_last_trade = {}
        self.get_exchange_rate()
        
        usd_krw_exchange_rate = self.usd_exchange_rate_dict["rates"]['KRW']
        
        for i in all_json_dict:
            
            if i == 'errorCode' or i == 'result' or i == 'timestamp':
                continue
            
            last_trade_krw =  all_json_dict[i]['last']
            last_trade_krw = float(last_trade_krw)
            last_trade_usd = last_trade_krw/usd_krw_exchange_rate
            coin_usdprice_last_trade[i] = last_trade_usd,last_trade_krw
        
        coinone_data = pd.DataFrame.from_dict(coin_usdprice_last_trade,orient = 'index')
        
        coinone_data = coinone_data.rename(index={'btc': 'BTC','eth':'ETH',
                                                    'bch':'BCH','etc':'ETC','xrp':'XRP','ltc':'LTC'},
                                         columns = {0:'coinone_usd',1:'coinone_krw'})
        
        self.coinone_data = coinone_data
        
        
        merged_eur = pd.merge(coinone_data,self.eur_kraken_data,left_index = True,right_index = True) 
        merged_usd = pd.merge(coinone_data,self.usd_kraken_data,left_index = True,right_index = True) 
        
        merged_list = [['EUR',merged_eur],['USD',merged_usd]]
        
        print '-----------------------------------------------------'
        print 'Check to see if arbitrage between Karaken and Coinone, base currency USD /n'
        print datetime.now()
        print 'Exchange rate krw-usd = ',usd_krw_exchange_rate
        
        max_diff_usd_eur_list = []
        
        for merged_info in merged_list:
            
            merged = merged_info[1]
            print merged_info[0]
            merged['coinone_usd'] = merged['coinone_usd'].astype('float')
            merged['kraken_usd'] = merged['kraken_usd'].astype('float')
            
            merged['diff'] = merged['coinone_usd']-merged['kraken_usd']
            merged['perc_diff'] = (merged['diff']/merged['coinone_usd'])*100
            
            print merged
            """calculate biggest difference between currencies
            Could always wait for makret to get closer together"""
            maximum_diff_between_coins = merged['perc_diff'].tolist()
            
            maximum_diff_between_coins.sort()
            print maximum_diff_between_coins
            biggest_diff = maximum_diff_between_coins[0] - maximum_diff_between_coins[-1]
            
            print 'Max diff is',  biggest_diff
    
            max_diff_usd_eur_list.extend(maximum_diff_between_coins)
        
        max_diff_usd_eur_list.sort()
        
        max_diff = max_diff_usd_eur_list[0] - max_diff_usd_eur_list[-1]
        print max_diff_usd_eur_list
        print max_diff
        
        
def main():
    """
    """
    
    CA = CryptoArbing()
    #CA.kraken_btc_fiat_arb()
    CA.get_kraken_tradeable_asset_pairs()
    CA.coinone_ripple_ticker()   
if __name__=="__main__":
    main()