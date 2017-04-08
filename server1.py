import socket
import os

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
    return ret





HOST, PORT = '', 80

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print request

    request = GetRequestDict(request)
    print os.listdir("./"), request["GET"]

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



    client_connection.sendall(http_response)
    client_connection.close()
