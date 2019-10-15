import socket
import select
import errno
import threading

IP = input("IP address: ")
PORT = 1234
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))


while True:
    # If message is not empty - send it
    message = input("Me >")
    if len(message):
        client_socket.send(message.encode('utf-8'))
    try:
        message = client_socket.recv(2048).decode('utf-8')
        if not len(message):
            print('Connection closed')
            sys.exit()
        else:
            print(f'someone > {message}')

    except IOError as e:
        continue

