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
. #logical_clocks
├── app.py #Script entry point
├── config.ini #Editable config file where ports+machine ids are specified
├── virtual_machine.py #code for running VMs
├── output_files # folder for output logs, individual files ignored
│   ├── {machine_id}.txt
```

## To Test

1. In the terminal, run the unit tests from the home directory:

``pytest -v test/``

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

## To Generate Code Coverage Report

1. In the terminal, generate the coverage reports:
   
``coverage run -a test/test_main.py

  coverage run -a test/test_virtual_machine.py``

2. Combine and output the coverage reports

``coverage report``
```
Name                 Stmts   Miss Branch BrPart  Cover
------------------------------------------------------
app.py                  14      1      4      2    83%
virtual_machine.py     114     29     24      3    74%
------------------------------------------------------
TOTAL                  128     30     28      5    75%
```