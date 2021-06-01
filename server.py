import socket 
import threading 
from funcs import csv_reader
from constants import *

# * Reading in the usernames and passwords from the local directory
usernames, passwords = csv_reader('usernames.csv')
online_users = []


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


def connect_clients(conn, username):
    # * Showing the active users
    while True:
        # ! STEP 1: SEND USERNAMES TO CLIENT
        print(f'[SENDING USER LIST] Sending usernames to {username}')
        send(conn, str(len(online_users)))
        for users in online_users:
            send(conn, users[0])


        # ! STEP 4: RECEIVING UOI FROM CLIENT
        print(f'[AWAITING USER RESPONSE] awaiting username from {username}')
        user_of_interest = receive(conn)
        # * Disconnecting 
        
        # ! STEP 5: DISCONNECT IF WANTED 
        if user_of_interest == DISCONNECT:
            idx = [i for i, v in enumerate(online_users) if v[0] == username][0]
            del online_users[idx]
            return
        

        # ! STEP 7: IF UOI IS FOUND
        if user_of_interest != NOT_FOUND:
            print(f'[REQUEST] {username} has requested to chat with {user_of_interest}')
            idx = [i for i, v in enumerate(online_users) if v[0] == user_of_interest][0]
            chat(conn, online_users[idx][2])
            return 
            
        # check = [item for item in online_users if user_of_interest in item]
        # print(check)
        # if user_of_interest in online_users:
        #     break 

    # print(user_of_interest)

    # # print([i for i, v in enumerate(online_users) if v[0] == user_of_interest])
    # idx = [i for i, v in enumerate(online_users) if v[0] == user_of_interest][0]
    # print(idx)
    # print("GOT HERE SUCCESSFULLY")
    # print(f'gotta connect {username} with {user_of_interest}')

    # chat(conn, online_users[idx][2])

def chat(c1, c2):
    print(f'[CHAT INITIALIZE] making a chat for {c1} and {c2}')
    ready = receive(c2)
    if ready == OK:
        send(c1, OK)
        send(c2, OK)

    pass

def handle_client(conn, addr):
    # * Successful Connection loop
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        # * Username verification
        user = verify_user_server(conn, addr)
        if not user:
            break
        
        
        # * Connecting different clients
        connect_clients(conn, user)

        
        # while True:
        #     data = receive(conn)
        #     # data = conn.recv(1024)
        #     if data == DISCONNECT:
        #         break 
        #     print(f'[{user}]:{data}')
            
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
            online_users.append((username, addr, conn))
            return username
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
        
            
                            


