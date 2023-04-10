import argparse
from grpc_chatbot import grpc_server, grpc_client
import uuid


# start program when run on command line
if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser()
    # add argument
    parser.add_argument("--mode", help="Client or Server mode",
                        type=str, choices=["client", "server"], required=True)
    
    #only require --server_id argument if mode == "server'"
    parser.add_argument("--server_id", help="Server ID",
                        type=int, required=False, )
    
    # parse arguments
    args = parser.parse_args()
    if args.mode == "client":
        chatbot_client = grpc_client.ChatbotClient()
        chatbot_client.run_client()
    elif args.mode == "server":
        # if no server_id is provided,raise an error
        if args.server_id is None:
            raise ValueError("server_id is required when mode is server")
        # prepend grpc_chatbot/datastore/ to filename
        filename = f"grpc_chatbot/datastore/message_store.{args.server_id}.json"
        print("persiting messages to", filename)
        grpc_server.run_server(filename=filename, server_id=args.server_id)
