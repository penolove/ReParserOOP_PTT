import psycopg2
import sqlite3


class Abs_DBconn(object):
    conn = None
    cur = None
    def submit(self,query_tuples_info):
        pass
    def connect(self):
        pass
    def reconnect(self):
        self.close()
        self.connect()
        
    def close(self):
        pass


class FoodDBconn(Abs_DBconn):
    def submit(self,query_tuples_info):
        for i in query_tuples_info:
            print i[2]
            self.cur.executemany(i[0],i[1])
        self.conn.commit()
    def connect(self):
        self.conn = psycopg2.connect("dbname='foodmining' user='penolove' host='localhost' password='password'")
        self.cur = self.conn.cursor()
    def close(self):
        self.conn.close()


class Gossipconn(Abs_DBconn):
    def submit(self,query_tuples_info):
        #check article query sucessfully
        if(len(query_tuples_info[0])==9 and len(query_tuples_info[1])!=0):
            check_parsen='SELECT hyperlink FROM webarticle where hyperlink = "'+query_tuples_info[0][5]+'"'
            self.curs.execute(check_parsen)
            li= self.curs.fetchall()
            print "DB has parsen check : "+ str(len(li))
            if(len(li)==0):
                self.curs.execute("INSERT INTO webarticle VALUES (?,?,?,?,?,?,?,?,?)",(query_tuples_info[0]))
                self.curs.execute("SELECT COUNT(*) FROM webarticle")
                xy= self.curs.fetchall()
                print "current rowid : "+str(xy)
                for push_ in query_tuples_info[1]:
                    if len(push_)==4:
                        trans=[x for x in push_]
                        trans.append(xy[0][0])
                        self.curs.execute("INSERT INTO webptt VALUES (?,?,?,?,?)", trans)
                    else:
                        print "the format for push_tuples are wrong"
                self.conn.commit()
        else:
            print "there are parse issue, tuples_len : "+str(len(query_tuples_info[0]))+", push_tuple_len : "+str(len(query_tuples_info[1]))
    def connect(self):
        self.conn = sqlite3.connect('/home/stream/Documents/kerkerman88/starbucks.sqlite')  #link
        self.curs = self.conn.cursor() 
    def close(self):
        self.conn.close()
