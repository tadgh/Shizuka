import psutil

def get_drive_mountpoints():
    return [drive.mountpoint for drive in psutil.disk_partitions()]


if __name__ == "__main__":
    print(get_drive_mountpoints())