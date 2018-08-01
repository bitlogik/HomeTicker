#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# Example for HomeTicker display
# Emulates a terminal on the HomeTicker, Windows Only
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

from msvcrt import getch
import time
import HomeTicker

myticker = HomeTicker.HomeTicker(False)

cursor_state = 1
debug = False

# Uncomment below to debug
#debug = True

print("PRESS ESC TO QUIT")
myticker.set_cursor( cursor_state )
while True:
    key = ord(getch())
    if debug:print "KeyCode:"+str(key)
    if key == 27: #ESC
        break
    elif key%224 == 0:
        key = ord(getch())
        if debug:print "2nd special code:"+str(key)
        if key == 59: #F1
            myticker.set_mode(1)
            print "Mode Circular Enabled"
        if key == 60: #F2
            myticker.set_mode(2)
            print "Mode Paging Enabled"
        if key == 61: #F3
            myticker.set_mode(3)
            print "Mode Line Scrolling Enabled"
        if key == 80: #Down arrow
            myticker.move_cursor_down()
            if debug:print "Curr Down"
        elif key == 72: #Up arrow
            myticker.move_cursor_up()
            if debug:print "Curr Up"
        elif key == 75: #Left arrow
            myticker.move_cursor_left()
            if debug:print "Curr Left"
        elif key == 77: #Right arrow
            myticker.move_cursor_right()
            if debug:print "Curr Right"
        elif key == 82: #Inser
            cursor_state += 1
            myticker.set_cursor( cursor_state%2 )
        elif key == 83: #Suppr
            myticker.clear_line()
        elif key == 71: #Home
            myticker.move_cursor_home()
            if debug:print "Curr Home"
        elif key == 79: #End
            myticker.move_cursor_end()
            if debug:print "Curr End"
    else:
        myticker.printchr(chr(key))
myticker.close()
