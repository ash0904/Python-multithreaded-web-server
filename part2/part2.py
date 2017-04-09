import socket
import os,time
from threading import Thread

class RequestThread(Thread):

    def __init__(self, threadNo, thread_connection):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.connection = thread_connection

    def run(self):
        request = self.connection.recv(1024)
        print request

        request = GetRequestDict(request)
        http_response = handleRequest(request)

        #print http_response
        self.connection.sendall(http_response)
        self.connection.close()
        time.sleep(60)
        print "Thread is closing", self.threadNo

def GetRequestDict(request):
    ret = dict()
    requestlist = request.split('\n')
    for requestelement in requestlist:
        Headers = requestelement.split(' ')
        if len(Headers) >= 2:
            ret[Headers[0]] = Headers[1]
            if Headers[0]=="GET":
                ret["Version"] = Headers[2]
                ret["GET"] = ret["GET"][1:]

        elif len(Headers) == 1:
            if "POST" in ret:
                var = re.split('& |=', Headers[0])
                if len(var) == 4:
                    ret[var[0]] = var[1]
                    ret["filename"] = var[3]
                #Headers = Headers.split('&')

    return ret

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



HOST, PORT = '10.1.37.78', 9991

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

    """
    pid = os.fork()

    if pid == 0:
        request = client_connection.recv(1024)
        print request

        request = GetRequestDict(request)

        http_response = ""
        if "GET" in request:
            http_response = handleRequest(request)
        #elif "Post" in request:
        #    http_response = handleUpload(request)

        client_connection.sendall(http_response)
        time.sleep(60)

    else:
        client_connection.close()
    """
