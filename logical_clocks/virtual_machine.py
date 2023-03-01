#Each model machine will run at a clock rate determined during initialization. You will pick a random number between 1 and 6, and that will be the number of clock ticks per (real world) second for that machine. This means that only that many instructions can be performed by the machine during that time. Each machine will also have a network queue (which is not constrained to the n operations per second) in which it will hold incoming messages. The (virtual) machine should listen on one or more sockets for such messages.

#Each of your virtual machines should connect to each of the other virtual machines so that messages can be passed between them. Doing this is part of initialization, and not constrained to happen at the speed of the internal model clocks. Each virtual machine should also open a file as a log. Finally, each machine should have a logical clock, which should be updated using the rules for logical clocks.

# SET UP
# Initialize clock rate (rand int)
# Initialize network queue
# Connect to other virtual machines, listen on one or more sockets for such messages
# Open file as a log
# Initialize logical clock
import socket

class VirtualMachine():

    def __init__(self, machine_id, clock_rate, output_log_path, clientsocket, port):
        # Initialize vars
        self.machine_id = machine_id
        self.clock_rate = clock_rate
        self.output_file = open(output_log_path, "rw")
        self.logical_clock = []
    
    def connect_to_other_vms(self, machine1_id, machine2_id):
        print("TO DO")

    def send(self, destination_machine_id, message):
        try:
            self.queue[destination_machine_id].put(message, block=False)
        except Exception as e:
            return None


    def recieve(self):
        try:
            self.queue[self.machine_id].get(block=False)
        except Exception as e:
            return None

def run_vm(host, port):
    #self.output_file.write("Starting VM")
    #self.output_file.write("Listening for messages...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        client_socket.send(b"howdy")

def main():
    run_vm("0.0.0.0", 8080)
    run_vm("0.0.0.0", 8081)
    run_vm("0.0.0.0", 8000)
        

if __name__ == '__main__':
    main()