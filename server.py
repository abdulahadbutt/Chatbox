import socket 
import sys 
import csv

HOST = 'localhost'
PORT = 42069 
CHUNK_SIZE = 1024

def csv_reader(fname):
    usernames = []
    passwords = []
    with open(fname) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            usernames.append(row[0])
            passwords.append(row[1])

    return (usernames, passwords)


usernames, passwords = csv_reader('usernames.csv')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
print('Starting up on {} port {}'.format(HOST, PORT))


# Listening mode
sock.listen()



while True:
    print('Waiting for a connection...')
    conn, addr = sock.accept() 
    data = ''
    try:
        print('Connection from {}'.format(addr))
        conn.sendall(b'Enter username to continue...')

        while True:
            datachunk = conn.recv(CHUNK_SIZE)
            if not datachunk:
                break 
            data += datachunk.decode()
            
        print("username is: {}".format(data))
        if data in usernames:
            conn.sendall(b'Access Granted')
        else:
            conn.sendall(b'Access denied, Username not found')            

    finally:
        conn.close()


