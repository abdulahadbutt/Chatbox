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


if __name__ == '__main__':
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((HOST, PORT))

        # * Verify the user
        if not verify_user_client(conn):
            print('Closing....')
            conn.close()

        # * Show the user list

        print('chatting')
        chat(conn)
        print('Closing...')
        conn.close()
