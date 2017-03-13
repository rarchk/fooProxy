import os
import sys
import select
import socket

port = 8000
host = ""

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        "Failed to connect to ", host, port
        sys.exit()
    print 'Connected to remote host. You can start sending messages'

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, _, _ = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from server'
                    sys.exit()
                else:
                    sys.stdout.write(data)
            else:
                msg = sys.stdin.readline()
                if (msg == "quit\n"):
                    sys.stdout.write('Quitting from server\n')
                    sys.stdout.flush()
                    sys.exit()
                s.send(msg)
finally:
    s.close()
    del s
