Foo Proxy Protocol  
=== 

## Description

Foo is a simple, powerful, extensible, cloud-native request/response protocol.
Foo protocol messages are UTF-8 encoded strings with the following BNF-ish definition:

```tla++
Msg  := Type <whitespace> Seq [<whitespace> Data] '\n'
Type := "REQ" | "ACK" | "NAK"
Seq  := <integer>
Data := <string without newline>
```

A Msg is composed of
 a Type string, either "REQ", "ACK", or "NAK";
 a Seq integer, starting with 1;
 an optional Data string;
 and a terminating newline character '\n', 0x0A.
A Foo client initiates a TCP connection to a Foo server,
 sends messages and receives replies in the request/response pattern,
 and eventually terminates the connection.
Clients produce REQ messages, and servers respond with ACK or NAK messages.
Only clients may terminate the connection.

Here is a valid example exchange of messages:

```
A->B: <connect>
A<-B: REQ 1 Hey\n
A<-B: ACK 1 Hello\n
A->B: REQ 2 Hey there\n
A<-B: ACK 2\n
A->B: REQ 3 Hey\n
A->B: REQ 4 Hey\n
A->B: REQ 5 Hey\n
A<-B: ACK 3 What\n
A<-B: ACK 4 What do you want\n
A->B: REQ 6 Hey\n
A<-B: NAK 5 Stop it\n
A<-B: NAK 6 Stop doing that\n
A->B: <disconnect>
```

## Task

Your task is to write a Foo protocol proxy server, which sits "in front" of an existing Foo server.
It should accept connections from arbitrary clients, and proxy them to the server.
In addition, it should collect statistics for the traffic that it proxies.
When your proxy receives SIGUSR1, it should report the current statistics to stdout as a JSON object.
Your object may include as many statistics as you like, but we will check for the following fields, named exactly as shown.

- `msg_total` — total number of messages (integer)
- `msg_req` — total number of REQ messages (integer)
- `msg_ack` — total number of ACK messages (integer)
- `msg_nak` — total number of NAK messages (integer)
- `request_rate_1s` — average REQ messages/sec, in a 1s moving window (floating point)
- `request_rate_10s` — average REQ messages/sec, in a 10s moving window (floating point)
- `response_rate_1s` — average ACK+NAK messages per second, in a 1s moving window (floating point)
- `response_rate_10s` — average ACK+NAK messages per second, in a 10s moving window (floating point)

## Test driver

In addition to this document, you should have received **server** and **client** binaries.
You may use these to confirm your proxy is behaving correctly.
The client will connect to the server, send a specific number of requests, and report results.

```
$ ./server
$ ./client
..........OK!
```

The client should work identically if you put your proxy in the middle.

```
$ ./server -listen=:8001
$ ./proxy -listen=:8002 -forward=localhost:8001
$ ./client -connect=localhost:8002
..........OK!
```

## Submission requirements

Language choice is entirely up to you.

Please submit the complete source code to your proxy (not the binaries).
Be sure to include a README or equivalent, with build and usage instructions.
Your submission should have as few third-party dependencies as possible,
 ideally none beyond your language's standard library.

Your submission should be what you consider _production quality_.
Treat your reviewers as you would treat your colleagues.
But, please don't spend more than 4 hours on this task.
If you need to leave some things out due to time constraints, no problem: just make a note in the code or README.

# Design Concepts 
- edge triggered polling vs level triggered polling 
- select vs polling vs epolling 
- Nagle Theorem (reducing small number of packets by waiting for previous ack) vs Dealyed_ACK policy on reciever(caused deadlock with reciever) 
- TCP_NODELAY(disables Nagle theorem) and TCP_CORK(aggressively accumulates data till a size)
	- both flags can exist together, but if yes then TCP_CORK will be given preference 
-  

# Patterns 
- 1 epoll for connecting, and multille epoll workers to process requests.
- Socket accpet preforking (multiple process to listen on the same port, and handeling client connections indpendently )
- A possible solution are worker processes that duplicate the client’s socket, a technique that allows the workers to processes requests and send responses directly to the client socket. This approach is particularly useful for long lasting connections with more than one request per session.
- multiprocessing and pickling of methods 

# EPOLL FLAGS 
EPOLLIN 		Available for read
EPOLLOUT 		Available for write
EPOLLPRI 		Urgent data for read
EPOLLERR 		Error condition happened on the assoc. fd
EPOLLHUP 		Hang up happened on the assoc. fd
EPOLLET 		Set Edge Trigger behavior, the default is Level Trigger behavior
EPOLLONESHOT 	Set one-shot behavior. After one event is pulled out, the fd is internally disabled
EPOLLRDNORM 	Equivalent to EPOLLIN
EPOLLRDBAND 	Priority data band can be read.
EPOLLWRNORM 	Equivalent to EPOLLOUT
EPOLLWRBAND 	Priority data may be written.
EPOLLMSG 		Ignored.	

# Assumptions or Declarations about code 
- Server always assumes that it will get a foo compliant client 
- Proxy server has to check whether client is
	- arbitrary client  
	- foo compliant client
- A client can send one or many requests without waitng for acknowledgement. Server accepts messages with **"\n"** as delimiter. For our foo protocol, I do not handle multiple requests without waiting for acknowledgement.    
- Clients can disconnect, and foo has to relay this info to server, and same behaviour from server too. 
- Sequence numbers are relative to connection, so multiple connection will have their own namespace of sequence numbers.
- NAK requests may come or may not. I do not understand in what conditions they may arise. 


# Implementation 
- FooProxyServer is a single threaded epoll edge-triggered server implemented in python. I chose this implementation because 
	- it best utilizes single core. 
	- Threading is not a good option in python because of GIL(Global Interpreter Lock)
	- Process can parallelize with epoll will be most efficient solution. But I did not do it. 

- Logging is used to take a log of all requests processed by proxy server. I chose to do it so, because all metrics are function of a good log. 
- Implementation took me one day, as using edge-triggered based code is difficult to program, and it was my first time.
- Signal handelling is done.
