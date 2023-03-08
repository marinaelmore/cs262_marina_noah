import pytest
from mock import patch
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))  # add parent directory to path
import app

class TestApp(unittest.TestCase):

    @patch('app.run_virtual_machine')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.open', create=True)
    def test_main(self, mock_open, mock_parse_args, mock_run_vm):
        # Set up mock objects
        mock_open.return_value.__enter__.return_value.read.return_value = '{"machine_2": {"ip_address": "127.0.0.1", "port": "8080"}}'
        mock_parse_args.return_value.machine_id = 'machine_2'
        mock_config = {'machine_2': {'ip_address': '127.0.0.1', 'port': '8080'}}

        with patch('json.loads', return_value=mock_config):
            # Call the function
            app.main()

        # Assert that the function does what it's supposed to do
        mock_run_vm.assert_called_once_with('machine_2')

