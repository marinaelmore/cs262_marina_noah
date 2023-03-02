import asyncio

class VMProtocol(asyncio.Protocol):

    def connection_made(self, socket):
        peername = socket.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.socket = socket

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        