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
# * Sends msg to conn using HEADER approach
    message = msg.encode()
    msg_len = len(message)
    send_len = str(msg_len).encode()
    send_len += b' ' * (HEADER - len(send_len))
    conn.send(send_len)
    conn.send(message)


def receive(conn:socket.socket) -> str:
# * Receives msg from conn using HEADER approach
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
        
        # * Checking if username matches the password
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


def chat2(c1, c2, u1, u2):
# * Creates a chatroom between two users
# * Returns from this function only when both users have agreed to disconnect

    # * Send the waiting a conn a message that allows it to send messages
    send(c2, OK)

    # * Choosing c1 to speak first 
    send(c1, 'True')
    send(c2, 'False')


    c2_closed, c1_closed = False, False 
    # * Main loop
    while True:
        if not c1_closed:
            s1 = receive(c1)

            # * Subroutine if c1 chooses to disconnect
            if s1 == DISCONNECT:
                c1_closed = True
                print(f'[DIS REQ] {u1} requesting to be disconnected')
                if not c2_closed:
                    send(c2, f'[{u1}] has left the chat')
                send(c1, OK)
            
            # * Subroutine if c1 chooses to send a message
            else:
                if not c2_closed:
                    send(c2, f'[{u1}] {s1}')
        
        
        if not c2_closed:
            s2 = receive(c2)
            # * Subroutine if c1 chooses to disconnect
            if s2 == DISCONNECT:
                print(f'[DIS REQ] {u2} requesting to be disconnected')
                c2_closed = True
                if not c1_closed:
                    send(c1, f'[{u2}] has left the chat')


            # * Subroutine if c2 chooses to send a message 
            else:
                if not c1_closed:
                    send(c1, f'[{u2}] {s2}')


        # * When both closed
        if c1_closed and c2_closed:
            print(f'[CHAT CLOSED] chat between {u1}  and {u2} closed')
            remove_username(u2)
                       
            return 


def remove_username(user):
# * Removes the username from the waiting list
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
            return

        elif client_ch == DISCONNECT:
            return

            
        else:
            uoi = client_ch # * Short for user of interest
            print(f'[REQUEST] {username} has requested to chat with {uoi}')
            
            # * Searching for the user of interest sock
            idx = [i for i, v in enumerate(online_users) if v[0] == uoi][0]
            uoi_sock = online_users[idx][2]

            # * Putting both users in a chatroom
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
            # * if the waiting client has been removed from the list
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
        
        # * Present the servive menu
        server_menu(conn, user)
        break 
    
    # * searching online_users for user
    # * Seeing if {user} is in {online_users}
    idx = [i for i, v in enumerate(online_users) if v[0] == user][0]
    # * Deleting the user from the online_users list
    del online_users[idx]
    print(f'[DISCONNECTED] {addr} was disconnected')
    conn.close()




if __name__ == "__main__":
    # * Reading in the usernames and passwords
    usernames, passwords = csv_reader('usernames.csv')
    online_users = []
    
    # * Initializing a pickle .txt file for waiting subroutine
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
    
    # * Error analysis
    except KeyboardInterrupt:
        print('\n[SHUTTING DOWN] keyboard interrupt detected')
        exit()