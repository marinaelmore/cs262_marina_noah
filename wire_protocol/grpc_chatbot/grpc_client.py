import grpc
from . import chatbot_pb2
from . import chatbot_pb2_grpc
from . import receiver_thread
import re


# DUP
def get_alphanumeric_input(prompt):
    alphanumeric = re.compile("[a-zA-Z0-9]+")
    while True:
        user_input = input(prompt)
        if re.fullmatch(alphanumeric, user_input):
            return user_input
        else:
            print("Please only use letters and numbers")


def run_client():

    print("Attempting to establish a connection...")

    with grpc.insecure_channel('localhost:50051') as channel:

        chatbot_stub = chatbot_pb2_grpc.ChatBotStub(channel)
        response = None
        receiver_thread.ReceiverThread(chatbot_stub)

        while True:

            command = input(
                "Select a Command \n CREATE, LOGIN, LIST, SEND, DELETE:  ").upper()

            if command == "CREATE":

                input_username = get_alphanumeric_input(
                    "Create a username [a-zA-Z0-9]: ")

                response = chatbot_stub.create_user(
                    chatbot_pb2.UserRequest(username=input_username))

            elif command == "LOGIN":

                username = get_alphanumeric_input(
                    "Login with username [a-zA-Z0-9]: ")

                response = chatbot_stub.login_user(
                    chatbot_pb2.UserRequest(username=username))

            elif command == "LIST":

                wildcard = input(
                    "Enter search prefix (or Enter for all accounts): ")

                response = chatbot_stub.list_users(
                    chatbot_pb2.ListRequest(wildcard=wildcard))

            elif command == "SEND":

                username = get_alphanumeric_input(
                    "Destination username [a-zA-Z0-9]: ")
                message = input("Type message: ")

                # Call server func
                response = chatbot_stub.send_message(
                    chatbot_pb2.MessageRequest(username=username, message=message))

            elif command == "DELETE":

                username = get_alphanumeric_input(
                    "Enter username to delete [a-zA-Z0-9]: ")

                # call server func
                response = chatbot_stub.delete_user(
                    chatbot_pb2.UserRequest(username=username))

            else:
                print("Invalid command, please try again.")

            print("\n---------------------------------------------------------")
            print(response.message)
            print("---------------------------------------------------------\n")
