#coding:utf-8
import message_pb2 as message
import pymssql as mssql_module
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
conn=mssql_module.connect(host='210.45.212.119',user='sa',password='admin@txsys2013',database='CPDB')
#conn=mysql_module.connect(host='172.24.9.35',port=1433,user='sa',password='123456',database='CPDB')
cur=conn.cursor()
cur.execute('select * from [dbo].[TIMERMONITORINFO]')
#print(cur.fetchall())
r=cur.fetchone()
i=1
f=open('timemonitordata.txt','a')#区分a模式和w模式
while r:
	id,depotid,content,type=r

	usinfo=message.TimerInstructRequestMsg()
	usinfo.ParseFromString(content)
	print(usinfo)
	f.write(str(usinfo))
	f.write('\n')
	r=cur.fetchone()
	i+=1
f.close()
cur.close()
conn.close()
