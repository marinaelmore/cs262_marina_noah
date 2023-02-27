#Each model machine will run at a clock rate determined during initialization. You will pick a random number between 1 and 6, and that will be the number of clock ticks per (real world) second for that machine. This means that only that many instructions can be performed by the machine during that time. Each machine will also have a network queue (which is not constrained to the n operations per second) in which it will hold incoming messages. The (virtual) machine should listen on one or more sockets for such messages.

#Each of your virtual machines should connect to each of the other virtual machines so that messages can be passed between them. Doing this is part of initialization, and not constrained to happen at the speed of the internal model clocks. Each virtual machine should also open a file as a log. Finally, each machine should have a logical clock, which should be updated using the rules for logical clocks.

# SET UP
# Initialize clock rate (rand int)
# Initialize network queue
# Connect to other virtual machines, listen on one or more sockets for such messages
# Open file as a log
# Initialize logical clock

class Message():
    def __init__(self):
        self.timestamp = None
        self.message = ""

class VirtualMachine():

    def __init__(self, clock_rate, output_log_path):
        self.clock_rate = clock_rate
        self.output_logpath = open(output_log_path, "rw")

    
    def send_message(curr_time):
        msg = Message(curr_time, "Hello from the Other Side")




