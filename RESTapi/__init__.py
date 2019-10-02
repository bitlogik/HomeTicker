#!/usr/bin/python2
# -*- coding: utf8 -*-

import json
import urllib
import urllib2

class getRestJSON:
    def __init__(self , url = "" , params = "" ):
        self.url = url
        self.params = dict(params)
        self.jsres = []
    
    def setURL(self,url):
        self.url = url
    
    def addParam(self,param):
        self.params.update(param)
        
    def getData(self):
        params_enc = urllib.urlencode( self.params )
        try:
            if params_enc:
                req = urllib2.Request(self.url+"?"+params_enc, headers={ 'User-Agent': 'Mozilla/5.0', 'Cache-Control':'max-age=0' })
            else:
                req = urllib2.Request(self.url, headers={ 'User-Agent': 'Mozilla/5.0', 'Cache-Control':'max-age=0' })
            self.webrsc = urllib2.urlopen(req)
            self.jsres = json.load(self.webrsc)
        except urllib2.URLError as err:
            if err.reason[1][:36] == '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE]':
                print "-"*30
                print "RESTapi can't connect to the remote server"
                print "Too old version of OpenSSL in your Python"
                print "On Mac, install Homebrew, then"
                print "$ brew install python@2"
                print " Use : $ python2 xxxx.py"
                print "-"*30
            raise IOError("Error while processing request:\n%s"%(self.url+"?"+params_enc))
        except Exception as err:
            raise IOError("Error while processing request:\n%s"%(self.url+"?"+params_enc))
    
    def getKey(self,keychar):
        out=self.jsres
        path=keychar.split("/")
        for key in path:
            if key.isdigit(): key=int(key)
            try:
                out = out[key]
            except:
                raise KeyError("Key Error. Did you get data?")
        return out
