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

Our chatbot is run via a python app in the parent directory:
``pip install -r requirements.txt``
``app.py --mode {client,server} [--port PORT] [--grpc]``



## To run the Wire Protocol version:

  
1. In a terminal window, start the server. The port is an optional argument - if you do not pass a port, it will default to 8000.
    
    * COMMAND: ``python3 app.y —-mode server [--port 8000]``
    
    * OUTPUT: ``Server listening on port 8000 ...``
   

2. In separate terminal window(s), start the client(s)
    
    *  COMMAND: ``python3 app.y —-mode client [--port 8000]``
    
    *  OUTPUT: `` Select a Command``
     ``CREATE, LOGIN, LIST, SEND, DELETE:``
 

## To run the gRPC version:
  
1. In a terminal window, start the server. The port is an optional argument - if you do not pass a port, it will default to 50051.
    
    * COMMAND: ``python3 app.y —-mode server [--port 50051] --grpc``
    
    * OUTPUT: ``GRPC Server started, listening on 50051``
   

2. In separate terminal window(s), start the client(s). The port is an optional argument - if you do not pass a port, it will default to 50051.
    
    *  COMMAND: ``python3 app.y —-mode client [--port 50051]``
    
    *  OUTPUT: `` Attempting to establish a connection...``
            ``Select a Command``
             ``CREATE, LOGIN, LIST, SEND, DELETE:``
             
             
  
## To interact with the Chatbot:
  
1. The Chatbot has the following capabilities:
    
    * ``CREATE <username>`` : create a user with an alphanumeric username.
    * ``LOGIN <username>`` : login a user by username.
    * ``LIST <wildcard>`` : list users. Search with wildcard or press ``ENTER`` to list all users.
    * ``SEND <to>:<message>``: send a message to another logged in user.
    * ``DELETE <username>``: delete a user by username.



Examples: 
1. Create User - Moah

```
Select a Command
 CREATE, LOGIN, LIST, SEND, DELETE:  create
Create a username [a-zA-Z0-9]: moah

---------------------------------------------------------
CREATE:SUCCESS:EOM
---------------------------------------------------------
```

2. Login User - Moah

```
Select a Command
 CREATE, LOGIN, LIST, SEND, DELETE:  login
Login with username [a-zA-Z0-9]: moah

---------------------------------------------------------
LOGIN:SUCCESS:EOM
---------------------------------------------------------
```

3. List Users

```
Select a Command
 CREATE, LOGIN, LIST, SEND, DELETE:  LIST
Enter search prefix (or Enter for all accounts):

---------------------------------------------------------
LIST:moah:EOM
---------------------------------------------------------
```

5. Send a Message to Another User


  * Client One: Moah (sender)
```
Select a Command
 CREATE, LOGIN, LIST, SEND, DELETE:  send
Destination username [a-zA-Z0-9]: narina
Type message: Hi Narina!

---------------------------------------------------------
SEND:SUCCESS:EOM
---------------------------------------------------------
```
  * Client Two: Narina (reciever)

```Select a Command
 CREATE, LOGIN, LIST, SEND, DELETE:
*** Incoming message from server ***
moah: Hi Narina!
*** Message Received ***
```

6. Delete User - Moah

```
Select a Command
 CREATE, LOGIN, LIST, SEND, DELETE:  delete
Enter username to delete [a-zA-Z0-9]: moah

---------------------------------------------------------
DELETE:SUCCESS:EOM
---------------------------------------------------------
```


## To Test The Chatbot

1. In the terminal, run the unit tests from the home directory:

``pytest -v unit_test.py``

## To Generate Code Coverage Report

1. In the terminal, generate the coverage report:

``coverage run --rcfile=setup.cfg  unit_test.py``

1. Output the coverage report:

``coverage report``

```
Name                          Stmts   Miss  Cover
-------------------------------------------------
chatbot/receiver_thread.py       18      5    72%
chatbot/server_thread.py         72     27    62%
chatbot/wire_protocol.py         37     25    32%
grpc_chatbot/grpc_server.py      59     14    76%
helpers/memory_manager.py        45      5    89%
-------------------------------------------------
TOTAL                           231     76    67%
```


