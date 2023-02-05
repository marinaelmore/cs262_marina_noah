import re

#define memory manager class
class User:
    def __init__(self, username):
        self.username = username
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)



class MemoryManager:
    def __init__(self):
        self.users = {}
        print("This is happening")
        
    def create_user(self, username):
        self.users[username] = User(username)
        print(self.users)

    def send_message(self,to,message):
        if to in self.users:
            self.users[to].add_message(message)
            return True
        else:
            return False

    def get_message(self,username):
<<<<<<< HEAD
        if len(self.users[username].messages) > 0:
            message = self.users[username].messages.pop(0)
=======
        user_messages = self.users[username].messages
        if len(user_messages) > 0:
            message = user_messages.pop(0)
>>>>>>> 8a06bd01e8ffcc4e99f7dc2e727a8288f430babf
            return message
        return ""

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

        else:
            print("User does not exist")


