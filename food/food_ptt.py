import sys
sys.path.append('..')
from lib.parse_class import FoodMenuParser
from lib.parse_class import FoodArticleParser
from lib.DBconn import FoodDBconn 


ww=FoodMenuParser()
ww.parse_url("https://www.ptt.cc/bbs/Food/index5882.html")
print ww.get_url_list()


FAP=FoodArticleParser("https://www.ptt.cc/bbs/Food/M.1483943634.A.A3E.html")

w=FAP.prepare_query_tuples()
#print w

a=FoodDBconn()
a.connect()
a.submit(w)
a.close()
