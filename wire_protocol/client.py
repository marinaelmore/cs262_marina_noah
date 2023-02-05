import socket
import sys


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    host = "0.0.0.0"
    port = int(sys.argv[1])
    client_socket.connect((host, port))

    while True:
        r = input('Waiting for input: ')
        client_socket.send(r.encode())
        data = client_socket.recv(1024).decode()
        print(data)



