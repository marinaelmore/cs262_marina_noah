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
        
    def create_user(self, username):
        self.users[username] = User(username)
        print(self.users)
    
