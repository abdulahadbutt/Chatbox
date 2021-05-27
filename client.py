import socket 

HOST = '127.0.0.1'
PORT = 42069
CHUNK_SIZE = 1024
NOT_FOUND = '404'
OK = '200'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Connecting to the server
    s.connect((HOST, PORT))
    
    while True:
        # Username verification
        # data = s.recv(1024)
        # print(data.decode())
        
        username = input('Enter your username (Enter -1 to exit):')
        if username == '-1':
            break 
        s.sendall(username.encode())
        
        
        datachunk = s.recv(CHUNK_SIZE)
        if datachunk.decode == OK:
            print('Access granted')
        


    # data = ''
    # while True:
    #     print(datachunk)
    #     if not datachunk:
    #             break 
    #     data += datachunk.decode()
    #     print(data)

