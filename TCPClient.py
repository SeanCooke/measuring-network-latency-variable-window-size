#!/usr/bin/env python
import sys, time, struct
from socket import *

# send_msg allows large messages to be recieved over a TCP socket.
# send_msg attatches the size of the message in bytes to the
# beginning of the message so the server knows the length of the
# message.
#
# input arguments:
# 1. sock - the socket object msg will be sent over
# 2. msg - the message you would like to send over sock
#
# return values:
# none
def send_msg(sock, msg):
	# Prefix each message with a 4-byte length (network byte order)
	msg = struct.pack('>I', len(msg)) + msg
	sock.sendall(msg)

# TCPClient() opens a TCP Connection with a server, sends data
# to that server and receives data from that server.
#
# input arguments:
# 1. serverName - the hostname of the server you wish to
# establish a TCP connection with
# 2. serverPort - the integer port number on [serverName] that
# listens for TCP connections
# 3. sendWindowSize - the integer size of the desired packet
# length to send to the server
# 4. data - the data you would like to send to
# [serverName]:[serverPort]
#
# return values:
# none
def TCPClient(serverName, serverPort, sendWindowSize, data):
	serverName = serverName
	serverPort = serverPort
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	clientSocket.setsockopt(SOL_SOCKET, SO_SNDBUF, sendWindowSize)
	receiveWindowSize = clientSocket.getsockopt(SOL_SOCKET, SO_RCVBUF)
	send_msg(clientSocket, data.encode())
	dataFromServer = ''
	# receive data from [serverName] in [receiveWindowSize] byte chunks
	while True:
		messageFragmentFromServer = clientSocket.recv(receiveWindowSize)
		if not messageFragmentFromServer:
			break
		dataFromServer += messageFragmentFromServer
	# print 'From Server:', dataFromServer.decode()
	clientSocket.close()

# getAverageTCPTimeToSend() establishes a TCP connection with 
# [serverName]:[serverPort].  Sends this server [data] [repetitions]
# times and returns the average number of seconds it takes to send
# [data] one time.
#
# input arguments:
# 1. serverName - the hostname of the server you wish to
# establish a TCP connection with
# 2. serverPort - the integer port number on [serverName] that
# listens for TCP connections
# 3. sendWindowSize - the integer size of the send buffer in bytes
# 4. data - the data you would like to send to
# [serverName]:[serverPort]
# 5. repetitions - The number of times you would like to send
# [serverName] [data].  The higher this number, the more accurate
# [avgTime] will be
#
# return values:
# avgTime - The average time, in seconds, it takes to send
# [data] to [serverName]:[serverPort] [repetitions] times
def getAverageTCPTimeToSend(serverName, serverPort, sendWindowSize, data, repetitions):
	timeStart = time.time()
	for iteration in range(0, repetitions):
		TCPClient(serverName, serverPort, sendWindowSize, data)
	deltaTime = time.time() - timeStart
	avgTime = deltaTime/repetitions
	return avgTime

# main() will send 10 MB to the host specified in the first
# command line argument on the port specified in the second
# command line argument 20 times.  The first 10 times 10 MB
# are sent, the buffer size of the sender will be 10 kB.
# The second 10 times 10 MB are sent, the buffer size of the sender
# will be 1 MB.
#
# main() will then print out the average round trip time for these
# data streams in a table as well as the number of repetitions and
# buffer size.
def main():
	if len(sys.argv) == 3:
		clientName = gethostname()
		serverName = sys.argv[1]
		serverPort = int(sys.argv[2])
		data = 'a' * 9999963
		dataSize = str(sys.getsizeof(data))
		sendWindowSizeList = [10000, 1000000]
		repetitions = 10
		
		print 'Number of Repetitions: '+str(repetitions)
		print 'Client\t\t\t\t\tServer\t\t\t\t\tBytes\t\tSend Window Size\tAverage Time (sec)'
		for sendWindowSize in sendWindowSizeList:
			avgTCPTimeCurrentWindowSize = str(getAverageTCPTimeToSend(serverName, serverPort, sendWindowSize, data, repetitions))
			print clientName+'\t'+serverName+'\t'+dataSize+'\t'+str(sendWindowSize)+'\t\t\t'+avgTCPTimeCurrentWindowSize
	else:
		print 'ERROR: Invalid number of arguments'

# RUN COMMAND:
# ./TCPClient [serverName] [serverPort]
main()