import grpc
import chatbot_pb2
import chatbot_pb2_grpc
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


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Attempting to establish a connection...")

    with grpc.insecure_channel('localhost:50051') as channel:

        chatbot_stub = chatbot_pb2_grpc.GreeterStub(channel)

        while True:

            command = input(
                "Select a Command \n CREATE, LOGIN, LIST, SEND, DELETE:  ").upper()

            if command == "CREATE":

                username = get_alphanumeric_input(
                    "Create a username [a-zA-Z0-9]: ")

                # Call server func

            elif command == "LOGIN":

                username = get_alphanumeric_input(
                    "Login with username [a-zA-Z0-9]: ")

                # Call server func

            elif command == "LIST":

                wildcard = input(
                    "Enter search prefix (or Enter for all accounts): ")

                # Call server func

            elif command == "SEND":

                username = get_alphanumeric_input(
                    "Destination username [a-zA-Z0-9]: ")
                message = input("Type message: ")

                # Call server func

            elif command == "DELETE":

                username = get_alphanumeric_input(
                    "Enter username to delete [a-zA-Z0-9]: ")

                #call server func

            else:
                raise ValueError("Invalid command")
  
            response = chatbot_stub.SayHello(chatbot_pb2.HelloRequest(name="marina"))
            print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()