import socket
import sys


import re

# create regexes for each command in the protocol
create_protocol = re.compile("^CREATE:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
send_protocl = re.compile("^LOGIN:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
list_protocol = re.compile("^LIST:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
send_protocol = re.compile("^SEND:[a-zA-Z0-9]+:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
delete_protocol = re.compile("^DELETE:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
alphanumeric = re.compile("[a-zA-Z0-9]+", re.IGNORECASE)


protocol_list = [create_protocol, send_protocl, list_protocol, send_protocol, delete_protocol]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    host = "0.0.0.0"
    port = int(sys.argv[1])
    client_socket.connect((host, port))

    while True:
        
        command = ""
        
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

            command = "LIST:wildcard:EOM"

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



