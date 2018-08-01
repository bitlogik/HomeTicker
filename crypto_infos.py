#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays real-time Bitcoin and Ethereum infos
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
import HomeTicker
import RESTapi

myticker = HomeTicker.HomeTicker()
pricebtc_api = RESTapi.getRestJSON('https://api.coindesk.com/v1/bpi/currentprice.json')
priceeth_api = RESTapi.getRestJSON("https://poloniex.com/public",{"command":"returnTicker"})
statsblkapi = RESTapi.getRestJSON("https://etherchain.org/api/blocks/count")
latestblock = RESTapi.getRestJSON('https://chain.api.btc.com/v3/block/latest')
myticker.set_brightness(4)
print "PRESS CTRL+C TO QUIT"

def printHT():
    myticker.clear_screen()
    myticker.pos_cursor(1,6)
    myticker.write("HomeTicker")
    myticker.pos_cursor(2,1)
    myticker.scroll_line("A desk ticker for home or office")

def printbtcprice():
    pricebtc_api.getData()
    latestblock.getData()
    btc_price = float( pricebtc_api.getKey("bpi/USD/rate").replace(",", "") )
    myticker.clear_screen()
    myticker.pos_cursor(1,1)
    myticker.write(("Bitcoin Stats\r\n1 BTC = %.2f USD") % btc_price)
    time.sleep(3)
    height = latestblock.getKey("data/height")
    myticker.pos_cursor(2,1)
    myticker.clear_line()
    myticker.write("Height: %s" % height)
    time.sleep(3)
    myticker.pos_cursor(2,1)
    myticker.clear_line()
    diff = int(latestblock.getKey("data/difficulty"))
    myticker.write("Diff  :  %i G" % (diff/10**9) )

def printethprice():
    priceeth_api.getData()
    statsblkapi.getData()
    btc_price = float( priceeth_api.getKey("BTC_ETH/last") )
    myticker.clear_screen()
    myticker.write(("Ethereum Stats\r\n 1 ETH =  %.1f mBTC")% (btc_price*1000) )
    btc_price = float( priceeth_api.getKey("USDT_ETH/last") )
    time.sleep(3)
    myticker.pos_cursor(2,1)
    myticker.clear_line()
    myticker.write((" 1 ETH =  %.2f USD")% btc_price )
    blkethn = statsblkapi.getKey("count")
    time.sleep(3)
    myticker.pos_cursor(2,1)
    myticker.clear_line()
    myticker.write(("Block#  %i")% (blkethn) )

while True:
    try:
        printbtcprice()
        time.sleep(3)
        printHT()
        printethprice()
        time.sleep(3)
        printHT()
    except KeyboardInterrupt:
        break
    except:
        print "Issue detected, check Internet and the HomeTicker USB"
        print "Press CTRL+C to abort"
        time.sleep(5)
myticker.close()

