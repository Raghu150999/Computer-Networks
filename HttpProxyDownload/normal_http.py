import socket
import base64
import ssl

MB = 65535

url = 'www.google.com'

address = (socket.gethostbyname(url), 443)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap socket for SSL (needed for making HTTPS connection)
sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
sock.connect(address)

req = \
    "GET / HTTP/1.1\r\n" + \
    "host: {}\r\n".format(url) + \
    "connection: close\r\n" + \
    "accept: text/html\r\n" + \
    "\r\n"

print(req)
req = req.encode('utf-8')
sock.sendall(req)

data = b''
while True:
    reply = sock.recv(65535)
    if not reply:
        break
    data = data + reply
    reply = reply.decode('utf-8', 'ignore')

print(data.decode('utf-8', 'ignore'))
l = data.find(b'<!doctype html>')
r = data.find(b'</html>') + 7
data = data[l:r]

# f = open('index.html', "wb")
# f.write(data)
# f.close()