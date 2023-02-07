import grpc
from concurrent import futures
import chatbot_pb2
import chatbot_pb2_grpc



class Greeter(chatbot_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return chatbot_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chatbot_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()


