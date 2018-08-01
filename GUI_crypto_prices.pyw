#!/usr/bin/python2
# -*- coding: utf8 -*-

# GUI example for HomeTicker display
# GUI to display various crypto-currencies prices
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
try:
    import tkMessageBox
except Exception as err:
    print err
    quit()
import Tkinter
try:
    myhometicker = HomeTicker.HomeTicker()
    myhometicker.write("Loading ... ")
except Exception as error_msg:
    Tkinter.Tk().withdraw()
    tkMessageBox.showerror("HomeTicker Error", error_msg)
    raise

import urllib
import json
import time
import os
import pickle
import RESTapi

if os.name == 'nt':
    import ctypes
    myappid = 'fr.bitlogik.GUIHT.001'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Getting the coin list
CoinListDBFileName = 'CoinList.db'
# Test if local data exists and is not too old (<2 days)
if os.path.exists(CoinListDBFileName) and (
             ( time.time()-os.path.getmtime(CoinListDBFileName) ) < 170000 ):
    # Load from file
    with open(CoinListDBFileName) as f:
        [coin_list_keyrank, coin_list_keyname, coin_list_keysymbol] = pickle.load(f)
else:
    # Load from Internet
    myhometicker.write("\n\r Getting coins data")
    try:
        listurlapi = urllib.urlopen(
                    "https://min-api.cryptocompare.com/data/top/volumes?tsym=USD&limit=350" )
        coinlist_full = json.loads( listurlapi.read().decode('cp850') )
    except:
        Tkinter.Tk().withdraw()
        myhometicker.write("\rInternet error !   ")
        tkMessageBox.showerror("Internet error",
                    "Can't reach the data server.\nPlease check your connection.\n\n" )
        myhometicker.close()
        raise
    # Sorting and cleaning the data
    coin_list_keyrank = {}
    coin_list_keyname = {}
    coin_list_keysymbol = {}
    idx = 1
    for coindata in coinlist_full["Data"]:
        if coindata["SYMBOL"] != coindata["FULLNAME"] and idx<=250:
            coindata["CoinName"] = coindata["NAME"].strip()
            coindata["FullName"] = coindata["FULLNAME"].strip()
            coin_list_keyrank[ idx ] = coindata
            coin_list_keyname[ coindata["NAME"] ] = coindata
            coin_list_keysymbol[coindata["SYMBOL"] ] = coindata
            idx+=1
    
    # Saving data to file
    with open(CoinListDBFileName, 'w') as f:
        pickle.dump([coin_list_keyrank, coin_list_keyname, coin_list_keysymbol], f)

# Generate coin list according to sorting option
def gosort(*args):
    global coin_list_sorted
    sort_option = sorting_choice.get()
    if sort_option == "SortOrder":
        coin_list_sorted = sorted(coin_list_keyrank)
    if sort_option == "CoinName":
        coin_list_sorted = sorted(coin_list_keyname)
    if sort_option == "Symbol":
        coin_list_sorted = sorted(coin_list_keysymbol)
    option.delete(0, Tkinter.END)
    coin_option_list = []
    if sort_option != "SortOrder":
        for coin in coin_list_sorted: #lim
            coin_option_list.append(coin)
    else:
        for coinrank in coin_list_sorted: #lim
            coin_option_list.append(str(coinrank) + " : "
              + coin_list_keyrank[coinrank]["SYMBOL"])
    for item in coin_option_list:
        option.insert(Tkinter.END, item)

def print_monitor(text):
    labelinfo['fg'] = 'dark green'
    labelinfo['text'] = "currently monitoring in %s :\n%s" % (currency_choice, text)

def print_error(text):
    labelinfo['fg'] = 'red'
    labelinfo['text'] = "Error :\n"+text

def display_info(name, price, currency):
    try:
        myhometicker.clear_screen()
        myhometicker.move_cursor_down()
        myhometicker.write( str(price)+" "+currency )
        myhometicker.move_cursor_home()
        myhometicker.write( name[:20] )
    except:
        print_error( "HomeTicker issue.\nRestart the app" )
        return

def display_coin(coindata):
    global display_loop
    # If end of coin list go to get new data
    if coindata == None:
        display_coin_list()
    else:
        # Display coin info
        selname = coindata["FullName"]
        try:
            price = coin_api.getKey( coindata["SYMBOL"]+"/"+currency_choice )
        except:
            price = " -- No data --     "
        display_info(selname, price, currency_choice)
        display_loop = master.after(8000, display_coin, next(coiniter, None))

# Get coins prices and display one by one
def display_coin_list():
    global currency_choice, coiniter, display_loop
    currency_choice = currency.get()
    selsymb = [coin["SYMBOL"] for coin in selected_coin_data_list]
    coin_api.addParam( { "extraParams": "HomeTicker display",
                "fsyms":",".join(selsymb), "tsyms": currency_choice} )
    try:
        coin_api.getData()
    except:
        print_error( "Internet service issue.\nRetrying in 10 sec." )
        display_loop = master.after(10000, display_coin_list)
        return
    print_monitor( " ".join(selsymb) )
    coiniter = iter(selected_coin_data_list)
    display_coin( next(coiniter, None) )

# Return data coin from the selection index
def get_sel_data_list(curselect):
    if sorting_choice.get() == "SortOrder":
        return coin_list_keyrank[ coin_list_sorted [ curselect ] ]
    if sorting_choice.get() == "CoinName":
        return coin_list_keyname[ coin_list_sorted [curselect ] ]
    if sorting_choice.get() == "Symbol":
        return coin_list_keysymbol[ coin_list_sorted [ curselect ] ]

# Get coin data from the selected options
def gowatch():
    global selected_coin_data_list
    if display_loop is not None:
        master.after_cancel(display_loop)
    selected_coin_data_list = map(get_sel_data_list, option.curselection() )
    if selected_coin_data_list == [] :
        labelinfo['text'] = ""
        myhometicker.clear_screen()
        myhometicker.write("Select coins")
        return
    display_coin_list()

def clear_sel_list():
    option.selection_clear(0, Tkinter.END)

# Initialize coin api
coin_api = RESTapi.getRestJSON( 
            'https://min-api.cryptocompare.com/data/pricemulti' )

# GUI building
master = Tkinter.Tk()
master.resizable(False, False)
leftframe = Tkinter.Frame(master, padx=30, pady=20)
leftframe.winfo_toplevel().title("HomeTicker CryptoCurrencies Prices")
if os.name == 'nt':
    leftframe.winfo_toplevel().wm_iconbitmap(bitmap='HTicon.ico')
else:
    leftframe.winfo_toplevel().wm_iconbitmap(bitmap='@HTicon.xbm')
leftframe.pack(fill=Tkinter.Y)
rightframe = Tkinter.Frame(leftframe, padx=20)
rightframe.pack( side = Tkinter.RIGHT)

labeltxt = Tkinter.Label( leftframe, text="Select the coins\nto display", font='bold' )
labeltxt.pack()
scrollbar = Tkinter.Scrollbar(leftframe, orient=Tkinter.VERTICAL)
option = Tkinter.Listbox(leftframe, exportselection=0, selectmode=Tkinter.MULTIPLE,
            yscrollcommand=scrollbar.set, height=25 )
scrollbar.config(command=option.yview)
scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
option.pack()
buttonclr = Tkinter.Button(leftframe, text="clear selection", font=("Arial", 12),
            command=clear_sel_list, anchor=Tkinter.N )
buttonclr.pack()

sorting_choice = Tkinter.StringVar()
sorting_choice.set("SortOrder")
sorting_choice.trace("w", gosort)
gosort()

labelsort = Tkinter.Label( rightframe, text="Sorting options",
            font='bold' )
labelsort.pack()

radiosort = Tkinter.Radiobutton(rightframe, text=" Rank     ",
            variable=sorting_choice, value="SortOrder" )
radiosort.pack()
radiosort = Tkinter.Radiobutton(rightframe, text=" Name   ",
            variable=sorting_choice, value="CoinName" )
radiosort.pack()
radiosort = Tkinter.Radiobutton(rightframe, text=" Symbol ",
            variable=sorting_choice, value="Symbol" )
radiosort.pack()

labelcurr = Tkinter.Label( rightframe, text="\n\nCurrency (ISO4217 code)",
            font='bold' )
labelcurr.pack()
currency = Tkinter.Entry(rightframe, width=6)
currency.pack()
currency.insert(0, "USD")
labelspace = Tkinter.Label( rightframe, text="", font=("",28) )
labelspace.pack()
button = Tkinter.Button(rightframe, text="Watch", font=("Arial", 16),
            command=gowatch, pady=12, padx=12, anchor=Tkinter.N )
button.pack()
labelinfo = Tkinter.Label( rightframe, text="", font=("",10), fg='red',
            pady=8, wraplength=175 )
labelinfo.pack()
labelsource = Tkinter.Label( master, text="Data provided by cryptocompare.com",
            font=("",8), fg='grey60')
labelsource.pack()

myhometicker.clear_screen()
myhometicker.write("Select coins")
display_loop = None
Tkinter.mainloop()
myhometicker.close()
