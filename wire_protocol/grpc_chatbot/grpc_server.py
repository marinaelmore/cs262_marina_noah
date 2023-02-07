import grpc
from concurrent import futures
import chatbot_pb2
import chatbot_pb2_grpc


class User:
    def __init__(self, username):
        self.username = username
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)


class MemoryManager(chatbot_pb2_grpc.MemoryManager):

    def __init__(self):
        self.users ={}

    def SayHello(self, request, context):
        return chatbot_pb2.HelloReply(message='Hello, %s!' % request.name)

    def create_user(self, request, context):
        username = request.username
        if username not in self.users:
            self.users[username] = User(username)
            return chatbot_pb2.ChatbotReply(message='Success! User \"{}\" created.'.format(username)) 
        else:
            return chatbot_pb2.ChatbotReply(message='Error! User \"{}\" already exists.'.format(username)) 

    def send_message(self, request, context):
        return None

    def get_message(self, request, context):
        return None

    def list_users(self, request, context):
        return None

    def delete_user(self, request, context):
        return None

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chatbot_pb2_grpc.add_MemoryManagerServicer_to_server(MemoryManager(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()


