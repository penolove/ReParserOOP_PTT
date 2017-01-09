
# -*- coding: UTF-8 -*-
from parse_class import Parser
from parse_class import GossipParser

class MenuParser(Parser):
    def get_url_list(self):
        self.urlist=[]
        for i in self.soup.select('.r-ent'):
            if(self.filter(i)):
                try:
                    self.urlist.append('https://www.ptt.cc'+i.select('a')[0]['href'])
                except IndexError:
                    pass
        return self.urlist
    def filter(self,i):
        return True


class FoodMenuParser(MenuParser):
    def filter(self,i):
        return True


class GossipMenuParser(GossipParser,MenuParser):
    """add interface to pass cookie and filter for MenuParser"""
    push_score_list=[]
    def filter(self,i):
        try:
            push_score=i.select('span')[0].text
            if(push_score=='爆'.decode('utf-8') or push_score==u'XX' or push_score=='99'):
                self.push_score_list.append(push_score)
                return True
            else:
                return False
        except IndexError:
            return False
    def clean_push_score(self):
        self.push_score_list=[]

    def get_date_list(self):
        date_list=[]
        for i in self.soup.select('.r-ent'):
            date_list.append(i.select('.date')[0].text)
        return date_list
