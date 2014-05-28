import unittest
import MonitorManager
import DataManager
import RamByteMonitor
import StorageByteMonitor
import logging

#TODO figure out proper logging practice.
logging.basicConfig(level=logging.INFO)

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.monitor_manager = MonitorManager.MonitorManager()
        self.data_manager = DataManager.DataManager()

    def test_poll_all_monitors_size_is_correct(self):
        mon1 = RamByteMonitor.RamByteMonitor()
        mon2 = StorageByteMonitor.StorageByteMonitor("C:\\")
        self.monitor_manager.add_monitor(mon1)
        self.monitor_manager.add_monitor(mon2)
        results = self.data_manager.poll_all()
        self.assertEquals(len(results), 2)
        self.monitor_manager.remove_monitor(mon1)
        self.monitor_manager.remove_monitor(mon2)

if __name__ == "__main__":
    unittest.main()

