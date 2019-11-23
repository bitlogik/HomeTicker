#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays stocks prices in real-time
# Copyright (C) 2018  BitLogiK

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import time
import RESTapi
import urllib
import HomeTicker

# See code at https://finance.yahoo.com/
stock_code_list = ["^DJI", "MSFT", "GOOG", "AAPL", "005930.KS", "^IXIC", "V", "INTC", "BTC-USD", "ETH-USD", "XAUUSD=X", "BZ=F","^FTSE", "^N225", "^BVSP"]

print "PRESS CTRL+C TO QUIT"

class YahooStockPrice():
    def __init__(self, quote_code):
        self.stocks_api = RESTapi.getRestJSON( 
            'https://query1.finance.yahoo.com/v7/finance/spark' )
        self.stocks_api.addParam( { "symbols":quote_code, "range":"1d",
                                   "interval":"1m", "indicators":"close",
                                   "includeTimestamps":False,
                                   "includePrePost":False,
                                   "corsDomain":"finance.yahoo.com",
                                   ".tsrc":"finance"} )
        self.getname(quote_code)
    
    def update(self):
        self.stocks_api.getData()
        QuoteKeyRoot = "spark/result/0/response/0/indicators/quote/0/close"
        try:
            i = len ( self.stocks_api.getKey(QuoteKeyRoot) ) - 1
            while self.stocks_api.getKey( QuoteKeyRoot+"/"+str(i) ) == None:
                i-=1
            self.latest = float ( self.stocks_api.getKey(QuoteKeyRoot+"/"+str(i)) )
        except:
            self.latest = float ( self.stocks_api.getKey("spark/result/0/response/0/meta/chartPreviousClose") )
        self.previous =  float ( self.stocks_api.getKey("spark/result/0/response/0/meta/previousClose") )
        self.currency = self.stocks_api.getKey("spark/result/0/response/0/meta/currency")
        self.variation = self.latest - self.previous
    
    def HometickerPrint(self, hometicker):
        self.update()
        hometicker.clear_screen()
        hometicker.write( self.name[1:20] )
        hometicker.pos_cursor(2,1)
        hometicker.write( "%.2f %s" % (self.latest, self.currency) )
        hometicker.pos_cursor(2,16)
        hometicker.write( "%+.0f" % (self.variation) )
    
    def getname(self, code):
        f = urllib.urlopen("https://finance.yahoo.com/quote/"+code)
        datapage = f.read(500)
        startstr = datapage.find("content=\"") + 9
        self.name = datapage[startstr:].split(",")[1].replace("amp;","").replace("USD","rate")

myhometicker = HomeTicker.HomeTicker()
myhometicker.write("Loading Wait")

apilist = []
while len(apilist)==0:
    try:
        for stock in stock_code_list:
            apilist.append(YahooStockPrice(stock))
    except:
        print "Issue detected, check Internet"
        print "Retrying in 5 seconds..."
        print "Press CTRL+C to abort"
        time.sleep(5)
while True:
    try:
        for api in apilist:
            api.HometickerPrint(myhometicker)
            time.sleep(8)
    except KeyboardInterrupt:
        break
    except:
        print "Issue detected, check Internet and the HomeTicker USB"
        print "Retrying in 5 seconds..."
        print "Press CTRL+C to abort"
        time.sleep(5)
myhometicker.close()
