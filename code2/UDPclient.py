#UDP Example -Chapter 2-udp.py

import socket,sys

host=sys.argv[1]
textport=sys.argv[2]
#host="127.0.0.1"
#textport=54312
#print("start:")
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
try:
    port=int(textport)
except ValueError:
    #That did not work.Please look it up instead.
    port=socket.getservbyname(textport,'udp')

s.connect((host,port))
print "Enter data to transmit: "
data=sys.stdin.readline().strip()
s.sendall(data)
print "Looking for replies;press Ctrl-C or Ctrl-Bleak to stop."
while 1:
	buf=s.recv(2048)
	if not len(buf):
		bread
	sys.stdout.write(buf)
	
	
#While 1:
#    buf=s.recv(2048)
#    if not len(buf):
#        braek
#    sys.stdout.write(buf)
