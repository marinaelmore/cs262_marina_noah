Our chatbot program is a Python application organized into three key directories: (1) chatbot, (2) chatbot with gRPC, and (3) helper functions that are shared across both protocols.

```
.
├── app.py
├── chatbot
│   ├── README.md
│   ├── client.py
│   ├── receiver_thread.py
│   ├── server.py
│   ├── server_thread.py
│   ├── unit_test.py
│   └── wire_protocol.py
├── grpc_chatbot
│   ├── README.md
│   ├── build_protos.sh
│   ├── chatbot.proto
│   ├── chatbot_pb2.py
│   ├── chatbot_pb2_grpc.py
│   ├── grpc_client.py
│   ├── grpc_server.py
│   └── receiver_thread.py
├── helpers
│   └── memory_manager.py
```

Our program is run via passing arguments to the app.py file in the parent directory.

``usage: app.py --mode {client,server} [--port PORT] [--grpc]``

To run the Wire Protocol version:
  
1. In a terminal window, start the server. The port is an optional argument - if you do not pass a port, it will default to 8000.
    
    * COMMAND: ``python3 app.y —-mode server [--port 8000]``
    
    * OUTPUT: ``Server listening on port 8000 ...``
   

2. In separate terminal window(s), start the client(s)
    
    *  COMMAND: ``python3 app.y —-mode client [--port 8000]``
    
    *  OUTPUT: `` Select a Command``
     ``CREATE, LOGIN, LIST, SEND, DELETE:``
 
 To run the gRPC version:
  
1. In a terminal window, start the server. The port is an optional argument - if you do not pass a port, it will default to 50051.
    
    * COMMAND: ``python3 app.y —-mode server [--port 50051] --grpc``
    
    * OUTPUT: ``GRPC Server started, listening on 50051``
   

2. In separate terminal window(s), start the client(s). The port is an optional argument - if you do not pass a port, it will default to 50051.
    
    *  COMMAND: ``python3 app.y —-mode client [--port 50051]``
    
    *  OUTPUT: `` Attempting to establish a connection...``
            ``Select a Command``
             ``CREATE, LOGIN, LIST, SEND, DELETE:``
 
 
