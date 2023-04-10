import re
import json
import jsonpatch
import hashlib
from ..proto_files import chatbot_pb2
import threading
import grpc

# A User class which stores a username and a list of messages sent to them


class User:
    def __init__(self, username):
        self.username = username
        self.messages = []

    # appends a message to the list of messages
    def add_message(self, message):
        self.messages.append(message)

    def user_to_dict(self):
        return {self.username: self.messages}


class MemoryManager:
    def __init__(self, primary, backup_servers, filename):
        self.users = {}
        self.primary = primary
        self.backup_servers = backup_servers
        self.filename = filename
        self.state = {}
        self.state_hash = hashlib.sha256(
            json.dumps(self.state, sort_keys=True).encode('utf-8')).hexdigest()

        self.initialize_memory()

    def set_primary(self, primary):
        old_primary = self.primary
        self.primary = primary
        if primary and not old_primary:
            self.initialize_memory()


    # this func called in server file to initialize memory
    def initialize_memory(self):
        #list through all the backup servers and get the full state
        for backup_server in self.backup_servers:
            result = self.get_state_from_primary(backup_server)
            if result:
                print("received result from primary server")
                return
        # try to open the file, if it does not exist, create it
        
        try:
            print("opening file", self.filename)
            with open(self.filename, 'r') as message_store:
                message_blob = json.loads(message_store.read())
                for username, msgs in message_blob.items():
                    self.create_user(username)
                    self.users[username].messages = msgs
        #if FIleNotFoundError or JSONDecodeError, create the file
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print("creating file", self.filename)
            with open(self.filename, 'w') as message_store:
                pass
        self.persist_and_replicate()

    def sync_state(self, from_hash, to_hash, diff):
        # check if the hashes match
        if from_hash == self.state_hash:
            # apply the diff to the state
            patch = jsonpatch.JsonPatch.from_string(diff)
            self.state = patch.apply(self.state)
            self.state_hash = hashlib.sha256(
                json.dumps(self.state, sort_keys=True).encode('utf-8')).hexdigest()
            # write the new state to the file
            with open(self.filename, 'w') as message_store:
                json_memory = json.dumps(self.state, sort_keys=True)
                message_store.write(json_memory)
        else:
            print("Hashes do not match, cannot sync state, refetching all memory")
            # get the full state from the primary server, in a new thread
            for backup in self.backup_servers:
                t = threading.Thread(
                    target=self.get_state_from_primary,args=([backup]))
                t.start()

    def get_state_from_primary(self, backup_server):
        try:
            print("Getting full state from primary server...")
            full_state = backup_server.get_full_state(
                chatbot_pb2.Empty())
            # load state into memory
            self.state = json.loads(full_state.state)
            #load all users
            for username, msgs in self.state.items():
                self.create_user(username)
                self.users[username].messages = msgs
            self.persist_and_replicate()
            return True
        except grpc.RpcError as e:
            return False


    def memory_to_dict(self):
        users_dict = {}
        for username, user_obj in self.users.items():
            users_dict[username] = user_obj.messages.copy()
        return users_dict

    def persist_and_replicate(self):
        if self.primary:
            users_dict = self.memory_to_dict()
            # hash users_dict and store hash in self.state_hash
            old_state = self.state
            old_hash = self.state_hash
            json_memory = json.dumps(users_dict, sort_keys=True)
            new_hash = hashlib.sha256(
                json_memory.encode('utf-8')).hexdigest()

            self.state = users_dict
            self.state_hash = str(new_hash)

            # persistance and replication operations
            patch = jsonpatch.make_patch(old_state, users_dict)
            print(old_state),
            print(users_dict)
            print("diff", patch)
            with open(self.filename, 'w') as message_store:
                message_store.write(json_memory)
            for backup in self.backup_servers:
                # these are non blocking to make sure the server does not hang
                try:
                    backup.sync_state(chatbot_pb2.SyncRequest(
                        from_hash=str(old_hash), to_hash=str(new_hash), diff=f"{patch}"))
                except Exception as e:
                    pass

    # Adds a new user to the memory manager

    def create_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
            self.persist_and_replicate()
            return True
        else:
            return False

    # Sends a message from one user to another

    def send_message(self, sender, to, message):
        if (sender in self.users) and (to in self.users):
            self.users[to].add_message(f"{sender}: {message}")
            print(f"Messages of {to}: {self.users[to].messages}")
            self.persist_and_replicate()
            return True
        else:
            return False

    # Gets the first message in the list of messages for a user,
    # and removes it from the list
    def get_message(self, username):
        if username in self.users:
            messages = self.users[username].messages
            if len(messages) > 0:
                msg = messages.pop(0)
                self.persist_and_replicate()
                return msg
        return None

    # Lists all users that match a wildcard
    def list_users(self, wildcard):
        matches = []
        try:
            matches = [user for user in self.users if re.match(wildcard, user)]

        except Exception:
            print("Poorly formatted search regex. Please try again")

        return matches

    # Deletes a user from the memory manager
    def delete_user(self, username):

        print("Deleting user {}".format(username))

        if username in self.users:
            self.users.pop(username)
            print("Deleted user: {}".format(username))
            self.persist_and_replicate()
            return True

        else:
            print("User does not exist")
            return False
