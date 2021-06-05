import socket 
import threading 
from constants import *
import csv

def csv_reader(fname: str) -> tuple:
# * Reads the usernames and passwords in fname
# * Returns a tuple of a list of usernames and passwords
    usernames = []
    passwords = []
    with open(fname) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            usernames.append(row[0])
            passwords.append(row[1])

    return (usernames, passwords)


def send(conn:socket.socket, msg:str) -> None:
# * Sends msg to conn
    message = msg.encode()
    msg_len = len(message)
    send_len = str(msg_len).encode()
    send_len += b' ' * (HEADER - len(send_len))
    conn.send(send_len)
    conn.send(message)


def receive(conn:socket.socket) -> str:
# * Receives msg from conn
    msg_len = conn.recv(HEADER).decode()
    msg_len = int(msg_len)
    msg = conn.recv(msg_len).decode()
    return msg


def verify_user_server(conn:socket.socket, addr:tuple) -> str or False:
# * Verifies if the user is registered
# * Returns the username otherwise returns false
# * Also appends the user and conn in the online_users list
    while True:
        # * receive username
        username = receive(conn)
        
        # * break the connection 
        if username == EXIT:
            return False 

        # * Verification
        password = receive(conn)
        # print(f'username: {username}')
        # print(f'password: {password}')
        
        if username in usernames and passwords[usernames.index(username)] == password:
            send(conn, OK)
            print(f"[VERIFIED] {addr} was verified")
            online_users.append((username, addr, conn))
            return username
        else:
            send(conn, NOT_FOUND)
            print(f"[NOT VERIFIED] {addr} was not verified")


def send_online_users(conn:socket.socket) -> None:
# * Shows the online users to conn
# * Sends the usernames of all active users
    send(conn, str(len(online_users)))
    for users in online_users:
        send(conn, users[0])


def chat(conn):
# * Currently just receives the message and prints it
    while True:
        print('waiting for message')
        msg = receive(conn)
        if msg == DISCONNECT:
            break 
        else:
            print(msg)

def server_menu(conn, username):
# * Mirrors the client menu
# * Receives username of client as well 
    client_ch = receive(conn)
    if client_ch == SHOW_CLIENTS:
        print(f'[SENDING USER LIST] Sending usernames to {username}')
        send_online_users(conn) 


def handle_client(conn:socket.socket, addr:tuple) -> None:
# * Multithreaded function to handle a client connection
    # * Successful Connection loop
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        # * Verify the user
        user = verify_user_server(conn, addr) 
        if not user:
            break
        
        server_menu(conn, user)
        # * Send the online users list to the user
        # show_online_users(conn)
        # chat(conn)
        break 
    
    idx = [i for i, v in enumerate(online_users) if v[0] == user][0]
    del online_users[idx]
    print(f'[DISCONNECTED] {addr} was disconnected')
    conn.close()




if __name__ == "__main__":
    # * Reading in the usernames and passwords
    usernames, passwords = csv_reader('usernames.csv')
    online_users = []
    

    # * Creating a socket and binding it
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    print('[STARTING] Starting up on {} port {}'.format(HOST, PORT))


    # * Turning on listening mode
    sock.listen()
    print(f'[LISTENING] Server is listening on {HOST}')


    # * The connection loop
    try:
        while True:
            # * Accepting a new connection
            conn, addr = sock.accept() 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f'[ACTIVE CONNECTION] {threading.activeCount() - 1}')
    except KeyboardInterrupt:
        print('\n[SHUTTING DOWN] keyboard interrupt detected')
        exit()