Our chatbot program is a Python application organized with the following directory strucutre
Notable files include:
* `app.py` - entrypoint
* `servers.json` - config file for setting host and ports of servers
* `memory_manager.py` - responsible for syncing and managing memory
* `grpc_client/server.py` - server/client functionality for chatbot
* `datastore/*` - directory where memory is persisted in json format
* `chatbot.proto`- protobuf specification
```
.
├── README.md
├── app.py
├── clean_datastore.py
├── grpc_chatbot
│   ├── datastore
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
├── servers.json
└── unit_test.py
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


