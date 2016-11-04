#!/usr/bin/env python
import sys, threading, struct
from socket import *

# recv_msg recieves a message of a known length over a socket.
# Since send_msg() is called from the client.  The length of the
# message is known
#
# input arguments:
# 1. sock - The socket object you would like to recieve data over
#
# return values:
# 1. recvall(sock, msglen) - The entire message sent over [sock]
def recv_msg(sock):
	# Read message length and unpack it into an integer
	raw_msglen = recvall(sock, 4)
	if not raw_msglen:
		return None
	msglen = struct.unpack('>I', raw_msglen)[0]
	# Read the message data
	return recvall(sock, msglen)

# recvall recieves [n] bytes into [data] over [sock]
# or returns None if EOF is hit
#
# input arguments:
# 1. sock - the socket object [n] bytes are being read over
# 2. n - the number of bytes to read through [sock]
#
# return values:
# data - [n] bytes read over [sock] or None if EOF is hit
def recvall(sock, n):
	data = ''
	while len(data) < n:
		packet = sock.recv(n - len(data))
		if not packet:
			return None
		data += packet
	return data

# requestThread() allows for a concurrent TCP server.
#
# requestThread() is a two tuple composed of a connectionSocket
# and an address.  connectionSocket is a socket object and
# address is a list composed of the hostname and port number
# this request thread listens on.  requestThread() processes
# a TCP request then kills the thread.
class requestThread(threading.Thread):
	def __init__(self, connectionSocket, addr):
		threading.Thread.__init__(self)
		self.connectionSocket = connectionSocket
		self.addr = addr
	def run(self):
		ipAddressPortNumber = self.addr[0]+':'+str(self.addr[1])
		print 'TCP connection opened with: '+ipAddressPortNumber
		message = 'Connection closed by client before response sent.'
		# receiving the entire data message from the client
		message = recv_msg(self.connectionSocket)
		self.connectionSocket.send(message.encode())
		self.connectionSocket.close()
		print 'TCP connection closed with: '+ipAddressPortNumber#+'.  Sent \''+message+'\'.'

# TCPServer() starts a concurrent TCP Server on the machine
# on which the TCPServer executable is run, on the parameter
# [serverPort].
# 
# input arguments:
# 1. serverPort - The integer port number on the machine on which
# the TCPServer executable is run that listens for TCP connections
#
# return values:
# none
def TCPServer(serverPort):
		serverName = gethostname()
		serverPortStr = str(serverPort)
		serverSocket = socket(AF_INET, SOCK_STREAM)
		serverSocket.bind(('',serverPort))
		receiveWindowSize = serverSocket.getsockopt(SOL_SOCKET, SO_RCVBUF)
		serverSocket.setsockopt(SOL_SOCKET, SO_RCVBUF, receiveWindowSize)
		serverSocket.listen(1)
		print serverName+' listening for TCP connections on port '+serverPortStr
		try:
			while True:
				# for each new TCP request, spawn off a new requestThread()
				connectionSocket, addr = serverSocket.accept()
				requestThread(connectionSocket, addr).start()
		except KeyboardInterrupt:
			print '\nTCP Server '+serverName+' listening on port '+serverPortStr+' stopped with a keyboard interrupt.'

# main() starts a concurrent TCP Server on the machine on which
# the TCPServer executable is run, on the port specified
# in the first command line argument.
def main():
	if len(sys.argv) == 2:
		TCPServer(int(sys.argv[1]))
	else:
		print 'ERROR: Invalid number of arguments'

# RUN COMMAND:
# ./TCPServer [serverPort]
main()