# Engineering Notebook
Marina Elmore + Noah Zweben for CS 262

# Assignment 3: Replication
## Implementation
4 April
* Decided to implement replication using the backup-server approach from the reading/lecture. We agreed on an architecture diagram and stages for implementation: (1) persistance, (2) replication on one machine, (3) networking of replication across two machines.
* #1: Persistance
    * Used shared memory to write to JSON blob
    * Replicate JSON blob across all machines - how are we going to do this? How are we going to name the file?
* #2: Replication on One Machine
    * Promote backup to primary server and load from JSON blob
* #3: Networking for Replication
   * Implementation TBD

# Assignment 2: Logical Clocks
## Logical Clock Observations:
* Queue buildup occurs when the slower rate falls roughly into the formula `# slower ticks per second < # faster ticks per second / 5` where the tick rate is the random number 1-6 that dicatates # of ticks. The 1/5 factor is derived from the fact that about 1/5th of the messages from the faster process end up in the slower process's queue (this is because dice rolls 1&3 out of 10 possible rolls send a message to a given queue). The formula is not a hard and fast rule, but generally applies. The greater the faster term is (`# slower ticks per second <<< # faster ticks per second` ), the larger the jumps in the logical clocks are upon reading from the queue (~8-10) and the larger buildup there are in the queues. As the ticks rates approach equal the junmps becomes smaller (~1-2). Changes to the internal event rate are discussed beloww.
* Changing the range of possible tick rates makes it more likely we have larger clock drift - specifically the larger the range, the more likely that we have clock drift
* As we make internal events more likely, we also get larger jumps in the clock (since they sync more infrequently). Internal events 
* As internal event rates become more likely, the slower queue builds up less, but the jumps are larger.
* Really slow clock frequencies start drifting more from actual system time.
* Using sockets provided the most scalable and extensive architecture (over piping). Allows extending across the network in the future
* Smaller differences in tick rates can make predicting timing of the system easier.

## Logical Clock: Implementation
After some trial and error, we decided to use the python asyncio library to facilitate the creation of three virtual machines. We choose this library because it has built in queue functionality and because you can pass a function to the server that will add items to the queue. In addition, because aysncio provides high-level implementations of the socket functionality, it allowed us to simplify our networking code and focus on the logical clock implementation

Please refer to our 
[README.md](https://github.com/marinaelmore/cs262_marina_noah/blob/main/logical_clocks/README.md) for more information on how we chose to implement this assignment. 

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
