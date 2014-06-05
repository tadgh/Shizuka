import unittest
import MonitorManager
import RamByteMonitor
import Constants
import logging
import Utils

#TODO figure out proper logging practice.
logging.basicConfig(level=logging.INFO)


class TestMonitorManager(unittest.TestCase):

    def setUp(self):
        self.manager = MonitorManager.MonitorManager()
        #have to manually wipe monitors in between tests because this singleton stubbornly holds onto data.
        self.manager.clear_monitors()

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
        self.assertRaises(KeyError, self.manager.remove_monitor_by_type(Constants.RAM_BYTE_MONITOR))

    def test_remove_monitor_by_type(self):
        self.manager.add_monitor(RamByteMonitor.RamByteMonitor())
        self.manager.remove_monitor_by_type(Constants.RAM_BYTE_MONITOR)
        print(self.manager.list_monitors())
        self.assertTrue(len(self.manager.list_monitors()) == 0)

    def test_monitor_factory_generates_correct_monitor(self):
        mon1 = self.manager.create_monitor(Constants.RAM_BYTE_MONITOR)
        self.assertIsInstance(mon1, RamByteMonitor.RamByteMonitor)

    def test_monitor_factory_fails_on_unknown_type(self):
        self.assertRaises(ValueError, self.manager.create_monitor, "Some Garbage Type")

    def test_monitor_factory_fails_on_bad_option_parse(self):
        mon1 = self.manager.create_monitor(Constants.STORAGE_BYTE_MONITOR + "ASDAS")#a garbage mount point.
        self.assertIsNone(mon1)

    def test_handle_config_successful_call(self):
        mp = Utils.get_drive_mountpoints()[0]
        cpu_mon = self.manager.create_monitor(Constants.CPU_PERCENT_MONITOR)
        self.manager.add_monitor(cpu_mon)

        config_dict = {
            "add": [
                Constants.RAM_BYTE_MONITOR,
                Constants.BYTES_RECEIVED_MONITOR,
                Constants.STORAGE_BYTE_MONITOR + mp
            ],
            "remove": [
                Constants.CPU_PERCENT_MONITOR
            ]
        }

        self.manager.handle_config(config_dict)
        self.assertTrue(len(self.manager.list_monitors()) == 3
                        and Constants.CPU_PERCENT_MONITOR not in self.manager.list_monitors().keys())



if __name__ == "__main__":
    unittest.main()

