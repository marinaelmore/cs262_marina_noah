import unittest
from unittest.mock import patch
from grpc_chatbot.grpc_client import ChatbotClient, get_alphanumeric_input

class TestChatbotClient(unittest.TestCase):

    @patch('builtins.input', side_effect=['abc123'])
    def test_get_alphanumeric_input_valid_input(self, mock_input):
        result = get_alphanumeric_input('Enter an alphanumeric string: ')
        self.assertEqual(result, 'abc123')

    @patch('grpc_chatbot.grpc_client.ChatbotClient.run_client_attempt')
    @patch('grpc_chatbot.grpc_client.ChatbotClient.run_client')
    def test_run_client(self, mock_run_client_attempt, mock_run_client):
        # Instantiate the client
        chatbot_client = ChatbotClient()

        # Run the client
        chatbot_client.run_client_attempt()
        chatbot_client.run_client()

        # Assert that the run_client_attempt method was called
        mock_run_client_attempt.assert_called()
        mock_run_client.assert_called()


if __name__ == '__main__':
    unittest.main()