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