import unittest
import sys
import os
from unittest.mock import Mock
import asyncio
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))  # add parent directory to path
import virtual_machine as vm  # nopep8

machine_1 = {
    "name": "machine 1",
    "output_path": "output.txt",
    "host": "localhost",
    "port": 9000
}
machine_2 = {
    "name": "machine 2",
    "output_path": "output2.txt",
    "host": "localhost",
    "port": 9001
}
machine_3 = {
    "name": "machine 3",
    "output_path": "output3.txt",
    "host": "localhost",
    "port": 9002
}


class TestVirtualMachineTest:
    @classmethod
    def setup_class(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.vm = vm.VirtualMachine(
            "machine_1", machine_1, machine_2, machine_3)

    @classmethod
    def teardown_class(self):
        self.loop.close()

    def test_init(self):
        assert self.vm.my_machine == machine_1
        assert self.vm.machine_2 == machine_2
        assert self.vm.machine_3 == machine_3
        assert (self.vm.logical_clock == 0)
        assert (self.vm.queue.qsize() == 0)
        assert self.vm.clock_rate > .15 and self.vm.clock_rate <= 1
        # check that self.ouput_file is created
        assert (os.path.exists('output.txt'))

    @pytest.mark.asyncio
    async def test_queue_protocol(self):
        reader = Mock(spec=asyncio.StreamReader)
        writer = Mock(spec=asyncio.StreamWriter)

        reader.readline.side_effect = [b'4\n', b'']
        await self.vm.queue_protocol(reader, writer)
        assert (self.vm.queue.qsize() == 1)
        assert (self.vm.queue.get_nowait() == 4)
        writer.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_server(self, mocker):
        server_mock = Mock(spec=asyncio.AbstractServer)
        server_mock.serve_forever.return_value = None

        mock_start_server = mocker.patch(
            'asyncio.start_server', return_value=server_mock)
        await self.vm.start_vm_server()

        # assert start_server is called with correct args
        mock_start_server.assert_called_once_with(
            self.vm.queue_protocol, self.vm.my_machine["host"], self.vm.my_machine["port"])

        server_mock.serve_forever.assert_called_once()

    @pytest.mark.asyncio
    async def test_connect_to_other_machines(self, mocker):
        reader_mock = Mock(spec=asyncio.StreamReader)
        stream_mock = Mock(spec=asyncio.StreamWriter)

        mock_open_connection = mocker.patch(
            'asyncio.open_connection', return_value=(reader_mock, stream_mock))
        await self.vm.connect_to_other_machines()

        # assert open_connection is called with correct args
        mock_open_connection.assert_has_calls([
            mocker.call(self.vm.machine_2["host"], self.vm.machine_2["port"]),
            mocker.call(self.vm.machine_2["host"], self.vm.machine_3["port"])
        ])

        assert self.vm.machine_2["reader"] == reader_mock
        assert self.vm.machine_2["stream"] == stream_mock
        assert self.vm.machine_3["reader"] == reader_mock
        assert self.vm.machine_3["stream"] == stream_mock

    @pytest.mark.asyncio
    async def test_send_clock_time(self, mocker):
        stream_mock = Mock(spec=asyncio.StreamWriter)
        mock_write = mocker.patch.object(stream_mock, 'write')
        self.vm.logical_clock = 627
        await self.vm.send_clock_time(stream_mock)
        mock_write.assert_called_once_with(b'627\n')

    @pytest.mark.asyncio
    async def test_tick_queue_empty(self, mocker):
        stream_mock_2 = Mock(spec=asyncio.StreamWriter)
        stream_mock_3 = Mock(spec=asyncio.StreamWriter)
        self.vm.machine_2["stream"] = stream_mock_2
        self.vm.machine_3["stream"] = stream_mock_3
        self.vm.logical_clock = 0
        mock_send_clock_time = mocker.patch.object(self.vm, "send_clock_time")
        mock_file_write = mocker.patch.object(self.vm.output_file, "write")

        await self.vm.tick_queue_empty(1)
        mock_send_clock_time.assert_called_once_with(stream_mock_2)
        assert self.vm.logical_clock == 1

        await self.vm.tick_queue_empty(2)
        # assert called multiple times
        assert mock_send_clock_time.call_args_list[1] == mocker.call(
            stream_mock_3)
        assert self.vm.logical_clock == 2

        await self.vm.tick_queue_empty(3)
        assert self.vm.logical_clock == 3
        assert mock_send_clock_time.call_args_list[2] == mocker.call(
            stream_mock_2)
        assert mock_send_clock_time.call_args_list[3] == mocker.call(
            stream_mock_3)
        assert mock_send_clock_time.call_count == 4

        # make sure internal ievent only and call count not called
        await self.vm.tick_queue_empty(4)
        assert self.vm.logical_clock == 4
        assert mock_send_clock_time.call_count == 4
        assert mock_file_write.call_args_list[3] == mocker.call(
            "internal, time 3\n")

        assert mock_file_write.call_count == 4

    @pytest.mark.asyncio
    async def test_tick_queue_has_item(self, mocker):
        self.vm.logical_clock = 0
        self.vm.queue.put_nowait(5)
        # picks greater of 2 times and increments by one
        mock_file_write = mocker.patch.object(self.vm.output_file, "write")
        self.vm.tick_queue_has_item()
        assert self.vm.logical_clock == 6
        assert mock_file_write.call_count == 1

        self.vm.logical_clock = 10
        self.vm.queue.put_nowait(8)
        self.vm.tick_queue_has_item()
        assert self.vm.logical_clock == 11
        assert mock_file_write.call_count == 2


def test_main(mocker):
    # assert that whichever id is passed as the vm's identify, machine_2 and 3 are set accordingly

    mocker_loop = mocker.patch.object(asyncio, "get_event_loop")
    mocker_loop.create_task.side_effect = None
    mocker_loop.run_forever.side_effect = None
    json_data = open('config.json').read()
    config = json.loads(json_data)

    vm_mock = mocker.patch.object(
        vm.VirtualMachine, "__init__", return_value=None)

    vm.run_virtual_machine("machine_2")
    vm_mock.assert_called_once_with(
        "machine_2", config["machine_2"], config["machine_1"], config["machine_3"])

    os.remove("output.txt")


if __name__ == '__main__':
    pytest.main()
