#!/usr/bin/python2
# -*- coding: utf8 -*-

# Python library for HomeTicker
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


import serial
import serial.tools.list_ports
import time

class HomeTicker:
    def __init__(self, ClearClose = True):
        gen_port = serial.tools.list_ports.grep('067B:2303')
        port = None
        for n in gen_port:
            port = n.device
        if port is None:
            raise IOError("Error finding HomeTicker\nCheck it is connected on this machine")
        try:
            self.device = serial.Serial(port)
        except Exception as err:
            if err[0]==13:
                raise IOError("Permission Denied\n do 'sudo usermod -a -G dialout $USER' \
                               then reboot/relog\n also check the HomeTicker is not in use.")
            else:
                print repr(err)
                raise IOError("Error initializing HomeTicker")
        self.clearclose = ClearClose
        self.reset()
        self.set_brightness(4)
        self.set_mode(1)
        self.set_charset("")
    
    def __del__(self):
        if hasattr('self', 'device'):
            time.sleep(0.2)
            self.device.flush()
            time.sleep(0.2)
            self.device.close()
    
    def close(self):
        if self.clearclose:
            self.clear_screen()
        time.sleep(0.2)
        self.device.flush()
        time.sleep(0.2)
        self.device.close()
        del self
    
    def send_buffer(self, buffer):
        self.device.write(buffer)
    
    def send_ctrl_seq(self, ctrl_seq):
        self.send_buffer([31]+ctrl_seq)
    
    def reset(self):
        self.send_buffer([27,64])
        
    def set_mode(self, mode):
        # 1 : Mode Circular
        # 2 : Mode Paging
        # 3 : Mode Line Scrolling
        if mode == 1 or mode == 2 or mode == 3:
            self.send_ctrl_seq([mode])
            self.current_mode = mode
        else:
            raise "Bad mode number"
    
    def set_charset(self, chrset):
        chrsetcode = 8
        self.chrset = "cp858" # Default charset
        if chrset == "cp437": # Code Page 437, ASCII
            self.chrset = chrset
            chrsetcode = 0
        if chrset == "cp932": # Code Page 932, Microsoft Japanese shift-JIS
            self.chrset = chrset
            chrsetcode = 1
        if chrset == "cp850": # Code Page 850, Generic Western Europe
            self.chrset = chrset
            chrsetcode = 2
        if chrset == "cp860": # Code Page 860, Portuguese
            self.chrset = chrset
            chrsetcode = 3
        if chrset == "cp863": # Code Page 863, French Canadian
            self.chrset = chrset
            chrsetcode = 4
        if chrset == "cp865": # Code Page 865, Scandinavia
            self.chrset = chrset
            chrsetcode = 5
        if chrset == "cp852": # Code Page 852, Eastern Europe
            self.chrset = chrset
            chrsetcode = 6
        if chrset == "cp866": # Code Page 866, Russian
            self.chrset = chrset
            chrsetcode = 7
        if chrset == "cp858": # Code Page 858, Western Europe
            self.chrset = chrset
            chrsetcode = 8
        if chrset == "cp1252": # Code Page w1252, Latin1 Europe
            self.chrset = chrset
            chrsetcode = 9
        if chrset == "cp1250": # Code Page w1250, Central Europe
            self.chrset = chrset
            chrsetcode = 14
        if chrset == "cp1251": # Code Page w1251, Cyrillic
            self.chrset = chrset
            chrsetcode = 15
        if chrset == "cp864": # Code Page 864, Arabic
            self.chrset = chrset
            chrsetcode = 27
        if chrset == "cp775": # Code Page 775, Baltic
            self.chrset = chrset
            chrsetcode = 28
        if chrset == "cp737": # Code Page 737, Greek
            self.chrset = chrset
            chrsetcode = 29
        if chrset == "cp1253": # Code Page w1253, Greek
            self.chrset = chrset
            chrsetcode = 30
        if chrset == "cp1254": # Code Page w1254, Turkish
            self.chrset = chrset
            chrsetcode = 31
        self.send_buffer([27, 116, chrsetcode])
        time.sleep(0.6)
    
    def set_brightness(self, brightness):
        self.send_ctrl_seq([88, brightness, 0])
    
    def clear_screen(self):
        self.send_buffer([12])
    
    def clear_line(self):
        self.send_buffer([24])
    
    def printchr(self, chr):
        self.send_buffer([chr])
    
    def set_cursor(self,onoff):
        self.send_ctrl_seq( [67,48+onoff] )
    
    def move_cursor_up(self):
        self.send_ctrl_seq( [10] )
    
    def move_cursor_down(self):
        self.send_buffer( [10] )
    
    def move_cursor_right(self):
        self.send_buffer( [9] )
    
    def move_cursor_left(self):
        self.send_buffer( [8] )
    
    def move_cursor_leftend(self):
        self.send_buffer( [13] )
    
    def move_cursor_rightend(self):
        self.send_ctrl_seq( [13] )

    def move_cursor_home(self):
        self.send_buffer( [11] )
    
    def move_cursor_end(self):
        self.send_ctrl_seq( [66] )
    
    def pos_cursor(self, line, col):
        assert( 1 <= line <= 9 )
        assert( 1 <= col <= 99 )
        buffer = [36, col, line]
        self.send_ctrl_seq( buffer )
    
    def write(self, msg):
        msge = msg.encode(self.chrset)
        while msge:
            msg_chr = list(msge)[0:29]
            self.send_buffer(map(ord, msg_chr))
            msge = msge[29:]
    
    def scroll_line(self, text, times = 1, speed = 3):
        twait = speed/20.0
        self.device.write([31,3])
        self.move_cursor_rightend()
        ltxt = len(text)+20
        text += " "*20
        while times>0:
            for i in range(0,ltxt):
                self.write(text[i])
                time.sleep(twait)
            times -= 1
        self.device.write([31,self.current_mode])
