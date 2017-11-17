#coding:utf-8
from htmlentitydefs import entitydefs
from HTMLParser import HTMLParser
import sys,re,urllib2

#interesting=['Day Forecast for ZIP']
interesting=['合肥一周天气']

class WeatherParser(HTMLParser):
	def __init__(self):
		#存储解析树
		self.taglevels=[]     
		#self.handledtags=['title','table','tr','td','th'] #感兴趣的标签列表
		self.handledtags=['title','table','li','div','p']
		self.processing=None
		self.interesting=0            #如果当前正在处理有趣表格，就设为TRUE
		self.row=[]     #如果正在处理有趣表格，保持当前行中的单元格
		HTMLParser.__init__(self)

	def handle_starttag(self,tag,attrs):
	#无论何时，只要系统出现了开始标签，系统就会在taglevels中记录下来；
		if len(self.taglevels) and self.taglevels[-1]==tag:     
			self.handle_endtag(tag)				
		self.taglevels.append(tag)
		if tag=='br':
			self.handle_data("<NEWLINE>")  #换行标签
		elif tag in self.handledtags:
			self.data=''
			self.processing=tag  #如果标签是程序处理的五种之一，就在self.processing设置标记							来通知系统开始记录数据。

	def handle_data(self,data):
		if self.processing:
			self.data+=data	 #开始记录数据

	def handle_endtag(self,tag):
	#程序会首先检查在查询中是否存在一个和结束标签对应的起始标签，如果没有，就会略过标签；如果看到了		标签，它就会找到最近出现的那个。它是从self.taglevels列表的末端开始，从后往前工作的。
		if not tag in self.taglevels:
			return

		while len(self.taglevels):
			starttag=self.taglevels.pop()   #获得清单里的最后一个标签并将它移除

			if starttag in self.handledtags:
				self.finishprocessing(starttag)	  #如果发现有趣标签，就会调用函数
			if starttag==tag:
				break

	def cleanse(self):
		self.data=re.sub('(\s|\xa0)+',' ',self.data)         #把文档里多余空格去掉
		self.data=self.data.replace('<NEWLINE>',"\n").strip() #用真实的newline字符替换<NEWLINE>

	def finishprocessing(self,tag):
		global interesting
		self.cleanse()
		if tag=='title' and tag==self.processing:
			print "*** %s ***" % self.data         #打印出网页的标题
		elif (tag=='td' or tag=='th' and tag==self.processing):
		#elif(tag=='li' or tag=='div' and tag==self.processing):
		#得到有趣表格的一个单元格

			if not self.interestingtable:     #如果还没处于有趣表格中，看看这个单元格是否可												以使表格有趣
				for item in interesting:
					if re.search(item,self.data,re.I):
					#当找到一个有趣表格时，标记它，并将它从有趣清单里移除，打印出头							   			部，并停止在清单里继续寻找
						self.interestingtable=1
						interesting=[x for x in interesting if x !=item]
						print "\n *** %s\n" % self.data.strip()
						break
					else:	#如果已经处于有趣表格时，仅仅将这个单元格加入到当前行中
						self.row.append(self.data)
			#elif tag=='tr' and self.interestingtable:
			elif tag=='p' and self.interestingtable:
			#打印出有趣的行
				self.writerow()
				self.row=[]
			elif tag=='table':
			#在表格的最后，系统已经不再处理这个有趣表格
				self.interestingtable=0
			self.processing=None

	def writerow(self):  #实现了实际的输出
		#设计一个用来在屏幕上展现的行
		cells=len(self.row)
		if cells<2:
			return
		if cells>2:
			width=(78-cells)/cells
			maxwidth=width
		else:
			width=20	#如果一个表格只有两个单元格，让左边的单元格窄一点，右边的宽一点
			maxwidth=58

		while [x for x in self.row if x!='']:
			for i in range(len(self.row)):
				thisline=self.row[i]
				if thisline.find("/n")!=-1:
				   #如果有很多排，我们只要第一排并保存，剩余的保存进清单中方便下次处理
					(thisline,self.row[i])=self.row[i].split("\n",1)
				else:
				   #如果仅有一排，并且已经保存了，那么将清单中标记空字符
					self.row[i]=''
				thisline=thisline.strip()
				sys.stdout.write("%-*.*s" %(width,maxwidth,thisline))
			sys.stdout.write("\n")

	def handle_charref(self,name):		#转换字符参考
		try:
			charnum=int(name)
		except ValueError:
			return

		if charnum<1 or charnum>255:
			return
		self.handle_data(char(charnum))

#sys.stdout.write("Enter ZIP code:")
#zip=sys.stdin.readline().strip()
#url="http://www.wunderground.com/cgi-bin/findweather/getForecast?query="+\zip
url="http://tianqi.sogou.com/hefei/"
#url="https://www.wunderground.com/weather/us/tx/77002"

req=urllib2.Request(url)
fd=urllib2.urlopen(req)

parser=	WeatherParser()
data=fd.read()
data=re.sub('([^=]+)=[^="]','\\1="',data)	#这个输入文档中包含了一些违反HTML的代码，这些代码不能用
						#	HTMLPsrser处理，所以用正则表达式来处理
data=re.sub('(?s)<!--.*?-->','',data)
parser.feed(data)
