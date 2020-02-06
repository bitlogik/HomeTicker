#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays Bitcoin price and network info in real-time
# Copyright (C) 2018-2019  BitLogiK

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

Your_Currency = "EUR"

import time
import RESTapi
import HomeTicker

print "PRESS CTRL+C TO QUIT"
myticker = HomeTicker.HomeTicker()
price_api = RESTapi.getRestJSON('https://api.coindesk.com/v1/bpi/currentprice.json')
latestblock = RESTapi.getRestJSON('https://api.blockchair.com/bitcoin/stats')
lntot_api = RESTapi.getRestJSON('https://txstats.com/api/datasources/proxy/1/query')
lntot_api.addParam({"db":"p2shinfo","q":'SELECT last("value") FROM "ln_stats" WHERE time > now()-1h GROUP BY time(0h) fill(null)'})

def printprice(curr):
    price_api.getData()
    latestblock.getData()
    lntot_api.getData()
    btc_price = float( price_api.getKey("bpi/"+curr+"/rate").replace(",", ""))
    myticker.clear_screen()
    myticker.write(("Bitcoin Price\r\n1 BTC = %.2f "+curr)%btc_price)
    time.sleep(10)
    myticker.clear_screen()
    myticker.write("Bitcoin Stats")
    height = latestblock.getKey("data/best_block_height")
    myticker.pos_cursor(2,1)
    myticker.write("Height:  %s"%height)
    time.sleep(5)
    diff = int(latestblock.getKey("data/difficulty"))
    myticker.pos_cursor(2,1)
    myticker.clear_line()
    myticker.write("Diff  :  %i G"% (diff/10**9) )
    time.sleep(5)
    lntot = float( lntot_api.getKey("results/0/series/0/values/0/1") ) / 100000000
    myticker.clear_screen()
    myticker.write("Total LN channels")
    myticker.pos_cursor(2,4)
    myticker.write( "   %.1f BTC   " % lntot )

while True:
    try:
        printprice("USD")
        time.sleep(5)
        printprice(Your_Currency)
        time.sleep(5)
    except KeyboardInterrupt:
        break
    except:
        print "Issue detected, check Internet and the HomeTicker USB"
        print "Retrying in 5 seconds..."
        print "Press CTRL+C to abort"
        time.sleep(5)
myticker.close()
