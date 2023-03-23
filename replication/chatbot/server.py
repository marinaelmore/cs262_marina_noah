import socket
from .server_thread import ServerThread


# function to run server and accept socket connections
def run_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        host = "0.0.0.0"
        serversocket.bind((host, port))
        serversocket.listen(5)
        print('Server listening on port', port, '...')
        while True:
            try:
                clientsocket, address = serversocket.accept()
                print(address, "has connected")
                # when we accept a connection, we create a new thread to handle it
                # so multiple connections can be managed independently
                ServerThread(clientsocket)
            # catch all errors
            except KeyboardInterrupt as error:
                break
            except Exception as error:
                print("Server closed unexpectedly: ", error)
                break
