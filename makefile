all:
	cp TCPClient.py TCPClient
	cp TCPServer.py TCPServer
	chmod +x TCPClient
	chmod +x TCPServer

clean:
	rm -rf TCPClient
	rm -rf TCPServer
