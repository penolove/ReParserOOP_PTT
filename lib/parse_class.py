# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import googlemaps
import random
print 'hello parser_class'
class Parser(object):
    def __init__(self):
        #this used to store cookie or something
        self.rs=requests.session()
    def parse_url(self,url):
        self.url=url
        res=self.rs.get(url)
        self.soup=BeautifulSoup(res.text)


class GossipParser(Parser):

    """add interface to pass cookie and filter for MenuParser"""
    def __init__(self):
        super(GossipParser, self).__init__()
        payload = {
            'from':'bbs/Gossiping/index.html',
            'yes':'yes'
        }
        self.askurl="https://www.ptt.cc/ask/over18"
        # get the over 18 cookie
        self.rs.post(self.askurl,data=payload)
