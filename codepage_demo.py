#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Example for HomeTicker
# Example about international code page
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

myticker = HomeTicker.HomeTicker()

# Code Page 866 Cyrillic Альтернативная кодировка
myticker.set_charset("cp866")
myticker.write(u"Привет идиот")
myticker.pos_cursor(2,16)
myticker.write(">\x9f".decode("cp866"))
myticker.device.write(">\x9f")
raw_input("PRESS ENTER to continue")

myticker.clear_screen()
# CodePage 932, "Shifted-JIS"
# requires half-width hankaku katakana (半角片仮名)
myticker.set_charset("cp932")
myticker.write(u"ｺｿﾆﾁﾜ ﾊﾞｶ")
raw_input("PRESS ENTER to continue")
myticker.close()
