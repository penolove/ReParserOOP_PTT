import sys
sys.path.append('..')
sys.path.append('/home/stream/Documents/ptt_web_oop')
from lib.menu_parser import FoodMenuParser
from lib.article_parser import FoodArticleParser
from lib.DBconn import FoodDBconn 

from bs4 import BeautifulSoup
import requests
import os
import datetime

def ptt_date_parser(ptt_date):
    date_list = ptt_date.split(' ')
    date = date_list[4]+'-'+date_list[1]+'-'+date_list[2]
    return datetime.datetime.strptime(date, "%Y-%b-%d")


res=requests.get('https://www.ptt.cc/bbs/Food/index.html')
soup=BeautifulSoup(res.text)
q=soup.select('.wide')[1]['href'].split('/')[3].split('.')[0]
if('index' in soup.select('.wide')[1]['href'].split('/')[3].split('.')[0]):
    newest=q.replace('index','')
    print "newest index is : "+str(newest)
else:
    print "cant't get index.html of food board"
    os._exit(1)

#  f = open('food_current_index.txt','r')
#  q=f.readlines()
#  current_idx=int(q[0].replace('\n',''))+1
#  f.close()
 

menuParser=FoodMenuParser()
parserSubmit=FoodDBconn()


parserSubmit.connect()
parserSubmit.cur.execute("select date from articletable ORDER By articleid DESC LIMIT 300")
latest_list = parserSubmit.cur.fetchall()
latest_list = [ptt_date_parser(i[0]) for i in latest_list]
latest= max(latest_list)
current=latest
parserSubmit.close()
print "print latest date is : "+ latest.strftime("%Y-%m-%d")

count=5000
#curr_record=current_idx
j = int(newest)+1
while True:
    if(count<0):
        break
    print "=========================nextpage===================="
    parserSubmit.connect()
    parserObjects=[]
    menuParser.parse_url('https://www.ptt.cc/bbs/Food/index'+str(j)+'.html')
    urlist=menuParser.get_url_list()
    #MenuParser.get_url_list()
    for i in urlist:
        try:
            fAP=FoodArticleParser(i)
            if fAP.lat!=181:
                current=ptt_date_parser(fAP.get_article_tuple()[2])
                if current > latest:
                    parserObjects.append(fAP.prepare_query_tuples())
        except:
            pass
            print "error "+str(IOError)
    for i in parserObjects:
        parserSubmit.submit(i)
        count=count-1
        if(count<0):
            break
    #curr_record=j
    parserSubmit.close()
    print "current page is : "+'https://www.ptt.cc/bbs/Food/index'+str(j)+'.html'
    print "print current date is : "+ current.strftime("%Y-%m-%d")
    if current<latest:
        break
    j-=1


#  print "the_current_index_is "+str(curr_record)
#  f = open('food_current_index.txt','w')
#  f.write(str(curr_record)+'\n')
#  f.close()
