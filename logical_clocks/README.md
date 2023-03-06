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
Feel free to edit `config.json` with the ports and hosts of interest.

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
.
├── app.py  #Script entry point
├── virtual_machine.py #code for running VMs
├── config.json #Editable config file where ports+machine ids are specified
├── output_files
│   └── {machine_id}.txt # folder for output logs, individual files ignored
├── requirements.txt
├── test # Test Directory
│   ├── test_main.py
│   └── test_virtual_machine.py
├── generate_coverage.sh #Bash file to generate code coverage statistics
├── EngineeringNotebook.md
└── README.md
```

# To Test

1. In the terminal, run the unit tests from the home directory:

``pytest -v test/``

```
============================= test session starts ==============================

test/test_main.py::TestApp::test_main PASSED                             [ 11%]
test/test_virtual_machine.py::TestVirtualMachineTest::test_init PASSED   [ 22%]
test/test_virtual_machine.py::TestVirtualMachineTest::test_queue_protocol PASSED [ 33%]
test/test_virtual_machine.py::TestVirtualMachineTest::test_start_server PASSED [ 44%]
test/test_virtual_machine.py::TestVirtualMachineTest::test_connect_to_other_machines PASSED [ 55%]
test/test_virtual_machine.py::TestVirtualMachineTest::test_send_clock_time PASSED [ 66%]
test/test_virtual_machine.py::TestVirtualMachineTest::test_tick_queue_empty PASSED [ 77%]
test/test_virtual_machine.py::TestVirtualMachineTest::test_tick_queue_has_item PASSED [ 88%]
test/test_virtual_machine.py::test_main PASSED                           [100%]

============================== 9 passed in 0.30s ===============================

```

# To Generate Code Coverage Report

1. In the terminal, generate the coverage reports from the home directory:

``./generate_coverage.sh``

```
Name                 Stmts   Miss  Cover
----------------------------------------
app.py                  14      1    93%
virtual_machine.py     114     29    75%
----------------------------------------
TOTAL                  128     30    77%
```

# Engineering Notebook

You can find our engineering notebook at:

[EngineeringNotebook.md](lhttps://github.com/marinaelmore/cs262_marina_noah/blob/main/logical_clocks/EngineeringNotebook.md)