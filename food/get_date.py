import sys
sys.path.append('..')
sys.path.append('/home/stream/Documents/ptt_web_oop')
from lib.DBconn import FoodDBconn 
import datetime
parserSubmit=FoodDBconn()
parserSubmit.connect()


parserSubmit.cur.execute("select date from articletable ORDER By articleid DESC LIMIT 10")
latest_list = parserSubmit.cur.fetchall()
latest_list = [i[0].split(' ') for i in latest_list]
latest_list = [i[4]+'-'+i[1]+'-'+i[2] for i in latest_list]
latest_list = [datetime.datetime.strptime(i, "%Y-%b-%d") for i in latest_list]
latest= max(latest_list)
current=datetime.datetime.strptime('2017-Jan-25', "%Y-%b-%d")
print current > latest
parserSubmit.close()
