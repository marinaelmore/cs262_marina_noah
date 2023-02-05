import socket
import sys
import re

alphanumeric = re.compile("[a-zA-Z0-9]+")

alphanumeric = re.compile("[a-zA-Z0-9]+")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    host = "0.0.0.0"
    port = int(sys.argv[1])
    client_socket.connect((host, port))

    while True:
        
        command = ""
        
        # TODO how not to block here if someone is waiting in the command area
        while command not in ["CREATE", "LOGIN", "LIST", "SEND", "DELETE"]:
            
            command = input("Select a Command \n CREATE, LOGIN, LIST, SEND, DELETE:  ")
        

        if command == "CREATE":
            
            username = input("Create a username [a-zA-Z0-9]: ")

            while not re.fullmatch(alphanumeric, username):
                print("Please only use letters or numbers")
                username = input("Create a username: ")

            command = "CREATE:{}:EOM".format(username)

        elif command == "LOGIN":

            username = input("Enter your username: ")

            command = "LOGIN:{}:EOM".format(username)

        elif command == "LIST":

            wildcard = input("Enter search wildcard: ")

            command = "LIST:{}:EOM".format(wildcard)

        elif command == "SEND":

            # Add to queue

            msg = input("Enter your message [a-zA-Z0-9]: ")

            while not re.fullmatch(alphanumeric, username):
                
                print("Please only use letters or numbers in your message")
                
                msg = input("Enter your message: ")

            command = "CREATE:{}:EOM".format(msg)
        
        elif command == "DELETE":
            
            username = input("Enter username to delete: ")

            while not re.fullmatch(alphanumeric, username):
                print("Please only use letters or numbers")
                username = input("Enter username to delete: ")

            command = "DELETE:{}:EOM".format(username)

        else:
            print("Not a valid command")

        
        print(command)
        client_socket.send(command.encode())
        data = client_socket.recv(1024).decode()
        print(data)



