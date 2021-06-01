import socket 
import threading 
from funcs import csv_reader
from constants import *

# * Reading in the usernames and passwords from the local directory
usernames, passwords = csv_reader('usernames.csv')


def send(conn, msg):
    message = msg.encode()
    msg_len = len(message)
    send_len = str(msg_len).encode()
    send_len += b' ' * (HEADER - len(send_len))
    conn.send(send_len)
    conn.send(message)


def receive(conn):
    msg_len = conn.recv(HEADER).decode()
    msg_len = int(msg_len)
    msg = conn.recv(msg_len).decode()
    return msg


def handle_client(conn, addr):
    # * Successful Connection loop
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        # * Username verification
        if not verify_user_server(conn, addr):
            break
        
        # print('Say something')
        while True:
            data = receive(conn)
            # data = conn.recv(1024)
            if data == DISCONNECT:
                break 
            print(data)
            
        break
        

    print(f'[DISCONNECTED] {addr} was disconnected')
    conn.close()

def verify_user_server(conn, addr):
    while True:
        # * receive username
        username = receive(conn)
        
        # * break the connection 
        if username == EXIT:
            return False 

        # * Verification
        password = receive(conn)
        print(f'username: {username}')
        print(f'password: {password}')
        
        if username in usernames and passwords[usernames.index(username)] == password:
            send(conn, OK)
            print(f"[VERIFIED] {addr} was verified")
            return True
        else:
            send(conn, NOT_FOUND)
            print(f"[NOT VERIFIED] {addr} was not verified")



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
        
            
                            


