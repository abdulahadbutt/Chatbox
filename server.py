import socket


HOST = '127.0.0.1'
PORT = 42069
# Creating a TCP/IP Socket
'''
    AF_NET is the internet address family for IPV4
    SOCK_STREAM is the socket type for TCP
'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind socket to a network interface and port number 
    s.bind((HOST, PORT))

    # Put the socket into listening mode 
    s.listen()
    print('Socket is listening')

    c, addr = s.accept()
    with c:
        print("Connected by", addr)
        while True:
            data = c.recv(1024)
            if not data:
                break 
            c.sendall(data)


