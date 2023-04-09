import argparse
from grpc_chatbot import grpc_server, grpc_client
import uuid


# start program when run on command line
if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser()
    # add argument
    parser.add_argument("--mode", help="Client or Server mode",
                        type=str, choices=["client", "backup", "primary"], required=True)
    parser.add_argument("--host", help="host IP address",
                        type=str, default="0.0.0.0")
    parser.add_argument("--port", help="port to run server on",
                        type=int, default=50051)

    parser.add_argument("--file", help="where to persist messages from/to",
                        type=str, default=f"message_store.{uuid.uuid4()}.json")

    # parse arguments
    args = parser.parse_args()
    if args.mode == "client":
        chatbot_client = grpc_client.ChatbotClient(args.host, args.port)
        chatbot_client.run_client()
    else:
        primary = True if args.mode == "primary" else False
        # prepend grpc_chatbot/datastore/ to filename
        print("persiting messages to", args.file)
        filename = f"grpc_chatbot/datastore/{args.file}"
        grpc_server.run_server(
            primary=primary, filename=filename, port=args.port)
