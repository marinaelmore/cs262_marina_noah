import asyncio
import random
import configparser
import datetime
import json

# A class to represent a virtual machine that
# will be used to simulate the logical clock
class VirtualMachine():

    def __init__(self, machine_id, my_machine, machine_2, machine_3):
        # Initialize vars

        # The clock rate is the number of seconds that the virtual machine
        # will sleep between actions. 
        self.clock_rate = 1. / random.randrange(1, 7)
        self.output_file = open(my_machine['output_path'], "w")
        self.machine_id = machine_id
        self.my_machine = my_machine
        # The other two machines that this machine will be communicating with
        self.machine_2 = machine_2
        self.machine_3 = machine_3
        self.logical_clock = 0
        # create one queue to store messages per virtual machine 
        self.queue = asyncio.Queue()

    # This function is responsible for listening for messages from
    # the other connected machines and adding them to the queue
    async def queue_protocol(self, reader, writer):
        # consistenly check for messages from the other machines
        while True:
            request = await reader.readline()
            try:
                self.queue.put_nowait(int(request.decode()))
            except ValueError:
                print("Received non-integer message")
            if reader.at_eof():
                break
        writer.close()

    # start the server task which listens for 
    # messages from other machines
    async def start_vm_server(self):
        print("Starting server task on port {}".format(
            self.my_machine["port"]))
        start_server_task = await asyncio.start_server(self.queue_protocol, self.my_machine["host"], self.my_machine["port"])
        await start_server_task.serve_forever()

    # This function is responsible for connecting to the other
    # virtual machines defined in the config file
    async def connect_to_other_machines(self):
        first_attempt = True
        # Keep trying to connect to the other machines until
        # a connection is established
        while True:
            try:
                self.machine_2["reader"], self.machine_2["stream"] = await asyncio.open_connection(self.machine_2["host"], self.machine_2["port"])
                self.machine_3["reader"], self.machine_3["stream"] = await asyncio.open_connection(self.machine_3["host"], self.machine_3["port"])
                print()
                break
            # if the other machines are not yet initialized,
            #  wait for a short delay before retrying
            except ConnectionRefusedError:
                # Connection failed, wait for a short delay before retrying
                # Sets up a nice little loading bar to show that we are waiting
                if first_attempt:
                    print(
                        "Peer VMs not initialized, retrying in 1 second", end="", flush=True)
                    first_attempt = False
                else:
                    print(".", end="", flush=True)
                await asyncio.sleep(1)
    
    # This function is responsible for sending 
    # the current logical clock, returns True or False if 
    # the message was sent successfully so that the caller
    # can decide whether to retry
    async def send_clock_time(self, writer):
        message = f"{self.logical_clock}\n"
        writer.write(message.encode())
        try: 
            await writer.drain()
            return True
        except ConnectionResetError:
            return False
             
    # This function is responsible for running the client task
    # It will read from the queue and send messages to the other
    # virtual machines
    async def run_vm_client(self):
        self.output_file.write("Starting VM\n")

        print("Connecting to other machines")
        await self.connect_to_other_machines()

        print("Connected and listening for messages....")
        self.output_file.write("Connected and listening for messages...\n")

        # Start the server task
        while True:
            # Sleep for the clock rate seconds.
            await asyncio.sleep(self.clock_rate)

            print("\n\n{} has slept for {} seconds".format(
                self.machine_id, self.clock_rate))

            # If the queue is empty we will roll the dice to determine
            # which machine to send a message to
            if self.queue.empty():
                print("Queue Empty, Roll the Dice")
                dice_roll = random.randrange(1, 10)
                await self.tick_queue_empty(dice_roll)
            else:
                # If the queue is not empty, we will read from the queue
                self.tick_queue_has_item()
            print('This round is finished, night night\n\n')

    # This function is responsible for handling the case where the queue is empty
    # It takes a dice roll as an argument and will send a message to the other
    # virtual machines based on the dice roll or process an internal event.
    async def tick_queue_empty(self, dice_roll):
        machines = []
        if dice_roll == 1:
            machines = [self.machine_2]
        elif dice_roll == 2:
            machines = [self.machine_3]
        elif dice_roll == 3:
            machines = [self.machine_2, self.machine_3]
        else:
            # if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.
            log_msg = f"internal, time {self.logical_clock}\n"
            print(log_msg)
            self.output_file.write(log_msg)

        # Based on the dice roll, send messages to the proper machines
        if len(machines) > 0:
            names = [m["name"] for m in machines]
            log_msg = f"send {names}, time {self.logical_clock}\n"
            print(log_msg)
            self.output_file.write(log_msg)

            for machine in machines:

                send_success = await self.send_clock_time(machine["stream"])
                # try to reconnect to the machine if the message was not sent successfully
                # due to a connection failure
                while not send_success:
                    print("Attempting to reconnect to other machines...")
                    await self.connect_to_other_machines() 
                    send_success = await self.send_clock_time(machine["stream"])

        # update local logical clock
        self.logical_clock += 1
        # write logs to file
        self.output_file.flush()

    # This function is responsible for handling the case where the queue is not empty
    # It will read from the queue and update the local logical clock
    def tick_queue_has_item(self):
        print("Queue Length: {}. Printing Message".format(
            self.queue.qsize()))
        msg = self.queue.get_nowait()
        print("--> Message: {}\n".format(msg))
        # Updates the logical clock to the max of the current logical clock and the message
        # received from the queue + 1 which gives us the new overall time.
        self.logical_clock = max(self.logical_clock, msg) + 1

        log_msg = f"receive, global time {datetime.datetime.now()}, new time {self.logical_clock}, queue length {self.queue.qsize()}\n"
        print(log_msg)
        # Write log file and flush to disk.
        self.output_file.write(log_msg)
        self.queue.task_done()
        self.output_file.flush()

# wrapper function which actually starts the vritual machine and setups the client and server tasks
def run_virtual_machine(machine_id):
    # Parse configuration
    json_data = open('config.json').read()
    config = json.loads(json_data)


    if machine_id in config.keys():
        my_machine = config[machine_id]
        # set machine 2 and 3 to the other 2 machine ids
        other_machines = [x for x in config.keys() if x != machine_id]
        machine_2 = config[other_machines[0]]
        machine_3 = config[other_machines[1]]
    else:
        print("Machine name does not exist")
        return None

    # Start Loop
    loop = asyncio.get_event_loop()

    # initialize the virtual machine
    vm = VirtualMachine(machine_id, my_machine, machine_2, machine_3)

    # create the server and client tasks
    loop.create_task(vm.start_vm_server())
    loop.create_task(vm.run_vm_client())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
