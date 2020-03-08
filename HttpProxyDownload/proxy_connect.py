import socket
import base64
import ssl
import argparse
from html_parsing import html_parser

MB = 65535

def make_request(args, get, mute=False):
    '''
    Creates connection request to proxy to url specified in args
    Args:
        get: specifies the GET request field
    
    Returns:
        Data section of the HTTP response as bytes
    '''

    url = args.url

    address = (args.ip, args.port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    key = "{}:{}".format(args.user, args.passw)
    # Encode credentials to base64
    hashed_key = base64.b64encode(key.encode('utf-8')).decode('utf-8')

    # Use port 80 -> HTTP, 443 -> HTTPS
    port = 443

    # Connection request to proxy server
    req = \
        "CONNECT {}:{} HTTP/1.1\r\n".format(url, port) + \
        "host: {}:{}\r\n".format(url, port) + \
        "proxy-connection: keep-alive\r\n" + \
        "proxy-authorization: Basic {}\r\n".format(hashed_key) + \
        "\r\n"

    if not mute:
        print(req)
    req = req.encode('utf-8')
    sock.sendall(req)
    reply = sock.recv(MB)

    if not mute:
        print(reply.decode('utf-8'))

    # HTTPS connection request
    req = \
        f"GET {get} HTTP/1.1\r\n" + \
        f"host: {url}\r\n" + \
        "connection: close\r\n" + \
        "\r\n"

    # Wrap socket for SSL (needed for making HTTPS connection)
    sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)

    # Send request
    sock.sendall(req.encode('utf-8'))

    # Receive response
    response = b''
    while True:
        reply = sock.recv(65535)
        if not reply:
            break
        response = response + reply
    idx = response.find(b'\r\n\r\n')
    idx += 4

    # Response header
    if not mute:
        print(response[:idx].decode('utf-8', 'ignore'))
    
    if args.v and not mute:
        print('Data section:') 
        print(response[idx:])
    
    data = response[idx:]
    return data

if __name__ == "__main__":

    parser = argparse.ArgumentParser('HTTP client for making request through proxy server')
    parser.add_argument('url', nargs='?', default='www.google.com', help='URL for making request')
    parser.add_argument('ip', nargs='?', default='172.16.108.14', help='IP address of proxy')
    parser.add_argument('port', nargs='?', default=3128, help='PORT of proxy', type=int)
    parser.add_argument('user', nargs='?', default='csf303', help='username for proxy authentication')
    parser.add_argument('passw', nargs='?', default='csf303', help='password for proxy authentication')
    parser.add_argument('-v', action='store_true', help='prints data section of response')
    parser.add_argument('--odir', default='output_dir', help='specify output directory (default use: "output_dir")')
    args = parser.parse_args()

    # GET html main page
    data = make_request(args, '/')

    # Save html file
    with open(f'{args.odir}/index.html', 'wb') as f:
        f.write(data)
    
    # Decode for parsing
    doc = data.decode('utf-8', 'ignore')

    # Make request to retrieve all images
    img_srcs = html_parser(doc)
    for i, img in enumerate(img_srcs):
        data = make_request(args, img, mute=False)
        with open(f'{args.odir}/img{i+1}.png', 'wb') as f:
            f.write(data)
