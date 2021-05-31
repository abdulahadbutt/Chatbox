import socket 
from constants import *

def verify_user_client(s):
    while True:
            username = input('Enter your username (Enter -1 to exit):')
            if username == '-1':
                s.send(EXIT)
            else:
                s.sendall(username.encode())
                
                
                datachunk = s.recv(CHUNK_SIZE)
                if datachunk == OK:
                    print('Access granted')
                    return  
                else:
                    print("Username not found, please re-input")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Connecting to the server
    s.connect((HOST, PORT))
    
    while True:
        # Username verification
        # data = s.recv(1024)
        # print(data.decode())
        verify_user_client(s)
        print("I'm in B/")


        s.close()
        


    # data = ''
    # while True:
    #     print(datachunk)
    #     if not datachunk:
    #             break 
    #     data += datachunk.decode()
    #     print(data)

