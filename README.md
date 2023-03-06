# Engineering Notebook
Marina Elmore + Noah Zweben for CS 262

# Assignment 2: Logical Clocks

29 Feb

Having issues with the server calls - not adding messages to the queue when passing protocol construct for the server:
```
class VMProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost


Error Message: TypeError: VMProtocol() takes no arguments
```
* Issue: passing a protocol to the server was for the lower level implementation (create_server) rather than the higher level protocol that we were using (start_server) that needed to take in a function with inputs reader, writer
*  Solution: Passing queueing function to the server call with asyncio queue
```
    async def queue_protocol(self, reader, writer):
        while True:

            request = await reader.readline()
            try:
                self.queue.put_nowait(int(request.decode()))
            except ValueError:
                print("Received non-integer message")
            if reader.at_eof():
                break
        writer.close()

    async def start_vm_server(self):
        print("Starting server task on port {}".format(self.my_port))
        start_server_task = await asyncio.start_server(self.queue_protocol, self.host, self.my_port)
        await start_server_task.serve_forever()

```

4 March

Creating config.json file to pass in attributes of machines so that no modifications to source code need to be made. This will also allow us to pass a Machine dataobject rather than fields for port, machine_id, etc.
```
{
    "machine_1": {
        "name": "Machine 1",
        "port": 8000,
        "host": "127.0.0.1",
        "output_path": "output_files/machine_1.txt"
  }
  
  await asyncio.open_connection(self.machine_2["host"], self.machine_2["port"])
```

5 March
```
  File "/Users/marina/Documents/*HBS*/*EC*/CS262/cs262_marina_noah/logical_clocks/virtual_machine.py", line 61, in send_clock_time
    await self.stream2.drain()
  File "/Users/marina/opt/anaconda3/lib/python3.8/asyncio/streams.py", line 387, in drain
    await self._protocol._drain_helper()
  File "/Users/marina/opt/anaconda3/lib/python3.8/asyncio/streams.py", line 190, in _drain_helper
    raise ConnectionResetError('Connection lost')
```
* Issue: Need to add try/expect for the connection lost possibility. In addition, how to keep it so that they retry connection upon connection lost?
* Solution: Updated send to catch error when connection lost and return a bool if message was sent sucecssful. If failure -> machine attempts to reconnect to other machines.
```
    if port == self.machine_2_port:
        self.stream2.write(message.encode())
        try:
            await self.stream2.drain()
            return True
        except ConnectionResetError as connection_lost:
            return False
```

# Assignment One: Chatbot

* In implementing our wireprotcol, it was amazing and disappointing to see how little control over the underlying bytes python afforded. C for the win!
* When we shifted from our own wire protocol -> gRPC, we realized the way we had been managing client login state on the server was less than ideal. We then improved our design to use a stateless server (similar to HTTP) where the gRPC server sets a login "cookie" for the client, which the client uses in subsequent requests. This was much cleaner.
* Implemeting helper functions as a reusable module was helpful for reducing code.
