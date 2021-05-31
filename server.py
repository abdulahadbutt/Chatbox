import socket 
import threading 
from funcs import csv_reader
from constants import *

# * Reading in the usernames and passwords from the local directory
usernames, passwords = csv_reader('usernames.csv')


def handle_client(conn, addr):
    # * Successful Connection loop
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        # * Username verification
        if not verify_user_server(conn):
            break
        
        
        msg = conn.recv()

    print(f'[DISCONNECTED] {addr} was disconnected')
    conn.close()

def verify_user_server(conn):
    while True:
        # * receive username
        datachunk = conn.recv(CHUNK_SIZE)
        
        # * break the connection 
        if datachunk == EXIT:
            return False 

        # * Username verification
        username = datachunk.decode()
        if username in usernames:
            conn.send(OK)
            print("username found")
            return 
        else:
            conn.send(NOT_FOUND)
            print("username not found")



# * Creating a socket and binding it
# HOST = socket.gethostbyname(socket.gethostname())
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
print('[STARTING] Starting up on {} port {}'.format(HOST, PORT))


# * Turning on listening mode
sock.listen()
print(f'[LISTENING] Server is listening on {HOST}')

# * The connection loop
while True:
    # * Accepting a new connection
    # print('Waiting for a connection...')
    conn, addr = sock.accept() 
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f'[ACTIVE CONNECTION] {threading.activeCount() - 1}')
    
    
    # * Successful Connection loop
    # print('Connection from {}'.format(addr))
    # while True:
        # * Username verification
    #     if not verify_user_server(conn):
    #         break

    # conn.close()
        
            
                            


