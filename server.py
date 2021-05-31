import socket 
from funcs import csv_reader
from constants import *

# * Reading in the usernames and passwords from the local directory
usernames, passwords = csv_reader('usernames.csv')


def verify_user(conn):
    while True:
        datachunk = conn.recv(CHUNK_SIZE)
        print(datachunk)
        if datachunk == EXIT:
            return False 

        username = datachunk.decode()

        if username in usernames:
            conn.send(OK)
            print("username found")
            return 
        else:
            conn.send(NOT_FOUND)
            print("username not found")







# * Creating a socket and binding it
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
print('Starting up on {} port {}'.format(HOST, PORT))


# * Turning on listening mode
sock.listen()


# * The connection loop
while True:
    # * Accepting a new connection
    print('Waiting for a connection...')
    conn, addr = sock.accept() 
    
    # * Successful Connection loop
    print('Connection from {}'.format(addr))
    while True:
        # Username verification
        # conn.sendall(b'Enter username to continue...'

        conn.close()
        # datachunk = conn.recv(CHUNK_SIZE)
        # uname = datachunk.decode()
            
        # # print(uname)
        # if uname not in usernames:
        #     print('Username NOT found')
        #     conn.sendall(NOT_FOUND.encode())

        # else:
        #     print('Username found')
        #     conn.sendall(OK.encode())
        
            
                            

        # finally:
        #     conn.close()


