import sys
sys.path.append('..')
from lib.menu_parser import GossipMenuParser

ww=GossipMenuParser()
ww.parse_url("https://www.ptt.cc/bbs/Gossiping/index19942.html")
print ww.get_url_list()
