import socket,sys,select
host='localhost'
port=51423

spinsize=10
spinpos=0
spindir=1

def spin():
	global spinsize,spinpos,spindir
	spindir='.'*spinpos+\
		'|'+'.'*(spinsize-spinpos-1)
	sys.stdout.write('\r'+spinstr+' ')
	sys.stdout.flush()

	spinpos+=spindir
	if spinpos<0:
		spindir=1
		spinpos=1
	elif spinpos>=spinsize:
		spinpos-=2
		spindir=-1

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

p=select.poll()
p.register(s.fileno(),select.POLLIN|select.POLLERR|select.POLLHUP)
while 1:
	result=p.poll(50)
	if len(results):
		if results[0][1]==select.POLLIN:
			data=s.recv[4096]
			if not len(data):
				print("\rRemote end closed connection;existing.")
				break
			# Only one item in here -- if there is anything,it's for us.
			sys.stdout.write("\rReceive: "+data)
			sys.stdout.flush()
	else:
		print "\rProgram occurred;exiting."
		sys.exit(0)
spin()
