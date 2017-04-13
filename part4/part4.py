import socket
import os,time
from threading import Thread
import re

template = """HTTP/1.1 200 OK
{headers}

{content}"""


class RequestThread(Thread):

    def __init__(self, threadNo, thread_connection):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.connection = thread_connection
        self.authenticated = False
        self.usrname = ""
        self.passwd = ""

    def extractCookies(self, string):

        cookies = dict()
        raw_cookies = string.split(' ')
        for raw_cookie in raw_cookies:
            cookie = raw_cookie.split('=')
            cookies[cookie[0]] = cookie[1]
        return cookies

    def sendLoginPage(self, request, cookies):

        with open("login.html") as f:
            data = f.read()
            head = 'Set-Cookie: nextpage = ' + request["GET"] + ";"
            if "nextpage" in cookies and cookies["nextpage"] != "deleted;":
                head = 'Set-Cookie: nextpage = ' + cookies["nextpage"] + ";"

            http_response = template.format(headers=head, content=data)
            self.connection.sendall(http_response)

    def run(self):

        raw_request = self.connection.recv(1024)
        print raw_request

        request = GetRequestDict(raw_request)

        cookies = dict()

        if "POST" in request and request["POST"] == "checkme":
            auth = self.checkCredential(raw_request)
            cookies = self.extractCookies(request["Cookie:"])
            request["GET"] = cookies["nextpage"][:-1]
            if auth is True:
                head = "Set-Cookie: authenticated = 1;"
                http_response = handleRequest(request, head)
                self.connection.sendall(http_response)
            else:
                self.sendLoginPage(request, cookies)

        elif "Cookie:" in request:
            cookies = self.extractCookies(request["Cookie:"])

            if "authenticated" in cookies and bool(int(cookies["authenticated"][0])) is True:
                head = "Set-Cookie: authenticated = 1;"
                if "GET" in request and request["GET"] == "logout":
                    page = "deleted"
                    head = "Set-Cookie: authenticated = 0;\nSet-Cookie: nextpage = " + page + ";"
                http_response = handleRequest(request, head)
                self.connection.sendall(http_response)
            else:
                self.sendLoginPage(request, cookies)

        else:
            self.sendLoginPage(request, cookies)

        print "Thread is closing", self.threadNo
        self.connection.close()

    def checkCredential(self, request):

        usrname = re.findall('Username=(.*?)&Password', request)
        passwd = re.findall('&Password=(.*?)$', request)

        auth_pass = False
        f = open("credentials.txt",'rb')
        data = f.read(1024)
        lines = data.split('\n')
        for line in lines:
            if line != "":
                words = line.split(' ')
                if words[0] == usrname[0] and words[1] == passwd[0]:
                    auth_pass = True
                    break

        return auth_pass

def GetRequestDict(request):
    ret = dict()
    requestlist = request.split('\n')
    for requestelement in requestlist:
        Headers = requestelement.split(' ',1)
        if len(Headers) >= 2:
            ret[Headers[0]] = Headers[1]
            if Headers[0]=="GET":
                ret["GET"] = ret["GET"].split(' ')[0][1:]
            elif Headers[0]=="POST":
                ret["POST"] = ret["POST"].split(' ')[0][1:]

    return ret

def handleRequest(request, head):

    if request["GET"] == "logout":
        http_response = template.format(headers=head, content="Logout Sucessfully!!!!!")
    elif request["GET"] not in os.listdir("./"):
        http_response = template.format(headers=head, content="404 Not Found")
    else:
        with open(request["GET"]) as f:
            data = f.read()
            http_response = template.format(headers=head, content=data)

    return http_response


HOST, PORT = '', 9991

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
