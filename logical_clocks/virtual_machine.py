# Each model machine will run at a clock rate determined during initialization. You will pick a random number between 1 and 6, and that will be the number of clock ticks per (real world) second for that machine. This means that only that many instructions can be performed by the machine during that time. Each machine will also have a network queue (which is not constrained to the n operations per second) in which it will hold incoming messages. The (virtual) machine should listen on one or more sockets for such messages.

# Each of your virtual machines should connect to each of the other virtual machines so that messages can be passed between them. Doing this is part of initialization, and not constrained to happen at the speed of the internal model clocks. Each virtual machine should also open a file as a log. Finally, each machine should have a logical clock, which should be updated using the rules for logical clocks.

# SET UP
# Initialize clock rate (rand int)
# Initialize network queue
# Connect to other virtual machines, listen on one or more sockets for such messages
# Open file as a log
# Initialize logical clock

# On each clock cycle, if there is a message in the message queue for the machine (remember, the queue is not running at the same cycle speed) the virtual machine should take one message off the queue, update the local logical clock, and write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.

import asyncio
import random
import configparser
import datetime


class VirtualMachine():

    def __init__(self, machine_id, output_log_path, host, myport, port2, port3):
        # Initialize vars
        self.machine_id = machine_id
        self.clock_rate = 1. / random.randrange(1, 7)
        self.output_file = open(output_log_path, "w")
        self.logical_clock = 0
        self.host = host
        self.my_port = myport
        self.queue = asyncio.Queue()
        self.machine_2_port = port2
        self.machine_3_port = port3

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

    async def connect_to_other_machines(self):
        first_attempt = True
        while True:
            try:
                self.reader2, self.stream2 = await asyncio.open_connection(self.host, self.machine_2_port)
                self.reader3, self.stream3 = await asyncio.open_connection(self.host, self.machine_3_port)
                print()
                break
            except ConnectionRefusedError:
                # Connection failed, wait for a short delay before retrying
                if first_attempt:
                    print(
                        "Peer VMs not initialized, retrying in 1 second", end="", flush=True)
                    first_attempt = False
                else:
                    print(".", end="", flush=True)
                await asyncio.sleep(1)

    async def send_clock_time(self, port):
        message = f"{self.logical_clock}\n"

        if port == self.machine_2_port:
            self.stream2.write(message.encode())
            await self.stream2.drain()

        if port == self.machine_3_port:
            self.stream3.write(message.encode())
            await self.stream3.drain()

    async def run_vm_client(self):
        self.output_file.write("Starting VM\n")

        print("Connecting to other machines")
        await self.connect_to_other_machines()

        print("Connected and listening for messages....")
        self.output_file.write("Connected and listening for messages...\n")

        while True:
            # Sleep for the clock rate seconds.
            await asyncio.sleep(self.clock_rate)

            print("\n\n{} has slept for {} seconds".format(
                self.machine_id, self.clock_rate))

            # print queue length

            if self.queue.empty():
                print("Queue Empty, Roll the Dice")
                randint = random.randrange(1, 10)
                ports = []
                if randint == 1:
                    ports = [self.machine_2_port]
                elif randint == 2:
                    ports = [self.machine_3_port]
                elif randint == 3:
                    ports = [self.machine_2_port, self.machine_3_port]
                else:
                    # if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.
                    log_msg = f"internal, time {self.logical_clock}\n"
                    print(log_msg)
                    self.output_file.write(log_msg)

                if len(ports) > 0:
                    log_msg = f"send {ports}, time {self.logical_clock}\n"
                    print(log_msg)
                    self.output_file.write(log_msg)
                    for port in ports:
                        await self.send_clock_time(port)

                self.logical_clock += 1

            else:
                print("Queue Length: {}. Printing Message".format(
                    self.queue.qsize()))
                msg = self.queue.get_nowait()
                print("--> Message: {}\n".format(msg))
                self.logical_clock = max(self.logical_clock, msg) + 1

                # update local logical clock
                log_msg = f"receive, global time {datetime.datetime.now()}, new time {self.logical_clock}, queue length {self.queue.qsize()}\n"
                print(log_msg)
                self.output_file.write(log_msg)
                self.queue.task_done()

            self.output_file.flush()
            print('This round is finished, night night\n\n')


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
        m2port = config['machine_1']['port']
        m3port = config['machine_2']['port']
        output_path = config['machine_3']['output_path']
    else:
        print("Machine name does not exist")
        return None

    # Start Loop
    loop = asyncio.get_event_loop()

    vm = VirtualMachine(machine_id, output_path,
                        myhost, myport, m2port, m3port)

    loop.create_task(vm.start_vm_server())
    loop.create_task(vm.run_vm_client())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
