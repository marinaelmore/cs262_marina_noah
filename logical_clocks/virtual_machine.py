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
import sys
import socket
from vm_protocol import VMProtocol
import configparser

queue = asyncio.Queue()

class VMProtocol(asyncio.Protocol):

    def connection_made(self, socket):
        peername = socket.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.socket = socket

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        queue.put_nowait(message)


class VirtualMachine():

    def __init__(self, machine_id, clock_rate, output_log_path):
        # Initialize vars
        self.machine_id = machine_id
        self.clock_rate = clock_rate
        self.output_file = open(output_log_path, "w")
        self.logical_clock = []

    async def connect_to_other_machine(self, host, port):
        self.reader1,self.stream1 = await asyncio.open_connection(host, port)

    def update_logical_clock(self):
        print("update logical clock")

    async def send_message(self, machine_id):
        message = "yoooo"

        self.output_file.write("Sending message to Machine {}".format(machine_id))

        self.stream1.write(message.encode())        
        await self.stream1.drain()

    async def run_vm_client(self, m1port, m2port):
        self.output_file.write("Starting VM\n")
        self.output_file.write("Listening for messages...\n")

        while True:
            # Sleep for the clock rate seconds.
            await asyncio.sleep(self.clock_rate)

            print(f'{self.machine_id} has slept for {self.clock_rate:.2f} seconds')

            if queue.empty():
                print("Queue Empty, Roll the Dice")
                randint = random.randrange(1, 10) 

                if randint == 1:
                    print("send msg to vm1") 
                    self.send_message(machine_id="machine1")
                    print("sent\n") 
                
                elif randint == 2:
                    print("send msg to vm2")
                    self.send_message(machine_id="machine2")
                    print("sent\n") 
                
                elif randint == 3:
                    print("send to vm 2 and 3\n")
                
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
        m1port = config['machine_2']['port']
        m2port = config['machine_3']['port']
        output_path = config['machine_1']['output_path']
    elif machine_id == "machine_2":
        myhost = config['machine_1']['host']
        myport = config['machine_1']['port']
        m1port = config['machine_1']['port']
        m2port = config['machine_3']['port']
        output_path = config['machine_1']['output_path']
    elif machine_id == "machine3":
        myhost = config['machine_1']['host']
        myport = config['machine_1']['port']
        m1port = config['machine_2']['port']
        m2port = config['machine_1']['port']
        output_path = config['machine_1']['output_path']
    else:
        print("Machine name does not exist")
        return None

    # Start Loop
    loop = asyncio.get_event_loop()


    print("Starting server task")
    start_server_task = loop.create_task(start_vm_server(myhost, myport))

    clock_rate = 5
    vm = VirtualMachine(machine_id, clock_rate, output_path)

    print("Starting client task")
    start_client_task = loop.create_task(vm.run_vm_client(m1port, m2port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass