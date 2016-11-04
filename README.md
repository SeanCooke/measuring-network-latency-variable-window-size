# Measuring Network Latency Variable Window Size

[Read me on GitHub!](https://github.com/SeanCooke/measuring-network-latency-variable-window-size)

## Commands
BUILD COMMAND: `$ make all`

RUN COMMANDS:

TCPServer: `$ ./TCPServer [server_port_number]`

TCPClient: `$ ./TCPClient [server_name] [server_port_number]`

CLEAN COMMAND: `$ make clean`

## Objective
Measuring Network Latency Variable Window Size measures the network latency of sending a 10 MB TCP message between two machines by varying the buffer size of both the sender and receiver.  Results are shown below for both the default buffer size of the send and  receive buffers and 1 MB byte send and receive buffers.

## Results
After running the command `$ ./TCPServer [server_port_number]` on machine SERVER_NAME then running `$ ./TCPClient [server_name] [server_port_number]` on machine CLIENT_NAME we see tables like the one shown below for the appropriate buffer sizes:

    VARYING CLIENT WINDOW SIZE

    Number of Repetitions: 10
    Default Server Window Size: 87380
    Client		Server		Bytes 		Send Window Size   Average Time (sec)
    CLIENT_NAME	SERVER_NAME	10000000 	10000 		       0.509085297585
    CLIENT_NAME	SERVER_NAME	10000000 	1000000 	       0.348921394348
    
    Number of Repetitions: 10
    Largest Server Window Size: 1000000
    Client		Server		Bytes		Send Window Size   Average Time (sec)
    CLIENT_NAME	SERVER_NAME	10000000	10000		       0.508465886116
    CLIENT_NAME	SERVER_NAME	10000000	1000000		       0.364720702171
    
    VARYING SERVER WINDOW SIZE
    
    Number of Repetitions: 10
    Default Client Window Size: 23080
    Client		Server		Bytes		Receive Window Size   Average Time (sec)
    CLIENT_NAME	SERVER_NAME	10000000	87380		          0.35788500309
    CLIENT_NAME	SERVER_NAME	10000000	1000000		          0.371294999123

    Number of Repetitions: 10
    Largest Client Window Size: 1000000
    Client		Server		Bytes		Receive Window Size   Average Time (sec)
    CLIENT_NAME	SERVER_NAME	10000000	87380		          0.367360401154
    CLIENT_NAME	SERVER_NAME	10000000	1000000		          0.337063789368

It is observed that generally increasing the buffer size generally decreases the average round trip time.

These observations were taken on two machines in the same network.

## Method
`TCPClient` starts a clock before sending a message to `TCPServer`.  `TCPClient` then sends 10 MB of data to `TCPServer` 10 times.  `TCPClient` then stops its clock, and divide the clock time by 10 to get the average round trip time for one request.

This process is repeated for varying sending and recieving buffer size via the `socket.setsockopt()` family of function calls.

## References
* Base client/server code modified from chapter 2.7.1 of __Computer Networking: A Top-Down Approach (7th Edition)__ by Kurose and Ross.
* Modified code on multithreading found [here](http://www.tutorialspoint.com/python/python_multithreading.htm).
* Used code on receiving large data objects over TCP found [here](http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data)