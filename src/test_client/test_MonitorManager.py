import unittest
import MonitorManager
import RamByteMonitor
import Constants
import logging


#TODO figure out proper logging practice.
logging.basicConfig(level=logging.INFO)


class TestMonitorManager(unittest.TestCase):

    def setUp(self):
        self.manager = MonitorManager.MonitorManager()

    def test_adding_monitor_to_manager(self):
        monitor_1 = RamByteMonitor.RamByteMonitor()
        self.manager.add_monitor(monitor_1)
        self.assertTrue(Constants.RAM_BYTE_MONITOR in self.manager.monitor_list.keys(), "uh oh, guess its not in the keys,.")

    def test_monitor_properly_deleted_through_object_deletion(self):
        monitor_1 = RamByteMonitor.RamByteMonitor()
        self.manager.add_monitor(monitor_1)
        self.manager.remove_monitor(monitor_1)
        self.assertFalse(Constants.RAM_BYTE_MONITOR in self.manager.monitor_list.keys(), "Not Properly Deleted, found ID in the keys.")

    def test_empty_list_raises_error(self):
        self.assertRaises(KeyError, self.manager.remove_monitor_by_id(1))


if __name__ == "__main__":
    unittest.main()

