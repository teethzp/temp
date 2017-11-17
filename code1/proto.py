#coding:utf-8
import sys
import message_pb2 as message
import pymssql as mssql_module
reload(sys)
sys.setdefaultencoding('utf-8')
conn=mssql_module.connect(host='210.45.212.119',user='sa',password='admin@txsys2013',database='CPDB')
cur=conn.cursor()
cur.execute('select * from [dbo].[TIMERMONITORINFO]')
r=cur.fetchone()
#print(cur.fetchall())
i=1
f=open('timemonitordata.txt','a')
while r:
	depotid,type,content,id=r
	usinfo=message.TimerInstructRequestMsg()
	usinfo.ParseFromString(content)

	print(usinfo)
	f.write(str(usinfo))
	#f.write(depotid)
	#f.write(',')
	#f.write(type)
	#f.write(',')
	#f.write(content)
	f.write('\n')
	r=cur.fetchone()
	i+=1
f.close()
cur.close()
conn.close()

