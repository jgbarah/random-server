#!/usr/bin/python

#
# Simple HTTP Server Random Logger
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# 2009 - 2015
#
# Returns an HTML page with a random link, and performs some other
#  few tricks

import socket
import random
import sys
import os
import datetime
import email.Utils

def parse (request):
    """Parse request, get relevant data.

    Currently just returns the resource name.

    """

    components = request.split(' ',2)
    method = components[0]
    resource = components[1]
    return (method, resource)

# Default headers for responses
default_headers = {
    "Server": "Random/1.0a",
    }


def og_data (resource):
    """Returns HTML with headers with Open Graph data.
    """

    template = """<meta property="og:title" content="Random Canary {resource}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="http://canary.libresoft.es/{resource}" />
<meta property="og:description" content="Random canaries all over the place: Now featuring {resource}." />
<meta property="og:site_name" content="Random Canaries" />
"""
    html = template.format (resource = resource[1:])
    return html

def twitter_card (resource):
    """Returns HTML with headers for a twitter card.
    """

    template = """<meta name="twitter:card" content="summary" />
<meta name="twitter:site" content="@jgbarah" />
<meta name="twitter:title" content="Random Canaries" />
<meta name="twitter:description" content="Random canaries all over the place: Now featuring {resource}." />
"""
    html = template.format (resource = resource[1:])
    return html

def process (method, resource):
    """Process request.

    Returns HTTP response, ready to send to requester.
    """

    headers = default_headers
    headers["Date"] = email.Utils.formatdate(usegmt = True)
    if method not in ("GET", "HEAD"):
        httpCode = "405 Method Not Allowed"
        body = None
    elif resource in ["/favicon.ico", "/sitemap.xml"]:
        httpCode = "404 Not Found"
        body = None
    elif resource == "/robots.txt":
        httpCode = "200 OK"
        body = "User-agent: *\nAllow: /\n"
        headers["Content-Type"] = "text/plain;charset=ascii"
    else:
        # Resource name for next url
        nextPage = str (random.randint (0,100000))
        nextUrl = "/" + nextPage
        # HTML body of the page to serve
        body = "<!DOCTYPE html><html lang='en'><head>" \
            + "<meta charset='utf-8'/>" \
            + twitter_card(nextPage) \
            + og_data(nextPage) \
            + "<title>Random Canaries</title>" \
            + "</head>" \
            + "<body><h1>Random canaries all over the place</h1>" \
            + "<p>Now featuring: <a href='" \
            + nextUrl + "'>" + nextPage + "</a></p></body></html>"
        httpCode = "200 OK"
        headers["Content-Language"] = "en"
        headers["Content-Type"] = "text/html;charset=utf-8"
        headers["Last-Modified"] = headers["Date"]
    if body:
        headers["Content-Length"] = str(len(body))
    else:
        headers["Content-Length"] = "0"
    httpHeaders = ""
    for header, value in headers.items():
        httpHeaders = httpHeaders + header + ": " + value + "\r\n"
    httpResponse = "HTTP/1.1 " + httpCode + "\r\n" \
        + httpHeaders + "\r\n" 
    if body and (method != "HEAD"):
        httpResponse =  httpResponse + body
    #print httpResponse
    return httpResponse

# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

myPort = 80

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
        request = recvSocket.recv(4096)
        print 'HTTP request received:',
        print datetime.datetime.now().isoformat(),
        print address
        print
        print request

        try:
            (method, resource) = parse (request)
        except:
            # In some cases, a malformed request can come. Abort.
            resource = None
            print "*** Malformed request?"
        if resource:
            response = process(method, resource)
            #print httpResponse
            recvSocket.send(response)
        recvSocket.close()

except KeyboardInterrupt:
    print "Closing bound socket"
    mySocket.close()
