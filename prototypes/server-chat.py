import socket, select

PORT = 42069
socket_list = []
users = {}

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.bind(('', PORT))
server_sock.listen()
socket_list.append(server_sock)
while True:
    rtr, rtw, ie = select.select(socket_list, [], [], 0)
    for sock in rtr:
        if sock == server_sock:
            connect, addr = server_sock.accept()
            socket_list.append(connect)
            connect.send(("You are connected from:" + str(addr)).encode())
        else:
            try:
                data = sock.recv(2048)
                if data.startswith("#"):
                    users[data[1:].lower()]=connect 
                    print("User" + data[1:] + "added")
                    connect.send("Your user detail saved as: " + str(data[1:]))
                elif data.startswith("@"):
                    users[data[1:data.index(':')].lower()].send(data[data.index(':')+1:])
            except:
                continue

server_sock.close()