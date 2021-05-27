import socket 
import sys 
import csv

HOST = 'localhost'
PORT = 42069 
CHUNK_SIZE = 1024
NOT_FOUND = '404'
OK = '200'

def csv_reader(fname):
    usernames = []
    passwords = []
    with open(fname) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            usernames.append(row[0])
            passwords.append(row[1])

    return (usernames, passwords)

# def verify_user(conn):

usernames, passwords = csv_reader('usernames.csv')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
print('Starting up on {} port {}'.format(HOST, PORT))


# Listening mode
sock.listen()


# The connection loop
while True:
    print('Waiting for a connection...')
    conn, addr = sock.accept() 
    
    # Successful Connection loop
    print('Connection from {}'.format(addr))
    while True:
        # Username verification
        # conn.sendall(b'Enter username to continue...')
        datachunk = conn.recv(CHUNK_SIZE)
        uname = datachunk.decode()
            
        # print(uname)
        if uname not in usernames:
            print('Username NOT found')
            conn.sendall(NOT_FOUND.encode())

        else:
            print('Username found')
            conn.sendall(OK.encode())
        
            
                            

        # finally:
        #     conn.close()


