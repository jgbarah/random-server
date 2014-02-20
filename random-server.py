#!/usr/bin/python

# Copyright (C) 2013 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

#
# Simple HTTP Server Random
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI, SAT, SARO subjects (Universidad Rey Juan Carlos)
# February 2014
#
# Returns an HTML page with a random link, and provides some logging
#

import os
import socket
import random
import datetime

reqList = []

# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

# myPort = 1234
myHost = socket.gethostname()
myPort = int (os.environ["PORT"])
print myHost, myPort
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind((myHost, myPort))

# Queue a maximum of 10 TCP connection requests

mySocket.listen(5)

# Initialize random number generator (not exactly needed, since the
# import of the module already is supposed to do that). No argument
# means time is used as seed (or OS supplied random seed).
random.seed()

def attendReq (recvSocket):
	print 'HTTP request received:'
	recv = ""
	# Now read until nothing is left, or 0.2 sec. passed
	# I should read until the number of bytes specified by
	# length header, but this works most of the time, and
	# avoids a simple DoS by not seding the promised length
	recvSocket.settimeout(0.2)
	while True:
		try:
			read = recvSocket.recv(4096)
			if read:
				recv = recv + read
			else:
				break
		except socket.timeout:
			break
	# Append the received request with logging purposes
	reqList.append((str(datetime.datetime.now()), recv))

	parts = recv.split(None, 2)
	htmlList = ""
	if (len(parts) > 1) and (parts[1] == "/log"):
		# /log received, prepare logs
		htmlList = "<p>Number of requests: " + \
		    str(len(reqList)) + "</p>\n"
		htmlList = htmlList + "<ol>"
		for entry in reqList:
			htmlList = htmlList + "<li><b>" + str(entry[0]) + \
			    "</b><br/><pre>"+ entry[1] + "</pre></li>\n"
		htmlList = htmlList + "</ol>"
	# Any resource: new random link
	nextPage = str (random.randint (0,10000))
	nextUrl = "/" + nextPage
	# HTML body of the page to serve
	htmlBody = "<h1>The most amusing web site in the galaxy</h1>" + \
	    "<p>Next page: <a href='" \
	    + nextUrl + "'>" + nextPage + "</a></p>\n"
	htmlBody = htmlBody + "<div style='text-align:right'>" + \
	    "<a href='https://github.com/jgbarah/random-server'>" + \
	    "Source code</a></div>\n"
	if htmlList:
		htmlBody = htmlBody + "<h1>Log</h1>\n" + htmlList
	else:
		htmlBody = htmlBody + "<div style='text-align:right'>" + \
		    "<a href='/log'>Log</a></div>\n"
	httpResp = "HTTP/1.1 200 OK \r\n\r\n" + \
	    "<!DOCTYPE HTML><html><body>" + htmlBody + \
	    "</body></html>" + \
	    "\r\n"
	totalSent = 0
	while totalSent < len(httpResp):
		sent = recvSocket.send(httpResp[totalSent:])
		if sent == 0:
			# Connection broken, don't try to send more data
			break
		totalSent = totalSent + sent
	recvSocket.close()

# Accept connections, read incoming data, and answer back an HTLM page
#  (in a loop)
try:
	while True:
		print 'Waiting for connections'
		(recvSocket, address) = mySocket.accept()
		attendReq (recvSocket)
finally:
	mySocket.close()
