# if runnign as a script delete all files matching pattern message_store.*.json
import os
import re
if __name__ == '__main__':
    for filename in os.listdir("grpc_chatbot/datastore"):
        # check filename against regex
        if re.match(r"message_store.+.json", filename):
            # delete file
            os.remove(os.path.join("grpc_chatbot/datastore", filename))
