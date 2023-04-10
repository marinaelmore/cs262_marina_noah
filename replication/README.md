Our chatbot program is a Python application organized with the following directory structure. Notable files include:
* `app.py` - entrypoint
* `servers.json` - config file for setting host and ports of servers
* `memory_manager.py` - responsible for syncing and managing memory
* `grpc_client/server.py` - server/client functionality for chatbot
* `datastore/` - directory where memory is persisted in json format
* `chatbot.proto`- protobuf specification
* `test/` - directory for unittests
```
.
├── README.md
├── app.py
├── clean_datastore.py
├── grpc_chatbot
│   ├── datastore/
│   ├── grpc_client.py
│   ├── grpc_server.py
│   ├── helpers
│   │   ├── heartbeat_thread.py
│   │   ├── memory_manager.py
│   │   └── receiver_thread.py
│   └── proto_files
│       ├── build_protos.sh
│       ├── chatbot.proto
├── requirements.txt
├── server.json
└── tests/
```

Our chatbot is run via a python app in the parent directory:

``git clone {directory} && cd replication``

``pip install -r requirements.txt``


## To run the gRPC version:
  
1. In a terminal window, start the server.
    
    * COMMAND: ``python3 app.py —-mode server --server_id {server_id from servers.json}``
    
    * OUTPUT: ``GRPC Server started, listening on {port}``
   

2. In separate terminal window(s), start the client(s). 
    
    *  COMMAND: ``python3 app.y --mode client ``
    
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


# Testing

1. In the terminal, run the unit tests from the home directory:

``pytest -v test``

## To Generate Code Coverage Report

1. In the terminal, generate the coverage report:

``./generate_coverage_report.sh``

```
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
grpc_chatbot/grpc_client.py                   69     48    30%
grpc_chatbot/grpc_server.py                  137     46    66%
grpc_chatbot/helpers/heartbeat_thread.py      20      3    85%
grpc_chatbot/helpers/memory_manager.py       133     28    79%
grpc_chatbot/helpers/receiver_thread.py       26     18    31%
--------------------------------------------------------------
TOTAL                                        385    143    66%

```


# Engineering Notebook

You can find our engineering notebook at:

[EngineeringNotebook.md](https://github.com/marinaelmore/cs262_marina_noah/blob/main/README.md)


