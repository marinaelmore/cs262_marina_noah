import asyncio
import random
import configparser
import datetime
import json


class VirtualMachine():

    def __init__(self, machine_id, my_machine, machine_2, machine_3):
        # Initialize vars
        print("ineher", my_machine)
        self.clock_rate = 1. / random.randrange(1, 7)
        self.output_file = open(my_machine['output_path'], "w")
        self.machine_id = machine_id
        self.my_machine = my_machine
        self.machine_2 = machine_2
        self.machine_3 = machine_3
        self.logical_clock = 0
        self.queue = asyncio.Queue()

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
        print("Starting server task on port {}".format(
            self.my_machine["port"]))
        start_server_task = await asyncio.start_server(self.queue_protocol, self.my_machine["host"], self.my_machine["port"])
        await start_server_task.serve_forever()

    async def connect_to_other_machines(self):
        first_attempt = True
        while True:
            try:
                self.machine_2["reader"], self.machine_2["stream"] = await asyncio.open_connection(self.machine_2["host"], self.machine_2["port"])
                self.machine_3["reader"], self.machine_3["stream"] = await asyncio.open_connection(self.machine_3["host"], self.machine_3["port"])
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

    async def send_clock_time(self, writer):
        message = f"{self.logical_clock}\n"
        writer.write(message.encode())
        await writer.drain()

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

            if self.queue.empty():
                print("Queue Empty, Roll the Dice")
                dice_roll = random.randrange(1, 10)
                await self.tick_queue_empty(dice_roll)
            else:
                self.tick_queue_has_item()
            print('This round is finished, night night\n\n')

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

        if len(machines) > 0:
            names = [m["name"] for m in machines]
            log_msg = f"send {names}, time {self.logical_clock}\n"
            print(log_msg)
            self.output_file.write(log_msg)
            for machine in machines:
                await self.send_clock_time(machine["stream"])

        self.logical_clock += 1
        self.output_file.flush()

    def tick_queue_has_item(self):
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


def main(machine_id):
    # Parse configurations
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

    vm = VirtualMachine(machine_id, my_machine, machine_2, machine_3)

    loop.create_task(vm.start_vm_server())
    loop.create_task(vm.run_vm_client())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
