import sys
sys.path.append('..')
sys.path.append('/home/stream/Documents/ptt_web_oop')
from lib.menu_parser import GossipMenuParser
from lib.article_parser import GossipArticleParser 
from lib.DBconn import Gossipconn

import time

print "kerker"

# get current date
today1=time.strftime("%m/%d")
years=time.strftime("%Y")
if(int(today1.split("/")[0])<10):
    today1=str(int(today1.split("/")[0]))+'/'+today1.split("/")[1]
    today=' '+today1
else:
    today=today1

print today
check_today=years+'/'+today
print years+'/'+today

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
        if len(i[0])==9 and len(i[1])!=0 and i[0][1]==check_today:
            print "day_checked, format checked : pass."
            GossDB.submit(i)
        else:
            print "date_check/format check : fail"
    gMP.clean_push_score()
    print j
    j-=1

f=open('datetemp.txt','w')
f.write(check_today)
f.close
