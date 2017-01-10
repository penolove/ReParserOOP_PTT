import sys
sys.path.append('..')
from lib.menu_parser import FoodMenuParser
from lib.article_parser import FoodArticleParser
from lib.DBconn import FoodDBconn 

from bs4 import BeautifulSoup
import requests
import os


res=requests.get('https://www.ptt.cc/bbs/Food/index.html')
soup=BeautifulSoup(res.text)
q=soup.select('.wide')[1]['href'].split('/')[3].split('.')[0]
if('index' in soup.select('.wide')[1]['href'].split('/')[3].split('.')[0]):
  newest=q.replace('index','')
else:
    print "cant't get index.html of food board"
    os._exit(1)

f = open('food_current_index.txt','r')
q=f.readlines()
current_idx=int(q[0].replace('\n',''))+1
f.close()
 

menuParser=FoodMenuParser()
parserSubmit=FoodDBconn()
count=21000
for j in range(current_idx,int(newest)+2):
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
            parserObjects.append(fAP.prepare_query_tuples())
        except:
            pass
        
    for i in parserObjects:
        parserSubmit.submit(i)
        count=count-1
        if(count<0):
            break
            
    parserSubmit.close()
    
print "the_current_index_is "+str(j)

f = open('food_current_index.txt','w')
f.write(str(j)+'\n')
f.close()
