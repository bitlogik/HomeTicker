#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays real-time Bitcoin price in any local currency
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


# See the currency string according to ISO4217
currency = "EUR"

import time
import RESTapi
import HomeTicker

myticker = HomeTicker.HomeTicker()
price_api = RESTapi.getRestJSON('https://min-api.cryptocompare.com/data/price')
price_api.addParam( { "extraParams": "HomeTicker display",
                "fsym":"BTC", "tsyms": currency} )

print "PRESS CTRL+C TO QUIT"
myticker.write("Bitcoin Price")
myticker.set_mode(3)
try:
    while True:
        price_api.getData()
        btc_price_cur = price_api.getKey( currency )
        myticker.pos_cursor(2,3)
        myticker.clear_line()
        myticker.write(
            "1 BTC = %.0f %s" %
            ( btc_price_cur , currency )
        )
        time.sleep(30)
except KeyboardInterrupt:
    pass
myticker.close()
