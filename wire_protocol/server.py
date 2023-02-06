import socket
from server_thread import ServerThread
import sys


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    host = "0.0.0.0"
    port = int(sys.argv[1])
    serversocket.bind((host, port))
    serversocket.listen(5)
    print('Server listening on port', port, '...')
    while True:
        try:
            clientsocket, address = serversocket.accept()
            print(address, "has connected")
            ServerThread(clientsocket)
        # catch all errors
        except KeyboardInterrupt as error:
            break
        except Exception as error:
            print("Server closed unexpectedly: ", error)
            break
