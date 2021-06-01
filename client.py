from os import wait
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


def chat(conn):
    print("Please wait to be connected...")
    send(conn, OK)
    go_ahead = receive(conn)
    if go_ahead == OK:
        print('You can now send messages to that guy')
        while True:
            msg = input('>> ')
            send(conn, msg)
            # if user_of_interest in users:
            #     send(s, user_of_interest)
            #     break 
            # else:
            #     print("Incorrect user, enter again")
            #     for user in users:
            #         print(user)

def connect_to_user(conn):
    while True:
        # * Receiving the number of online users
        # ! STEP 2: RECEIVING USERNAMES FROM SERVER
        num_online = int(receive(conn))
        print(f'Number of online users: {num_online}')
        
        # * Printing all the online users
        users = []
        for _ in range(num_online):
            user = receive(conn)
            users.append(user)
            print(user)
        
        
        print("\nEnter the user name you want to communicate with")
        print("Enter -1 to exit and R to reload active users")
        user_of_interest = input(">> ")
        # ! STEP 3: SENDING UOI TO SERVER

        # ! STEP 6: DISCONNECTING IF WANTED
        if user_of_interest == '-1':
            send(conn, DISCONNECT)
            return  
        


        # * If user is found
        # ! STEP 3 CONTINUED
        elif user_of_interest in users:
            send(conn, user_of_interest)
            chat(conn)
            

        else:
            send(conn, NOT_FOUND)
            print('User was not found, please enter again...')


        # while True:
        #     print("Here")
        #     user_of_interest = input('>> ')
        #     if user_of_interest in users:
        #         send(s, user_of_interest)
        #         break 
        #     else:
        #         print("Incorrect user, enter again")
        #         for user in users:
        #             print(user)

def verify_user_client(s):
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



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Connecting to the server
    s.connect((HOST, PORT))
    
    
    # Username verification
    if not verify_user_client(s):
        print('Closing...')
        s.close()
    

    connect_to_user(s)
    s.close()

    # print("Say something... (Enter -1 to disconnect)")
    
    
    # print(receive(s))
    
        
    # while True:
    #         msg = input('>> ')
            
    #         if msg == '-1':
    #             send(s, DISCONNECT)
    #             break 
            
    #         send(s, msg)
    # s.close()
        


    # data = ''
    # while True:
    #     print(datachunk)
    #     if not datachunk:
    #             break 
    #     data += datachunk.decode()
    #     print(data)

