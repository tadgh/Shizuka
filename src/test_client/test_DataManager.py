import unittest
import MonitorManager
import DataManager
import RamByteMonitor
import RamPercentMonitor
import logging

#TODO figure out proper logging practice.
logging.basicConfig(level=logging.INFO)

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.monitor_manager = MonitorManager.MonitorManager()
        self.data_manager = DataManager.DataManager()

    def test_poll_all_monitors_size_is_correct(self):
        mon1 = RamByteMonitor.RamByteMonitor(1)
        mon2 = RamPercentMonitor.RAMPercentMonitor(2)
        self.monitor_manager.add_monitor(mon1)
        self.monitor_manager.add_monitor(mon2)
        results = self.data_manager.poll_all()
        self.assertEquals(len(results), 2)
        self.monitor_manager.remove_monitor(mon1)
        self.monitor_manager.remove_monitor(mon2)

    def test_individual_poll_returns(self):
        mon1 = RamByteMonitor.RamByteMonitor(100)
        self.monitor_manager.add_monitor(mon1)
        results = self.data_manager.poll_monitor_by_id(100)
        self.assertIsNotNone(results)
        self.monitor_manager.remove_monitor(mon1)

    def test_individual_poll_fails_when_monitor_does_not_exist(self):
        mon1 = RamByteMonitor.RamByteMonitor(100)
        self.monitor_manager.add_monitor(mon1)
        self.assertRaises(KeyError, self.data_manager.poll_monitor_by_id(101))
        self.monitor_manager.remove_monitor(mon1)

if __name__ == "__main__":
    unittest.main()

