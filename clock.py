#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays date and time as a clock app
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

import HomeTicker
import time

myticker = HomeTicker.HomeTicker()
print "PRESS CTRL+C TO QUIT"

def printdate(oneticker):
    present_time = time.localtime()
    oneticker.pos_cursor(1,1)
    remaining = 60 - present_time.tm_sec
    date = time.strftime("%a %d %b %Y", present_time).center(20)
    oneticker.write(date)
    hour = time.strftime("%H:%M", present_time)
    oneticker.pos_cursor(2,8)
    oneticker.write(hour)
    time.sleep(remaining)

try:
    while True:
        printdate(myticker)
except KeyboardInterrupt:
    pass
myticker.close()
