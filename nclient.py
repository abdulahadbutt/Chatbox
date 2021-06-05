import socket 
from constants import *

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


def verify_user_client(s):
# * Verification on client side
# * returns True if user is logged in, False if otherwise
    while True:
        username = input('Enter your username (Enter -1 to exit): ')
        if username == '-1':
            send(s, EXIT)
            return False 
        password = input('Enter your password: ')
        # print(f'({username}, {password})')
    
        
        send(s, username)
        send(s, password)
        datachunk = receive(s)
        
        # datachunk = s.recv(CHUNK_SIZE)
        if datachunk == OK:
            print('Access granted')
            return True
        else:
            print("Username not found, please re-input")


def close_conn(conn):
    print('Closing....')
    conn.close()


def chat(conn):
# * Currently just sends messages to server where they are printed
    while True:
        msg = input('>> ')
        
        if msg == '-1':
            send(conn, DISCONNECT)
            break 
        
        send(conn, msg)


def get_online_users(conn):
# * Gets all the users that are currently active

    num_online = int(receive(conn))
    print(f'Number of online users: {num_online}')
    
    # * Printing all the online users
    users = []
    for _ in range(num_online):
        user = receive(conn)
        users.append(user)
        
    return users

def menu(conn):
# * Shows the menu of the client side
# * Returns None when you enter -1
# * Prints online users if you enter R using print_online_users
    
    print('Enter R to show the online active users')
    print('Enter !wait to wait to be connected')
    print('Enter -1 to exit')

    choice = input('>>')
    if choice == '-1':
        send(conn, DISCONNECT)
        return

    elif choice == 'R':
        send(conn, SHOW_CLIENTS)
        users = get_online_users(conn)
        print_online_users(users)

    elif choice == '!wait':
        send(conn, WAIT)
        print('Waiting on this side')
        ack = wait_for_confirm(conn)
        if ack == OK:
            print('Can now talk')



def wait_for_confirm(conn):
    msg = receive(conn)
    return msg 


def print_online_users(users: list) -> None:
# * Helper function that prints all the usersnames taken
    for user in users: 
        print(user)

if __name__ == '__main__':
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((HOST, PORT))
        try:
            # * Verify the user
            if not verify_user_client(conn):
                print('Closing....')
                conn.close()

            # * Show the user list
            menu(conn)

            # print('chatting')
            # chat(conn)
            print('Closing...')
            conn.close()
        except KeyboardInterrupt:
            print('\nOkay bye')
            conn.close()
            exit()
