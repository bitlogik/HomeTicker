#!/usr/bin/python2
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays present weather conditions in a defined city
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

city = "Paris"
state_code = "fr"
metric_units = True


import RESTapi
import HomeTicker

myticker = HomeTicker.HomeTicker(False)

mydata = RESTapi.getRestJSON()

query = "select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s, %s\")" % (city, state_code)
if metric_units:
    query+=" and u=\"c\""
    temp_unit = "C"
else:
    temp_unit = "F"

mydata.setURL("https://query.yahooapis.com/v1/public/yql")
mydata.addParam({ "q":query, "format":"json" })
print "WAIT FOR DATA READING...",
mydata.getData()

weather = mydata.getKey("query/results/channel/item/condition/text").lower()
pres_temp = int(mydata.getKey("query/results/channel/item/condition/temp"))
# can also use :
# query/results/channel/units pressure speed temperature
# query/results/channel/astronomy sunrise sunset
# query/results/channel/atmosphere humidity pressure
# query/results/channel/item/forecast/1/text

myticker.write(u"%s weather :" % city )
myticker.pos_cursor(2,1)
myticker.clear_line()
myticker.write(u"%i°%s  %s" % ( pres_temp, temp_unit, weather ) )

myticker.close()
