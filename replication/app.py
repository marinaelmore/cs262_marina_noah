import argparse
from grpc_chatbot import grpc_server, grpc_client


def initialize_file(filename):
    fp = open(filename)
    fp.close()

# start program when run on command line
if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser()
    # add argument
    parser.add_argument("--mode", help="Client or Server mode",
                        type=str, choices=["client", "backup_server", "primary_server"], required=True)
    parser.add_argument("--host", help="host IP address",
                        type=str, default="0.0.0.0")
    parser.add_argument("--port", help="port to run server on",
                        type=int, default=8000)

    # parse arguments
    args = parser.parse_args()


    if args.mode == "primary_server":
        #Ensure memory file exists
        filename = "grpc_chatbot/datastore/message_store.json"
        initialize_file(filename) 

        # Start primary server
        grpc_server.run_server(primary=True, filename=filename)

    elif args.mode == "backup_server":
        #Ensure memory file exists
        filename = "grpc_chatbot/datastore/message_store.json"
        initialize_file(filename) 

        # Start backup server
        grpc_server.run_server(primary=False, filename=filename)
    
    elif args.mode == "client":
        # Start client
        chatbot_client = grpc_client.ChatbotClient(args.host)
        chatbot_client.run_client()