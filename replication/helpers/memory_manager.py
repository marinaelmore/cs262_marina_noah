import re
import json


# A User class which stores a username and a list of messages sent to them
class User:
    def __init__(self, username):
        self.username = username
        self.messages = []

    # appends a message to the list of messages
    def add_message(self, message):
        self.messages.append(message)

    def user_to_dict(self):
        return {self.username : self.messages}


class MemoryManager:
    def __init__(self):
        self.users = {}
        self.filename = ""

    def initialize_memory(self, filename):
        self.filename = filename
        with open(self.filename, 'r') as message_store:
            print("Initializing memory from data store....")
            message_blob = json.loads(message_store.read())

            for username, msgs in message_blob.items():
                self.create_user(username)
                self.users[username].messages = msgs

        print("Initialization Complete...")

    def json_dump_users(self):
        with open(self.filename, 'w') as message_store:
            users_dict = {}
            for username,user_obj in self.users.items():
                users_dict[username] = user_obj.messages
            json.dump(users_dict, message_store)


    # Adds a new user to the memory manager
    def create_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
            self.json_dump_users()
            return True
        else:
            return False
        

    # Sends a message from one user to another
    def send_message(self, sender, to, message):
        if (sender in self.users) and (to in self.users):
            self.users[to].add_message(f"{sender}: {message}")
            print(f"Messages of {to}: {self.users[to].messages}")
            self.json_dump_users()
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
                self.json_dump_users()
                return msg
        return None

    # Lists all users that match a wildcard
    def list_users(self, wildcard):

        matches = []
        print(self.users)
        print(wildcard)

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
            self.json_dump_users()
            return True

        else:
            print("User does not exist")
            return False
