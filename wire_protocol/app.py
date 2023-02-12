import argparse
from chatbot import server, client
from grpc_chatbot import grpc_server, grpc_client
# if name is main
if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser()
    # add argument
    parser.add_argument("--mode", help="Client or Server mode",
                        type=str, choices=["client", "server"], required=True)
    parser.add_argument("--port", help="port to run server on",
                        type=int, default=8000)
    parser.add_argument("--grpc", help="run grpc server",
                        action="store_true")
    # parse arguments
    args = parser.parse_args()
    # if grpc
    if args.grpc:
        if args.mode == "server":
            grpc_server.run_server()
        elif args.mode == "client":
            grpc_client.run_client()
    else:
        if args.mode == "server":
            server.run_server(args.port)
        elif args.mode == "client":
            client.run_client(args.port)
