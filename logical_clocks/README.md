# Scale Models and Logical Clocks
<hr>
Implementation of a distributed 3-machine VM system that use logical clocks to internally keep track of system time as messages are sent between machines.
<hr>

# Installation #
To setup this project:

```zsh
git clone https://github.com/marinaelmore/cs262_marina_noah.git
cd logical_clocks
pip install -r requirements.txt
```

# To Run #
Within `logical_clocks/` open 3 different terminals (one for each virtual machine)
```zsh
#Terminal 1:
python app.py --machine_id machine_1

#Terminal 2:
python app.py --machine_id machine_2

#Terminal 3:
python app.py --machine_id machine_3
```

Each command will initialize a VM and attempt to connect to the other machines. Expected output should be:

```
Starting server task on port 8000
Connecting to other machines
Peer VMs not initialized, retrying in 1 second....
```

Once all peer VMs are found, the program will output
```
Connected and listening for messages....
```
and begin the dice-rolling logical clock loop.


# Directory Structure #
```zsh
. #logical_clocks
├── app.py #Script entry point
├── config.ini #Editable config file where ports+machine ids are specified
├── virtual_machine.py #code for running VMs
├── output_files # folder for output logs, individual files ignored
│   ├── {machine_id}.txt
```
