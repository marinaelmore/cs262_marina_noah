#Each model machine will run at a clock rate determined during initialization. You will pick a random number between 1 and 6, and that will be the number of clock ticks per (real world) second for that machine. This means that only that many instructions can be performed by the machine during that time. Each machine will also have a network queue (which is not constrained to the n operations per second) in which it will hold incoming messages. The (virtual) machine should listen on one or more sockets for such messages.

#Each of your virtual machines should connect to each of the other virtual machines so that messages can be passed between them. Doing this is part of initialization, and not constrained to happen at the speed of the internal model clocks. Each virtual machine should also open a file as a log. Finally, each machine should have a logical clock, which should be updated using the rules for logical clocks.

# SET UP
# Initialize clock rate (rand int)
# Initialize network queue
# Connect to other virtual machines, listen on one or more sockets for such messages
# Open file as a log
# Initialize logical clock

#On each clock cycle, if there is a message in the message queue for the machine (remember, the queue is not running at the same cycle speed) the virtual machine should take one message off the queue, update the local logical clock, and write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.

import asyncio
import random
import configparser

queue = asyncio.Queue()



class VMProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        message = data.decode()
        queue.put_nowait(message)

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)

class VirtualMachine():

    def __init__(self, machine_id, clock_rate, output_log_path, port2, port3):
        # Initialize vars
        self.machine_id = machine_id
        self.clock_rate = clock_rate
        self.output_file = open(output_log_path, "w")
        self.logical_clock = []
        self.machine_2_port = port2
        self.machine_3_port = port3

    async def connect_to_other_machines(self, host, port2, port3):
        while True:
            try:
                self.reader2, self.stream2 = await asyncio.open_connection(host, port2)
                self.reader3, self.stream3 = await asyncio.open_connection(host, port3)
                break
            except ConnectionRefusedError:
                # Connection failed, wait for a short delay before retrying
                await asyncio.sleep(1)

    def update_logical_clock(self):
        print("update logical clock")

    async def send_message(self, port):
        message = "yoooo"

        self.output_file.write("Sending message to machine at port: {}\n".format(port))

        if port == self.machine_2_port:
            self.stream2.write(message.encode())        
            await self.stream2.drain()
        if port == self.machine_3_port:
            self.stream3.write(message.encode())        
            await self.stream3.drain()

    async def run_vm_client(self,host, m2port, m3port):
        print("Starting client task")
        self.output_file.write("Starting VM\n")

        print("Connecting to other machines")
        await self.connect_to_other_machines(host, m2port, m3port)
        
        print("Listening for messages....")
        self.output_file.write("Listening for messages...\n")

        while True:
            # Sleep for the clock rate seconds.
            await asyncio.sleep(self.clock_rate)

            print(f'{self.machine_id} has slept for {self.clock_rate:.2f} seconds')

            if queue.empty():
                print("Queue Empty, Roll the Dice")
                randint = random.randrange(1, 10) 

                if randint == 1:
                    print("send msg to vm2") 
                    await self.send_message(m2port)
                    print("sent\n") 
                
                elif randint == 2:
                    print("send msg to vm3")
                    await self.send_message(m3port)
                    print("sent\n") 
                
                elif randint == 3:
                    print("send to vm 2 and 3\n")
                    await self.send_message(m2port)
                    await self.send_message(m3port)
                
                else:
                    #if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.
                    print("Internal event\n")
            else:
                print("Queue Not Empty, Print Message\n")
                msg = queue.get_nowait()
                print(msg)
                queue.task_done()

            print('This round is finished, night night\n\n')

async def start_vm_server(host, port):
    print("Starting server task on port {}".format(port))
    start_server_task = await asyncio.start_server(VMProtocol, host, port)

    async with start_server_task:
        await  start_server_task.serve_forever()

def main(machine_id):
    # Parse configurations

    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')

    if machine_id == "machine_1":
        myhost = config['machine_1']['host']
        myport = config['machine_1']['port']
        m2port = config['machine_2']['port']
        m3port = config['machine_3']['port']
        output_path = config['machine_1']['output_path']
    elif machine_id == "machine_2":
        myhost = config['machine_2']['host']
        myport = config['machine_2']['port']
        m2port = config['machine_1']['port']
        m3port = config['machine_3']['port']
        output_path = config['machine_2']['output_path']
    elif machine_id == "machine_3":
        myhost = config['machine_3']['host']
        myport = config['machine_3']['port']
        m2port = config['machine_2']['port']
        m3port = config['machine_1']['port']
        output_path = config['machine_3']['output_path']
    else:
        print("Machine name does not exist")
        return None

    # Start Loop
    loop = asyncio.get_event_loop()

    start_server_task = loop.create_task(start_vm_server(myhost, myport))

    #clock_rate = random.randint(1,6)
    clock_rate = 5
    vm = VirtualMachine(machine_id, clock_rate, output_path, m2port, m3port)
    
    start_client_task = loop.create_task(vm.run_vm_client(myhost, m2port, m3port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
