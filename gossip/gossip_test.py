# -*- coding: UTF-8 -*-

import sys
sys.path.append('..')
from lib.article_parser import GossipArticleParser 


url="https://www.ptt.cc/bbs/Gossiping/M.1484651804.A.6FC.html"
ps='爆'

gAP=GossipArticleParser(url,ps)
print gAP.prepare_query_tuples()
