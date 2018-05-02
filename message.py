#!/usr/bin/python2
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Displays messages with unicode characters at different locations
# and changes the brightness
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
myTicker = HomeTicker.HomeTicker()

myTicker.write(u"Cet été sera\n\rtrès chaud!CALIENTE!")
myTicker.pos_cursor(1,14)
myTicker.printchr(0xC8)
myTicker.pos_cursor(1,18)
myTicker.write(u"¤")
for b in range(1,5):
    print b,
    myTicker.set_brightness(b)
    time.sleep(2)
raw_input("PRESS ENTER TO EXIT")
myTicker.close()
