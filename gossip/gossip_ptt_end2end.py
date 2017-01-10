import sys
sys.path.append('..')
from lib.menu_parser import GossipMenuParser
from lib.article_parser import GossipArticleParser 
from lib.DBconn import Gossipconn

import time


# get current date
today1=time.strftime("%m/%d")
years=time.strftime("%Y")
if(int(today1.split("/")[0])<10):
    today1=str(int(today1.split("/")[0]))+'/'+today1.split("/")[1]
    today=' '+today1
else:
    today=today1

print today


GossDB=Gossipconn()
GossDB.connect()



 
gMP=GossipMenuParser()
gMP.parse_url("https://www.ptt.cc/bbs/Gossiping/index.html")
j=int(gMP.soup.select('.btn')[3]['href'].split('/')[3].split('.')[0].replace('index',''))
while (today in gMP.get_date_list()):
    parserObjects=[]
    gMP.parse_url("https://www.ptt.cc/bbs/Gossiping/index"+str(j)+".html")
    for (url,ps) in zip(gMP.get_url_list(),gMP.push_score_list):
        print url
        gAP=GossipArticleParser(url,ps)
        parserObjects.append(gAP.prepare_query_tuples())
    for i in parserObjects:
        GossDB.submit(i)
    gMP.clean_push_score()
    print j
    j-=1


