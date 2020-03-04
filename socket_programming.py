import sys
from socket import *

# main func
def main():
    # designate port #
    port_number = 4242
    # create a TCP server socket, or, as per python docs, INET socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    # prepare a server socket, SO_REUSEADDR flag tells the kernel to reuse loc
    # al socket in TIME_WAIT state, without waiting for its natural timeout
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # bind the socket to address. the socket mus
    # t not be previously bound to any address
    server_socket.bind(('', port_number))
    # enable a server to accept co
    # nnections. backlog is 1, whi
    # ch specifies the number of u
    # naccepted connections that t
    # he system will allow before
    # refusing new connection
    server_socket.listen(1)
    print('Server listening on port ', port_number)

    while True:
        # establish the connection
        print('server established.')
        # accept a connection. socket must be bound
        # to an address and listening for connections 
        (conn, addr) = server_socket.accept()

        try:
            # receive a message request
            msg = conn.recv(1024)
            # extract path of requested object from the message
            print(msg, '::', msg.split()[0], ':', msg.split()[1])
            # path is the secon
            # d arg of the HTTP 
            # header, in as [1]
            fn = msg.split()[1]
            print(fn, '||', fn[1:])
            # the extended path of 
            # the HTTP request inc
            # ludes character '\', 
            # so we must read path
            # from the second char
            fp = open(fn[1:])
            # store the content of
            # requested file in te
            # mporary buffer
            out_buffer = fp.read()

            # send a single HTTP header line into socket
            conn.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            # send the content of the requested 
            # file to the client 
            for i in range(0, len(out_buffer)):
                conn.send(out_buffer[i].encode())

            conn.send("\r\n".encode())

            # close clie
            # nt connect
            # ion socket
            conn.close()
            # close fp
            fp.close()
            
        except IOError:
            # if trying to get a file th
            # at is not present at the s
            # server, send a 404 msg
            print("404, Page Not Found")
            conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            # close clie
            # nt socket.
            conn.close()
            # close fp
            fp.close()

        server_socket.close()
        sys.exit()

# our program entry point
if __name__ == "__main__":
    main()

