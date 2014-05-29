import psutil

## Returns a list of partition mount points for a given computer
def get_drive_mountpoints():
    return [drive.mountpoint for drive in psutil.disk_partitions()]
