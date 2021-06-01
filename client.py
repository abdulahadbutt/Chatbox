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
    while True:
        username = input('Enter your username (Enter -1 to exit): ')
        if username == '-1':
            send(s, EXIT)
            return False 
        password = input('Enter your password: ')
        # print(f'({username}, {password})')
    
        # s.send(username.encode())
        # s.send(password.encode())
        send(s, username)
        send(s, password)
        datachunk = receive(s)
        
        # datachunk = s.recv(CHUNK_SIZE)
        if datachunk == OK:
            print('Access granted')
            return True
        else:
            print("Username not found, please re-input")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Connecting to the server
    s.connect((HOST, PORT))
    
    
    # Username verification
    if not verify_user_client(s):
        print('Closing')
        s.close()
    else:
        print("Say something... (Enter -1 to disconnect)")
        while True:
                msg = input()
                
                if msg == '-1':
                    s.send(DISCONNECT)
                    break 
                
                s.send(msg.encode())
        s.close()
        


    # data = ''
    # while True:
    #     print(datachunk)
    #     if not datachunk:
    #             break 
    #     data += datachunk.decode()
    #     print(data)

