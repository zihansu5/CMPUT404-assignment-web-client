#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        try:
            code = int(data.split()[1])  
            return code
        except:
            return None

    def get_headers(self,data):
        try:
            header_list = data.split('\r\n\r\n')[0].split('\r\n')[1:]
            headers = []
            for header in header_list:
                header_info = header.split()
                headers.append((header_info[0], header_info[1]))
            return headers
        except:
            return None

    def get_body(self, data):
        try:
            body = data.split('\r\n\r\n')[1]
            return body
        except:
            return None

    def parse_url(self, url):
        host = urllib.parse.urlparse(url).hostname
        port = urllib.parse.urlparse(url).port
        path = urllib.parse.urlparse(url).path
        if port == None:
            port = 80       # HTTP Client application should use port 80
        if path == '':
            path = '/'
        return host, port, path

    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        host, port, path = self.parse_url(url)
        # connect
        self.connect(host, port)
        # request
        playload = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: */*\r\nConnection: close\r\n\r\n'
        self.sendall(playload)
        #self.socket.shutdown(socket.SHUT_WR)
        # receive data
        data = self.recvall(self.socket)
        #close
        self.close()

        #print(data)
        code = self.get_code(data)
        body = self.get_body(data)
        print('-----------------GET-body-----------------')
        print(body)
        print('------------------------------------------\r\n\r\n')
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host, port, path = self.parse_url(url)
        # connect
        self.connect(host, port)
        # request
        if args == None:
            request = f'POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 0\r\n\r\n'
        else:
            query = urllib.parse.urlencode(args)
            request = f'POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(query)}\r\n\r\n{query}\r\n'
        self.sendall(request)
        # receive data
        data = self.recvall(self.socket)
        #close
        self.close()

        #print(data)
        code = self.get_code(data)
        body = self.get_body(data)
        print('-----------------POST-body-----------------')
        print(body)
        print('-------------------------------------------\r\n\r\n')
        

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
