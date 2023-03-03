import unittest
import sys
import os
from unittest.mock import Mock
import asyncio
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))  # add parent directory to path
from virtual_machine import VirtualMachine  # nopep8


class TestVirtualMachineTest:
    @classmethod
    def setup_class(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.vm = VirtualMachine(
            'machine_1', 'output.txt', 'localhost', '9000', '9001', '9002')

    @classmethod
    def teardown_class(self):
        self.loop.close()

    def test_init(self):
        assert (self.vm.machine_id == 'machine_1')
        assert (self.vm.host == 'localhost')
        assert (self.vm.my_port == '9000')
        assert (self.vm.machine_2_port == '9001')
        assert (self.vm.machine_3_port == '9002')
        assert (self.vm.logical_clock == 0)
        assert (self.vm.queue.qsize() == 0)
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
        server_mock = Mock(spec=asyncio.Server)
        server_mock.serve_forever.return_value = None

        mock_start_server = mocker.patch(
            'asyncio.start_server', return_value=server_mock)
        await self.vm.start_vm_server()

        # assert start_server is called with correct args
        mock_start_server.assert_called_once_with(
            self.vm.queue_protocol, self.vm.host, self.vm.my_port)

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
            mocker.call(self.vm.host, self.vm.machine_2_port),
            mocker.call(self.vm.host, self.vm.machine_3_port)
        ])

        assert self.vm.reader2 == reader_mock
        assert self.vm.stream2 == stream_mock
        assert self.vm.reader3 == reader_mock
        assert self.vm.stream3 == stream_mock


if __name__ == '__main__':
    pytest.main()
