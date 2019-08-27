import io
import unittest
from unittest.mock import MagicMock
from plugins.slack_reader import UsersAveragePlugin


class TestUsersAveragePlugin(unittest.TestCase):
    def setUp(self) -> None:
        self.plugin = UsersAveragePlugin()
        self.data = {"type": "message", "user": "xyz", "channel": "cnl"}

    def test_process_message_no_user(self):
        self.plugin.get_username_from_id = MagicMock(return_value=None)
        self.assertEqual(self.plugin.process_message(self.data), None)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_process_message_text_not_number(self, mock_stdout):
        self.data["text"] = 'foo'
        self.plugin.get_username_from_id = MagicMock(return_value='John')
        self.plugin.process_message(self.data)
        self.assertEqual(mock_stdout.getvalue(), "User input is not a number\n")

    @unittest.mock.patch("plugins.slack_reader.requests.put")
    def test_process_message_text_is_number(self, mock_response):
        mock_response.return_value = MagicMock()
        mock_response.return_value.json = MagicMock(
            return_value={"average": "2", "count": 1}
        )
        self.data["text"] = " 2 "
        self.plugin.get_username_from_id = MagicMock(return_value='John')
        self.plugin.process_message(self.data)
        self.assertEqual(
            self.plugin.outputs[0], ['cnl', 'User John average is 2'])
