#!/usr/bin/python

#
# Simple HTTP Server Random
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Returns an HTML page with a random link

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
	# Now read until nothing is left
	recv = ""
	recvSocket.settimeout(0.2)
	while True:
		try:
			read = recvSocket.recv(4096)
			print "Read: ", read
			if read:
				recv = recv + read
			else:
				break
		except socket.timeout:
			break
	print recv
	reqList.append((str(datetime.datetime.now()), recv))

	parts = recv.split(None, 2)
	if (len(parts) > 1) and (parts[1] == "/list"):
		htmlBody = "<ul>"
		for entry in reqList:
			htmlBody = htmlBody + "<li><b>" + str(entry[0]) + \
			    "</b><br/>"+ entry[1] + "</li>\n"
		htmlBody = htmlBody + "</ul>"
	else:
		# Resource name for next url
		nextPage = str (random.randint (0,10000))
		nextUrl = "/" + nextPage
		# HTML body of the page to serve
		htmlBody = "<h1>It works!</h1>" + '<p>Next page: <a href="' \
		    + nextUrl + '">' + nextPage + "</a></p>"
	recvSocket.send("HTTP/1.1 200 OK \r\n\r\n" +
			"<html><body>" + htmlBody + "</body></html>" +
			"\r\n")
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
