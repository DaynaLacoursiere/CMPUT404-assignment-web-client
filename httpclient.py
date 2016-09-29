#!/usr/bin/env python
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
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        if port is None:
            port = 80
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host,port))
        # use sockets!
        return client

    def get_code(self, data):
        print("herehereherehere")
        print "GET code from:",data
        print data
        code = int(data.split(' ')[1])
        return code

   
    # TODO: parse out headers from data
    def get_headers(self,data):
        return None

    def get_body(self, data):
        body = data.split ("\r\n\r\n",1)[1]
        return body

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
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        # TODO: Add a try/except for invalid urls

        parsedurl = urlparse(url)

        if parsedurl.hostname:
            # case: http://www.google.ca/
            hostname = parsedurl.hostname
        else:
            # case: www.google.ca
            hostname = parsedurl.path


        client = self.connect(hostname,parsedurl.port)

        http_request = 'GET '+ url +' HTTP/1.0\r\n\r\n'
        http_request += 'Host:' + hostname + '\r\n'
        http_request += 'Accept: */*\r\n'
        http_request += 'Connection: Close\r\n'
        http_request += '\r\n'
        http_request += '\r\n'


        client.send(http_request)
        # theoretically, these lines will work once the headers are right
        msg = self.recvall(client)
        code = self.get_code(msg)
        body = self.get_body(msg)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        print("POSTS ARE STARTING NOW")
        code = 500
        body = ""
        # TODO: Add a try/except for invalid urls

        parsedurl = urlparse(url)

        if parsedurl.hostname:
            # case: http://www.google.ca/
            hostname = parsedurl.hostname
        else:
            # case: www.google.ca
            hostname = parsedurl.path


        client = self.connect(hostname,parsedurl.port)

        # TODO: figure out args for POST

        http_request = 'POST '+ url +' HTTP/1.0\r\n\r\n'
        http_request += 'Host:' + hostname + '\r\n'
        http_request += 'Accept: */*\r\n'
        http_request += '\r\n'
        http_request += '\r\n'
        # TODO: Add other headers to http_request here
     
        client.sendall(http_request)
        # theoretically, these lines will work once the headers are right
        msg = self.recvall(client)
        code = self.get_code(msg)
        body = self.get_body(msg)

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
        # if you run python httpclient.py
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        # if you run python httpclient.py POST/GET www.url.com
        print client.command( sys.argv[2], sys.argv[1] )
    elif (len(sys.argv) == 4):
        # if you run python httpclient.py POST/GET www.url.com "param1=value1&param2=value2"
        print "NOT IMPLEMENTED YET"
        sys.exit(1)

        """
        Might not be necessary -- not in freetests.py
        TODO:
            from:
                "param1=value1&param2=value2"
            to:
                {
                    "param1" : value1,
                    "param2" : value2
                }
        """
        args = makeJSON(sys.argv[3])
        print client.command( sys.argv[2], sys.argv[1], args)
    else:
        # if you run python httpclient.py www.url.com
        print client.command( sys.argv[1] )  
