import socket 

HOST = '127.0.0.1'
PORT = 42069
CHUNK_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.sendall(b'Hello world!')
    data = s.recv(1024)
    print(data)
    
    
    username = input()
    s.sendall(username.encode())
    data = ''
    while True:
        datachunk = s.recv(CHUNK_SIZE)
        if not datachunk:
                break 
        data += datachunk.decode()
        print(data)

