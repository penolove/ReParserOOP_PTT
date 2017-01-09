import time

from lib.menu_parser import GossipMenuParser

today1=time.strftime("%m/%d")
years=time.strftime("%Y")

if(int(today1.split("/")[0])<10):
    today1=str(int(today1.split("/")[0]))+'/'+today1.split("/")[1]
    today=' '+today1
else:
    today=today1

print today



gMP=GossipMenuParser()
gMP.parse_url("https://www.ptt.cc/bbs/Gossiping/index.html")
j=int(gMP.soup.select('.btn')[3]['href'].split('/')[3].split('.')[0].replace('index',''))
while (today in gMP.get_date_list()):
    gMP.parse_url("https://www.ptt.cc/bbs/Gossiping/index"+str(j)+".html")
    gMP.clean_push_score
    print j
    j-=1
