import socket
import sys
import re
from receiver_thread import ReceiverThread
from time import sleep
from wire_protocol import WireProtocol


def get_alphanumeric_input(prompt):
    alphanumeric = re.compile("[a-zA-Z0-9]+")
    while True:
        user_input = input(prompt)
        if re.fullmatch(alphanumeric, user_input):
            return user_input
        else:
            print("Please only use letters and numbers")


alphanumeric = re.compile("[a-zA-Z0-9]+")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    host = "0.0.0.0"
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    client_socket.connect((host, port))

    # start listening for incoming messages on a seperate non-blocking thread
    ReceiverThread(client_socket)

    # collect input
    while True:

        command = ""

        while command not in ["CREATE", "LOGIN", "LIST", "SEND", "DELETE"]:

            command = input(
                "Select a Command \n CREATE, LOGIN, LIST, SEND, DELETE:  ").upper()

        if command == "CREATE":

            username = get_alphanumeric_input(
                "Create a username [a-zA-Z0-9]: ")
            command = WireProtocol.serialize_request(command, username)

        elif command == "LOGIN":

            username = get_alphanumeric_input(
                "Login with username [a-zA-Z0-9]: ")
            command = WireProtocol.serialize_request(command, username)

        elif command == "LIST":

            wildcard = input(
                "Enter search prefix (or Enter for all accounts): ")
            command = WireProtocol.serialize_request(command, wildcard)

        elif command == "SEND":

            username = get_alphanumeric_input(
                "Destination username [a-zA-Z0-9]: ")
            message = input("Type message: ")

            command = WireProtocol.serialize_request(
                command, username, message)

        elif command == "DELETE":

            username = get_alphanumeric_input(
                "Enter username to delete [a-zA-Z0-9]: ")
            command = WireProtocol.serialize_request(command, username)

        else:
            raise ValueError("Invalid command")
        
        client_socket.send(command)
        sleep(1)
