import socket 
import threading 
from constants import *
import csv
import pickle
from time import sleep

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

def chat2(c1, c2, u1, u2):

    # * Send the waiting a conn a message that allows it to send messages
    send(c2, OK)

    c2_closed, c1_closed = False, False 
    
    while True:

        s1 = receive(c1)
        if s1 == DISCONNECT:
            c1_closed = True
            print(f'[DIS REQ] {u1} requesting to be disconnected')
        else:
            print(s1)
        
        
        s2 = receive(c2)
        if s2 == DISCONNECT:
            print(f'[DIS REQ] {u1} requesting to be disconnected')
            c2_closed = True
            
        else:
            print(s2)

        if c1_closed and c2_closed:
            print('[CHAT CLOSED] chat between {u1}  and {u2} closed')
            remove_username(u2)
            send(c1, OK)
                       
            return 


def remove_username(user):
    with open('connected_users.txt', 'rb') as f:
        conn_users = pickle.load(f)

    conn_users.remove(user)
    with open('connected_users.txt', 'wb') as f:
        pickle.dump(conn_users, f)
    


def server_menu(conn, username):
# * Mirrors the client menu
# * Receives username of client as well 
# * Returns after a chat closes
    while True:
        client_ch = receive(conn)
        if client_ch == SHOW_CLIENTS:
            print(f'[SENDING USER LIST] Sending usernames to {username}')
            send_online_users(conn) 

        elif client_ch == WAIT:
            print(f'[WAITING] {username} is waiting to be connected to')
            wait_until_over(username)
            # send(conn, OK) 
            return

        else:
            uoi = client_ch
            print(f'[REQUEST] {username} has requested to chat with {uoi}')
            idx = [i for i, v in enumerate(online_users) if v[0] == uoi][0]
            uoi_sock = online_users[idx][2]
            chat2(conn, uoi_sock, u1=username, u2=uoi)
            return 

        



def wait_until_over(user):
# * Keeps the thread in this loop until finished with our chat
    # * Initially adding our user in the list of conn users

    with open('connected_users.txt', 'rb') as f:
        conn_users = pickle.load(f)

    conn_users.append(user)
    with open('connected_users.txt', 'wb') as f:
        pickle.dump(conn_users, f)
        print('[DUMPED]')

    # * Monitoring for change
    while True:
        sleep(WAIT_TIME)
        with open('connected_users.txt', 'rb') as f:
            conn_users = pickle.load(f)
        
        if user not in conn_users:
            # print('[WE ARE OUT]')
            return



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
    
    # ! Adding pickle thingy
    with open('connected_users.txt', 'wb') as f:
        pickle.dump([], f)

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