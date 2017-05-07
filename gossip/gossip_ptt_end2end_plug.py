import sys
sys.path.append('..')
from lib.menu_parser import GossipMenuParser
from lib.article_parser import GossipArticleParser 
from lib.DBconn import Gossipconn

import time




# get current date should be look like
" 1/10"
"10/15"
"12/13"
today=" 3/21"
years="2017"

print "current parsing"+ today
check_today=years+'/'+today
print years+'/'+today

GossDB=Gossipconn()
GossDB.connect()



 
gMP=GossipMenuParser()
#here need to change the url to the date you want
gMP.parse_url("https://www.ptt.cc/bbs/Gossiping/index21042.html")
j=21042

while (today in gMP.get_date_list()):
    parserObjects=[]
    gMP.parse_url("https://www.ptt.cc/bbs/Gossiping/index"+str(j)+".html")
    for (url,ps) in zip(gMP.get_url_list(),gMP.push_score_list):
        print url
        gAP=GossipArticleParser(url,ps)
        parserObjects.append(gAP.prepare_query_tuples())
    for i in parserObjects:
        if i[0][1]==check_today:
            print "day_checked"
            GossDB.submit(i)
    gMP.clean_push_score()
    print j
    j-=1


f=open('datetemp.txt','w')
f.write(check_today)
f.close
