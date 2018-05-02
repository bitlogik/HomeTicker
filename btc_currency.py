#!/usr/bin/python2
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


# See the currency list using currency codes
# at https://openexchangerates.org/api/currencies.json
currency = "EUR"

import time
import api.getRestJSON
import HomeTicker

myticker = HomeTicker.HomeTicker()
price_api = api.getRestJSON.getRestJSON('https://api.coindesk.com/v1/bpi/currentprice.json')
RateApi = api.getRestJSON.getRestJSON(
                'https://openexchangerates.org/api/latest.json',
                {"app_id":"2af667e95c984a1a8c1cb635c1eb6aab"}
            )

print "PRESS CTRL+C TO QUIT"
myticker.write("Bitcoin Price")
try:
    while True:
        price_api.getData()
        btc_price = float( price_api.getKey("bpi/USD/rate").replace(",", "") )
        RateApi.getData()
        currency_price = RateApi.getKey("rates/"+currency)
        btc_price_cur = btc_price * currency_price
        myticker.pos_cursor(2,3)
        myticker.write(
            "1 BTC = %.0f %s  " %
            ( btc_price_cur , currency )
        )
        time.sleep(60)
except KeyboardInterrupt:
    pass
myticker.close()
