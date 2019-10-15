import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
sockets_list = [server_socket]

server_socket.listen()
clients = []

print(f'Listening for connections on {IP}:{PORT}...')

def receive_message(client_socket):
    try:
        message = client_socket.recv(2048).decode('utf-8')
        print("recieving msg: " + message)
        if not len(message):
            return False
        return message
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for soc in read_sockets:
        if soc == server_socket:
            client_socket, client_address = server_socket.accept()
            # accepted socket
            sockets_list.append(client_socket)
            clients.append(client_socket)
            print("New user connected")
        else:
            # receive message
            message = receive_message(soc)
            if message == False:
                print("Closed connection")
                sockets_list.remove(soc)
                clients.remove(soc)
                continue

            # broadcast message
            for client_socket in clients:
                if client_socket != soc:
                    print("sending msg...")
                    client_socket.send(message.encode('utf-8'))
