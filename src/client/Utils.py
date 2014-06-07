import psutil
from server.Server import Server


## Returns a list of partition mount points for a given computer
def get_drive_mountpoints():
    return [drive.mountpoint for drive in psutil.disk_partitions()]


def mock_server():
    mocked_server = Server()
    return mocked_server

