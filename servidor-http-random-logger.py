#!/usr/bin/python

#
# Simple HTTP Server Random
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Returns an HTML page with a random link

import socket
import random
import sys
import os
import datetime
import email.Utils

# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

myPort = 1234

some_HTTPHeaders = "Server: Random/1.0\r\n" + \
"Content-Language: en\r\n" + \
"Content-Type: text/html;charset=utf-8\r\n"

mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind((socket.gethostname(), myPort))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Initialize random number generator (not exactly needed, since the
# import of the module already is supposed to do that). No argument
# means time is used as seed (or OS supplied random seed).
random.seed()

# Reopen stdout without buffering, to get synchronous output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

# Accept connections, read incoming data, and answer back an HTLM page
#  (in a loop)
try:
    while True:
        print 'Waiting for connections'
        (recvSocket, address) = mySocket.accept()
        print 'HTTP request received:',
        print datetime.datetime.now().isoformat(),
        print address
        print
        print recvSocket.recv(2048)
        
        # Resource name for next url
        nextPage = str (random.randint (0,100000))
        nextUrl = "/" + nextPage
        # HTML body of the page to serve
        htmlBody = "<!DOCTYPE html><html lang='en'><head>" \
                + "<meta charset='utf-8'/></head>" \
                + "<body><h1>It works!</h1>" \
                + "<p>Next page: <a href='" \
                + nextUrl + "'>" + nextPage + "</a></p></body></html>"
        content_line = "Content-Length: " + str(len(htmlBody)) + "\r\n"
        date_line = "Date: " + email.Utils.formatdate(usegmt = True) + "\r\n"
        httpResponse = "HTTP/1.1 200 OK\r\n" \
                       + some_HTTPHeaders \
                       + date_line \
                       + content_line + "\r\n" \
                       + htmlBody
        #print httpResponse
        recvSocket.send(httpResponse)
        recvSocket.close()

except KeyboardInterrupt:
    print "Closing binded socket"
    mySocket.close()
