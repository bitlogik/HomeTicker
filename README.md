
# HomeTicker Software

Python software to control the HomeTicker desk ticker display.

## Installation

Requirements :

 - A HomeTicker ( [website](https://hometicker.shop) )
 - Python v2.7

To get details how to install HomeTicker software, visit https://hometicker.shop/software


To test everything is OK, connect the HomeTicker on your machine and start :

    hello.py

This should display "hello, world!" on the HomeTicker.


## Using the TickerShop library

There are many examples provided in this software. You can use them straight forward, or modify them (let your modifications public, this is under GPLv3).
To use the library, just use import as usual :

    import HomeTicker

You need HomeTicker and serial directories aside your python program. Eventually the api directory, in case you are using getRestJSON.


#### Initialization

Class constructor detects, tries to connect to the HomeTicker, initializes it and finally returns an object to send commands.

    myticker = HomeTicker.HomeTicker()

There is an optional argument : "clear close". It setups whether the screen is cleared (black) at the end when the hometicker object is closed. The default behavior is True, so the HomeTicker clears it self at the end. In the helloworld demo, this is set to False so the message stays even the library finished and returns.


#### Clear Screen

Clear and erase the HomeTicker screen.

    myticker.clear_screen()


#### Print a Character

Print a character from its number at the cursor position

    myticker.printchr(CHAR_CODE)


#### Position Cursor

Change the position of the cursor to a given column and line.

    myticker.pos_cursor(LINE, COLUMN)


#### Write Message

Write a message to the HomeTicker screen at the cursor position. This function uses automatic decoding of any unicode character. In case you provide directly the string don't forget trailing u (  u"string" ). You can use "\r" and "\n" inside the string to get line control.

    myticker.write(MESSAGE_STRING)


#### Close Device

Close the connection properly with the HomeTicker. Normally, when python program stops, it closes the link automatically.

    myticker.close()

If you opened it with clearclose=False, then the last message displayed is kept as it is.


**For more details: see code of the many examples provided**

More functions will be documented here later, such as cursor management, scrolling display mode, brightness control and international charsets.


## License

Copyright (C) 2018  BitLogiK

Some software files are from PySerial library under 3-Clause BSD License
Copyright (c) 2001-2017 Chris Liechti <cliechti@gmx.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

