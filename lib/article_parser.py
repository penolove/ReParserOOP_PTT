# -*- coding: UTF-8 -*-
from parse_class import Parser
from parse_class import GossipParser


from bs4 import BeautifulSoup
import bs4
import random
import googlemaps

class ArticleParser(Parser):
    """the __init__ should be implement in specific class (Food,Gossip)"""
    def get_article_tuple(self):
        """return list with len 5
        [title,Date,Author,Context,url]"""
        try:
            count=0
            a=[];
            for i in self.soup.select('.article-metaline'):
                count=0
                if(count==0):
                    a.append(i.select('.article-meta-value')[0].text.split('(')[0].strip())
                else:
                    a.append(i.select('.article-meta-value')[0].text.strip())
                count=count+1
            #way to get main context
            elem_lists=main_context=self.soup.select('#main-content')[0].contents
            #filter the not realtive elements(e.g. spans)
            fil_elem_list=[ i for i in elem_lists if isinstance(i,bs4.element.NavigableString)]
            main_context = ''.join(fil_elem_list)
            if(len(a)<3):
                a=['','','']
            return [a[1],a[2],a[0],main_context,self.url]
        except IndexError:
            #if parse fail return len=0
            print "ArticleParser->get_article_tuple format error" 
            return []
    
    def get_push_tuple(self):
        """return push tags (url,userid,push-tag,push-content)..."""
        try:
            pushs=self.soup.select('.push')
            pushset=[(self.url ,\
              i.select('.push-userid')[0].text, \
              i.select('.push-tag')[0].text, \
              i.select('.push-content')[0].text[2:]) for i in pushs ]
            return pushset
        except IndexError:
            #if parse fail return len=0
            print "ArticleParser->get_push_tuple format error" 
            return []
    
    def prepare_query_tuples(self):
        print "this function should be implement by subclass"


class FoodArticleParser(ArticleParser):
    """ this class is used to parse Food acrticles in ptt 
        we will get url, address, name(store),lat,lon infomations
        and get infomations that needed in write to postgres DB 
    """
    
    url=""
    address=""
    name=""
    lat=181
    lon=91
    hours=""
    soup=BeautifulSoup()
    def __init__(self,url):
        super(FoodArticleParser, self).__init__()
        self.url=url
        res=self.rs.get(url)
        self.soup=BeautifulSoup(res.text)
        
        main_context=self.soup.select('#main-content')[0].text
        self.address=FoodArticleParser.parse_address(main_context)[0]
        self.name=FoodArticleParser.parse_title(main_context)[0].replace("%", '').replace("'","").replace("$", '')
        tu=FoodArticleParser.getLatLon(self.address)
        self.lat=tu[0]
        self.lon=tu[1]

    @staticmethod
    def parse_address(main_context):
        def check_addr_string(x):
            return ("地".decode('utf-8') in i) and ("址".decode('utf-8') in i)
        def clear_string(x):
            x= x.replace('地'.decode('utf-8'),'')
            x= x.replace('址'.decode('utf-8'),'')
            x= x.replace('：'.decode('utf-8'),'')
            x= x.replace("!@#$%^&*()[]{};:,./<>?\|`~-=_+", '')
            return x.strip()
        w=[clear_string(i) for i in  main_context.split('\n') if check_addr_string(i)  ]
        if len(w)==0:
            return [""]
        return list(set(w))
    
    @staticmethod
    def parse_title(main_context):
        """used to parse title from main context"""
        def check_addr_string(x):
            return ("餐廳名稱".decode('utf-8') in i) or ("店名".decode('utf-8') in i) or ("店家名稱".decode('utf-8') in i)
        def clear_string(x):
            x= x.replace('餐廳名稱'.decode('utf-8'),'')
            x= x.replace('店名'.decode('utf-8'),'')
            x= x.replace('：'.decode('utf-8'),'')
            x= x.replace("!@#$%^&*()[]{};:,./<>?\|`~-=_+\'\"", '')
            return x.strip()
        w=[clear_string(i) for i in  main_context.split('\n') if check_addr_string(i)  ]
        if len(w)==0:
            return [""]
        return list(set(w))
    
    @staticmethod
    def getLatLon(address):
        #1-5
        mykeys=["AIzaSyB3VU7yJZhnfn3yZtWB-Y7OWoh9D1iA8m8",
                "AIzaSyAlowHbmmfIsAAdGywwxiWi-jT6kjwAGQk",
                "AIzaSyBwGh6vpBLsNogMEyoeQk5hGGhSG_DXijs",
                "AIzaSyD_aEKp7K3Bv2j-_YLee_A8U1Mi6juiubI",
                "AIzaSyBGb_1EMRWPrXFuoyrrDCrr12Hx5PjBl7c",
                "AIzaSyAyEzqfl7QiqDTeJNbQMJX4BVgiknqzZsc",
                "AIzaSyC6PjDyAoyKaNiZytZ4X5_rgmK0JumLwbo",
                "AIzaSyB7DNp56xqS26PtOzktydnd9N7MagVyb1s",
                "AIzaSyD4-QT1CjGpoWbNAox4JPmWGypWuDlzTTo",
                "AIzaSyCGwTE-diiJZUhOkSdXw4GpodEI3Cbtivk"
               ]

        #mykey="AIzaSyCGwTE-diiJZUhOkSdXw4GpodEI3Cbtivk"

        if(address==""):
            return (181,91)

        gmaps = googlemaps.Client(key=mykeys[random.randint(0,9 )])
        geocode_result = gmaps.geocode(address)
        lat=geocode_result[0]['geometry']['location']['lat']
        lon=geocode_result[0]['geometry']['location']['lng']
        return (lat,lon)
        
    def __str__(self):
         return "store_name : " + self.name.encode('utf-8') +"\n"+ \
         "address : " + self.address.encode('utf-8') +"\n" + \
         "lat,lon : " + str(self.lat)+" ,"+str(self.lon) +"\n"
        
    def get_store_tuple(self):
        if (self.name==""):
            return (self.address,str(self.lat)+","+str(self.lon),1)
        return (self.address,self.name,str(self.lat)+","+str(self.lon),1)
    
    def get_article_tuple(self):
        a=super(FoodArticleParser,self).get_article_tuple()
        if len(a)==0:
            print "FoodArticleParser->get_article_tuple format error" 
            return []
        return [str(self.lat)+","+str(self.lon),a[0],a[1],a[2],a[3],a[4]]

    
    def prepare_query_tuples(self):
        QT_tuple=[]
        # store
        if(self.lat!=181):
            print self.address
            if(self.name==""):
                store_table_q="""INSERT INTO StoreTable(address,latlon,count) VALUES (%s,%s,%s) ON CONFLICT (latlon) DO UPDATE SET count=StoreTable.count+1"""
            else:
                store_table_q="INSERT INTO StoreTable(address,storeName,latlon,count) VALUES (%s,%s,%s,%s) ON CONFLICT (latlon) DO UPDATE SET count=StoreTable.count+1 , storeName='"+self.name+"'"
            QT_tuple.append( [store_table_q, [self.get_store_tuple()], "Sent to Store Table"])
            
            #article
            _article_tuple=self.get_article_tuple()
            if(len(_article_tuple)>0):
                art_table_q="""INSERT INTO ArticleTable(latlon,title,Date,Author,Context,url) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (url) DO NOTHING"""
                QT_tuple.append([art_table_q, [_article_tuple], "sent to ArticleTable"])
            
            #pushTable
            _push_tuple=self.get_push_tuple()
            if len(_push_tuple)>0:
                art_table_q="""INSERT INTO PushTable(url,userid,pushtag,pushcontext) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
                QT_tuple.append([art_table_q, _push_tuple,"sent to Pushtable"])

        return QT_tuple



import time
years=time.strftime("%Y")
from datetime import datetime
class GossipArticleParser(GossipParser,ArticleParser):
    def __init__(self,url,push_score):
        super(GossipArticleParser, self).__init__()
        self.url=url
        res=self.rs.get(url)
        self.soup=BeautifulSoup(res.text)
        self.push_score=push_score
    def webarticle_tuple(self):
        """return list with len 9 
        [pushcount,date,author,title,context,hyperlink,green,blue,fe]"""
        a=super(GossipArticleParser, self).get_article_tuple()
        #""" it should return [title,Date,Author,Context,url]"""
        if len(a)==0:
            #if parent cls:ArticleParserparse fail return [] len=0
            print "GossipArticleParser->webarticle_tuple article parse fail"
            return []
        url=a[4].replace('https://www.ptt.cc','')

        def date_transform(x):
            date_list=x.split(' ')
            date_list=[i for i in date_list if i !='']
            date_str=date_list[1]+'/'+date_list[2]+'/'+date_list[4]
            date_object = datetime.strptime(date_str, '%b/%d/%Y')
            #re-configure_format
            date_str=date_object.strftime('%Y/%m/%d')
            date_list=date_str.split('/')
            if(int(date_list[1])<10):
                date_str=date_list[0]+'/ '+str(int(date_list[1]))+'/'+date_list[2]
                print date_str
                return date_str
            else:
                print date_list[1]
                print date_str
                return date_str


        try:
            date_tuple=date_transform(a[1])
        except IndexError:
            #if parse fail return len=0
            print "GossipArticleParser->webarticle_tuple article parse fail"
            return []
        return [self.push_score,date_tuple,a[2],a[0],a[3],url,0,0,0]

    def webptt_tuple(self):
        """return [(pushtag,userid,pcontext,pdate,articlekey)....]"""
        def reshpae_date(a):
            return (a[0][2],a[0][1],a[0][3],a[1])
        a=super(GossipArticleParser, self).get_push_tuple()
        if len(a)>0:
            pushs=self.soup.select('.push')
            pushdate=[years+"/"+i.select('.push-ipdatetime')[0].text for i in pushs]
            a=zip(a,pushdate)
            a=[reshpae_date(i) for i in a]
            #"""return push tags (url,userid,push-tag,push-content)..."""
        else:
            print "GossipArticleParser->webptt_tuple pushes  parse fail"
        # if parsen fail also pass a (which is []) out
        return a
    
    def prepare_query_tuples(self):
        QTuples=[self.webarticle_tuple(),self.webptt_tuple()]
        return QTuples
