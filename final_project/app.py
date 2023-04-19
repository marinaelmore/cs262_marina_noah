from server import run_server
from client import PongClient
import argparse

def main():
    # add command line arguments --mode server or client
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='server', help='server or client')
    args = parser.parse_args()
    if args.mode == 'server':
        run_server()
    elif args.mode == 'client':
        client = PongClient()
        client.run_client('localhost')


if __name__ == "__main__":
    main()