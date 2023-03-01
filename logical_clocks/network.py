import socket
from virtual_machine import VirtualMachine
import select
import sys

ports = 8000, 8080, 8081
socket_list = []
host = '0.0.0.0'
buf_size = 1024
num_connections = 3


try:
    for port in ports:
        network_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        network_socket.bind((host, port))
        network_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
        network_socket.listen(num_connections)
        socket_list.append(network_socket)
except Exception as e:
    for socket in socket_list:
        socket.close()
    print('Could not open sockets')
    sys.exit(1)

while True:
    print("connecting....")
    read, write, error = select.select(socket_list,[],[])

    for r in read:
        if r in socket_list:
            accepted_socket, address = r.accept()

            print('We have a connection with {}'.format(address))
            
            data = accepted_socket.recv(buf_size)
            
            if data:
                print(data)
                accepted_socket.send(b'Hello, and goodbye.')
                accepted_socket.close()