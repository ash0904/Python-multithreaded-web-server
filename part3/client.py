from socket import *
import sys

if (len(sys.argv)!=4):
	print "give host, port, and filename as command line argument"
	exit()

host = sys.argv[1]
port = int(sys.argv[2])
filename = sys.argv[3]
hostPort = "%s:%s" %(host, port)

try:
	clientConn = socket(AF_INET,SOCK_STREAM)
	clientConn.connect((host,port))
	Headers = {
	"GET" : " /%s HTTP/1.1" %(filename),
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "en-us",
	"Host": hostPort,
	}
	request = "\r\n".join("%s%s" %(item,Headers[item]) for item in Headers)
	clientConn.send("%s\r\n\r\n" %(request))
	print request
except IOError:
	print "There is some error connecting to server"
	sys.exit(1)

final=""
responseMessage=clientConn.recv(1024)
while responseMessage:
	final += responseMessage
	responseMessage = clientConn.recv(1024)

clientConn.close()
print "final:",final
