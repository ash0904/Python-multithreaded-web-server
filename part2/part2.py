import socket
import os,time
from threading import Thread
# import difflib
class RequestThread(Thread):

    def __init__(self, threadNo, thread_connection):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.connection = thread_connection

    def run(self):
        request = self.connection.recv(1024)
        print request

        request,method = GetRequestDict(request)
        if method == "POST":
            http_response = """\
HTTP/1.1 200 OK

"""
            wflag = 1
            while wflag:
                request = self.connection.recv(1024)
                requestlist = request.split('\n')
                for requestelement in requestlist:
                    Headers = requestelement.split(' ')
                    print requestelement
                    if Headers[0] == "Content-Disposition:":
                        print "breaking"
                        wflag = 0
                        break
            a = self.connection.recv(1024)
            print "Printing a :", a
            http_response = """\
HTTP/1.1 200 OK

<html>
<body>
Uploaded cheers!
<br>
<a href= "http://10.1.37.98:9991/upload.html"> Upload Again </a>
</body>
</html>
"""
            self.connection.sendall(http_response)
        else:
            http_response = handleRequest(request)
            self.connection.sendall(http_response)

        #print http_response
        self.connection.close()
        time.sleep(60)
        print "Thread is closing", self.threadNo

def GetRequestDict(request):
    ret = dict()
    requestlist = request.split('\n')
    for requestelement in requestlist:
        Headers = requestelement.split(' ')
        if Headers[0] == "Content-Disposition:":
            ret["filename"] = Headers[3][10:len(Headers[3])-2]
            method = "POST"
        elif len(Headers) >= 2:
            ret[Headers[0]] = Headers[1]
            if Headers[0]=="GET":
                method = "GET"
                ret["Version"] = Headers[2]
                ret["GET"] = ret["GET"][1:]

    return ret,method

def handleRequest(request):
    if request["GET"] not in os.listdir("./"):
        http_response = """\
HTTP/1.1 200 OK

404 Not Found!
"""
    else:
        with open(request["GET"]) as f:
            http_response = """\
HTTP/1.1 200 OK

"""
            for line in f:
                http_response += line

    return http_response

def handleUpload(request):

    if "filename" in request:

        data = self.rfile.read(content_length)
        with open(request["filename"], 'wb') as fw:
            f.write(data)



HOST, PORT = '10.1.37.98', 9991

socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_listen.bind((HOST, PORT))
socket_listen.listen(1)
print 'Serving HTTP on port %s ...' % PORT

requestList = list()

while True:
    client_connection, client_address = socket_listen.accept()

    newRequest = RequestThread(len(requestList), client_connection)
    newRequest.start()
    requestList.append(newRequest)

    for request in requestList:
        if not request.isAlive():
            requestList.remove(request)
            request.join()
