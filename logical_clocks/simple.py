import asyncio
import random


queue = asyncio.Queue()

class VMProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        queue.put_nowait(message)
        print('Data received: {!r}'.format(message))

        # TO DO
        #print('Send: {!r}'.format(message))
        #self.transport.write(data)

        # TO DO
        #print('Close the client socket')
        #self.transport.close()


class VirtualMachine():

    def __init__(self, machine_id, clock_rate, output_log_path):
        # Initialize vars
        self.machine_id = machine_id
        self.clock_rate = clock_rate
        self.output_file = open(output_log_path, "w")
        self.logical_clock = []
    
    def update_logical_clock(self):
        print("update logical clock")

    async def run_vm_client(self):
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
                    #send to one of the other machines a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time
                    print("send msg to vm1") 
                elif randint == 2:
                    #end to the other virtual machine a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
                    print("send msg to vm2")
                elif randint == 3:
                    print("self to vm 2 and 3")
                else:
                    #if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.
                    print("Internal event")
            else:
                print("Queue Not Empty, Print Message")
                msg = queue.get_nowait()
                print(msg)
                queue.task_done()

            print('This round is finished, night night')


def main():
    loop = asyncio.get_event_loop()

    vm = VirtualMachine("machine1", 5, "output_files/templog.txt")

    print("Starting server task")
    start_server_task = loop.create_task(loop.create_server(VMProtocol, '127.0.0.1', 8000))

    print("Starting client task")
    start_client_task = loop.create_task(vm.run_vm_client())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

if __name__=="__main__":
    main()
