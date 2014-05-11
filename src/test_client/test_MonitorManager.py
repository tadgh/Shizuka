import unittest
import MonitorManager
import RamByteMonitor
import RamPercentMonitor
import logging

##TODO figure out proper logging practice.
logging.basicConfig(level=logging.INFO)


class TestMonitorManager(unittest.TestCase):

    def setUp(self):
        self.manager = MonitorManager.MonitorManager()

    def test_adding_monitor_to_manager(self):
        monitor_1 = RamByteMonitor.RamByteMonitor(1)
        self.manager.add_monitor(monitor_1)
        self.assertTrue(1 in self.manager.monitor_list.keys(), "uh oh, guess its not in the keys,.")

    def test_monitor_properly_deleted_through_ID_deletion(self):
        monitor_1 = RamPercentMonitor.RAMPercentMonitor(1)
        self.manager.add_monitor(monitor_1)
        self.manager.remove_monitor_by_id(1)
        self.assertFalse(1 in self.manager.monitor_list.keys(), "Monitor not Properly Deleted, found ID in the keys.")

    def test_monitor_properly_deleted_through_object_deletion(self):
        monitor_1 = RamPercentMonitor.RAMPercentMonitor(1)
        self.manager.add_monitor(monitor_1)
        self.manager.remove_monitor(monitor_1)
        self.assertFalse(1 in self.manager.monitor_list.keys(), "Not Properly Deleted, found ID in the keys.")

    def test_empty_list_raises_error(self):
        self.assertRaises(KeyError, self.manager.remove_monitor_by_id(1))

    def test_poll_all_monitors_size_is_correct(self):
        mon1 = RamByteMonitor.RamByteMonitor(1)
        mon2 = RamPercentMonitor.RAMPercentMonitor(2)
        self.manager.add_monitor(mon1)
        self.manager.add_monitor(mon2)
        results = self.manager.poll_all()
        self.assertEquals(len(results), 2)

    def test_individual_poll_returns(self):
        mon1 = RamByteMonitor.RamByteMonitor(100)
        self.manager.add_monitor(mon1)
        results = self.manager.poll_monitor_by_id(100)
        self.assertIsNotNone(results)

    def test_individual_poll_fails_when_monitor_does_not_exist(self):
        mon1 = RamByteMonitor.RamByteMonitor(100)
        self.manager.add_monitor(mon1)
        self.assertRaises(KeyError, self.manager.poll_monitor_by_id(101))




if __name__ == "__main__":
    unittest.main()

