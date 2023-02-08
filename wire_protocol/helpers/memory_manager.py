import re

# define memory manager class


class User:
    def __init__(self, username):
        self.username = username
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)


class MemoryManager:
    def __init__(self):
        self.users = {}

    def create_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
            return True
        else:
            return False

    def send_message(self, sender, to, message):
        if (sender in self.users) and (to in self.users):
            self.users[to].add_message(f"{sender}: {message}")
            print(f"Messages of {to}: {self.users[to].messages}")
            return True
        else:
            return False

    def get_message(self, username):
        if username in self.users:
            messages = self.users[username].messages
            if len(messages) > 0:
                msg = messages.pop(0)
                return msg
        return None

    def list_users(self, wildcard):

        matches = []
        print(self.users)
        print(wildcard)

        try:
            matches = [user for user in self.users if re.match(wildcard, user)]

        except Exception:
            print("Poorly formatted search regex. Please try again")

        return matches

    def delete_user(self, username):

        print("Deleting user {}".format(username))

        if username in self.users:
            self.users.pop(username)
            print("Deleted user: {}".format(username))
            return True

        else:
            print("User does not exist")
            return False
