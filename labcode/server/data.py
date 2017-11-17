#coding:utf-8
import pymssql,pickle

class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host=host
	self.user=user
	self.pwd=pwd
	self.db=db

    def _GetConnect(self):
        if not self.db:
	    raise(NameError,"have not set server information")
	self.conn=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
	cur=self.conn.cursor()
	if not cur:
	    raise(NameError,"Failed to connect to server")
	else:
	    return cur

    def ExecQuery(self,sql):
        cur=self._GetConnect()
	cur.execute(sql)
	resList=cur.fetchall()

	self.conn.close()
	return resList

    def ExecNonQuery(self,sql):
        cur=self._GetConnect()
	cur.execute(sql)
	self.conn.commit()
	self.conn.close()

ms=MSSQL(host="210.45.212.119",user="sa",pwd="admin@txsys2013",db="CPDB")
reslist=ms.ExecQuery("select * from TIMERMONITORINFO")
#with open('reslist.TIMERMONITORINFO','rb') as f1:
#	aa=pickle.load(f1)
#	print(aa)
#for i in reslist:
#    print i

        
