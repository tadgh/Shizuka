import psutil
import socket
import platform
from uuid import getnode
from server.Server import Server


## Returns a list of partition mount points for a given computer
def get_drive_mountpoints():
    return [drive.mountpoint for drive in psutil.disk_partitions()]


def mock_server():
    mocked_server = Server()
    return mocked_server


## Builds the discovery message. Includes: FQDN/IP/MAC/Mountpoints/# of CPUs/Amount of ram(Bytes)/System Platform
# @return the dict containing discovery data.
def discover():
    discovery_data = {}
    discovery_data["FQDN"] = socket.getfqdn()
    discovery_data["IP"] = socket.gethostbyname(socket.getfqdn())
    discovery_data["MAC"] = getnode()
    discovery_data["MOUNT_POINTS"] = get_drive_mountpoints()
    discovery_data["CPU_COUNT"] = psutil.cpu_count()
    discovery_data["RAM_COUNT"] = psutil.virtual_memory().total
    discovery_data["PLATFORM"] = platform.system()
    return discovery_data

