import socket
from server_thread import ServerThread


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    host = "0.0.0.0"
    port = 8000
    serversocket.bind((host, port))
    serversocket.listen(5)
    print('server started and listening')
    while True:
        try:
            clientsocket, address = serversocket.accept()
            ServerThread(clientsocket)
        # catch all errors
        except KeyboardInterrupt as error:
            print("Server closed unexpectedly: ", error)
            break
