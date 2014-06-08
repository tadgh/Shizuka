import MessageHandler
import MonitorManager

import unittest
import MonitorManager
import RamByteMonitor
import Constants
import logging
import ClientErrors

#TODO figure out proper logging practice.
logging.basicConfig(level=logging.INFO)


class TestMessageHandler(unittest.TestCase):

    def setUp(self):
        self.handler = MessageHandler.MessageHandler("shizuka.client.Mulder")
        #have to manually wipe monitors in between tests because this singleton stubbornly holds onto data.

    def test_message_queue_starts_empty(self):
        self.assertTrue(self.handler._message_queue.empty())

    def messages_add_to_queue_correctly(self):
        self.handler.queue_message({"test": "data"})
        self.assertTrue(len(self.handler._message_queue) == 1)

    def test_adding_message_from_another_module(self):
        monman = MonitorManager.MonitorManager()
        monman.set_message_handler(self.handler)
        monman.send_message_to_server({"test": "data"})
        #self.assertListEqual(self.handler._message_queue, [{"test": "data"}])

    def test_sending_to_server_fails_when_not_associated(self):
        self.handler.set_server(None, None)
        self.assertRaises(ClientErrors.ServerNotFoundError, self.handler.post_to_server, "test")






if __name__ == "__main__":
    unittest.main()

