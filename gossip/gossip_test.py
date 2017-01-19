# -*- coding: UTF-8 -*-

import sys
sys.path.append('..')
from lib.article_parser import GossipArticleParser 
url="https://www.ptt.cc/bbs/Gossiping/M.1484760077.A.E1E.html"

ps='爆'

gAP=GossipArticleParser(url,ps)
w=gAP.prepare_query_tuples()

print len(w)
print len(w[0])
print len(w[1])
