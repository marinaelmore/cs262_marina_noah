from threading import Thread
from time import sleep
from ..proto_files import chatbot_pb2


class HeartbeatThread(Thread):

    def __init__(self, backup_servers, server_id):
        Thread.__init__(self)
        self.backup_servers = backup_servers
        self.server_id = server_id
        # keep track of the logged in user at the client thread level
        self.start()

    def run(self):
        while True:
            # every 0.5 seconds set heartbeat message to all backup servers
            for backup_server in self.backup_servers:
                try:
                    backup_server.heartbeat(
                        chatbot_pb2.Heartbeat(server_id=self.server_id))
                except:
                    pass
            sleep(0.5)
