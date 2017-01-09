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
        pass
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
    def reconnect(self):
        self.conn.close()
        self.conn = psycopg2.connect("dbname='foodmining' user='penolove' host='localhost' password='password'")
        self.cur = self.conn.cursor()
    def close(self):
        self.conn.close()


class Gossipconn(Abs_DBconn):
    def submit(self,query_tuples_info):
        self.curs.execute("INSERT INTO webarticle VALUES (?,?,?,?,?,?,?,?,?)",(query_tuples_info[0]))
        self.curs.execute("SELECT COUNT(*) FROM webarticle")
        xy= self.curs.fetchall()
        print "current rowid : "+str(xy)
        for push_ in query_tuples_info[1]:
            trans=[x for x in push_]
            trans.append(xy[0][0])
            self.curs.execute("INSERT INTO webptt VALUES (?,?,?,?,?)", trans)
        self.conn.commit()
    def connect(self):
        self.conn = sqlite3.connect('/home/stream/Documents/kerkerman88/starbucks.sqlite')  #link
        self.curs = self.conn.cursor() 
    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect('/home/stream/Documents/kerkerman88/starbucks.sqlite')  #link
        self.curs = self.conn.cursor() 
    def close(self):
        self.conn.close()
