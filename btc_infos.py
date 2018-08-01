#!/usr/bin/python2
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays Bitcoin price and network info in real-time
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
import HomeTicker

print "PRESS CTRL+C TO QUIT"
myticker = HomeTicker.HomeTicker()
price_api = RESTapi.getRestJSON('https://api.coindesk.com/v1/bpi/currentprice.json')
latestblock = RESTapi.getRestJSON('https://chain.api.btc.com/v3/block/latest')

def printprice(curr):
    price_api.getData()
    latestblock.getData()
    btc_price = float( price_api.getKey("bpi/"+curr+"/rate").replace(",", ""))
    myticker.clear_screen()
    myticker.write(("Bitcoin Price\r\n1 BTC = %.2f "+curr)%btc_price)
    time.sleep(10)
    myticker.clear_screen()
    height = latestblock.getKey("data/height")
    myticker.write("Height:  %s"%height)
    myticker.pos_cursor(2,1)
    diff = int(latestblock.getKey("data/difficulty"))
    myticker.write("Diff  :  %i G"% (diff/10**9) )

while True:
    try:
        printprice("USD")
        time.sleep(5)
        printprice("EUR")
        time.sleep(5)
    except KeyboardInterrupt:
        break
    except:
        print "Issue detected, check Internet and the HomeTicker USB"
        print "Press CTRL+C to abort"
        time.sleep(5)
myticker.close()
