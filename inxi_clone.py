
import os
import platform
import psutil
import socket

def get_system_info():
    info = {}

    # System
    info['system'] = {
        'os': platform.system(),
        'os_version': platform.version(),
        'hostname': socket.gethostname(),
        'kernel': platform.release(),
    }

    # CPU
    info['cpu'] = {
        'model': platform.processor(),
        'cores': psutil.cpu_count(logical=False),
        'threads': psutil.cpu_count(logical=True),
        'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A',
    }

    # Memory
    mem = psutil.virtual_memory()
    info['memory'] = {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'percent': mem.percent,
    }

    # Disk
    info['disk'] = []
    for part in psutil.disk_partitions():
        usage = psutil.disk_usage(part.mountpoint)
        info['disk'].append({
            'device': part.device,
            'mountpoint': part.mountpoint,
            'fstype': part.fstype,
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent,
        })

    # Network
    info['network'] = []
    net_io = psutil.net_io_counters(pernic=True)
    for iface, addrs in psutil.net_if_addrs().items():
        info['network'].append({
            'interface': iface,
            'addresses': [addr.address for addr in addrs if addr.family == socket.AF_INET],
            'bytes_sent': net_io[iface].bytes_sent if iface in net_io else 'N/A',
            'bytes_recv': net_io[iface].bytes_recv if iface in net_io else 'N/A',
        })

    return info

def print_system_info(info):
    # System
    print(f"System: {info['system']['os']} {info['system']['os_version']}")
    print(f"Hostname: {info['system']['hostname']}")
    print(f"Kernel: {info['system']['kernel']}")

    # CPU
    print("\nCPU:")
    print(f"  Model: {info['cpu']['model']}")
    print(f"  Cores: {info['cpu']['cores']}")
    print(f"  Threads: {info['cpu']['threads']}")
    print(f"  Frequency: {info['cpu']['frequency']} MHz")

    # Memory
    print("\nMemory:")
    print(f"  Total: {info['memory']['total'] // (1024 ** 2)} MB")
    print(f"  Available: {info['memory']['available'] // (1024 ** 2)} MB")
    print(f"  Used: {info['memory']['used'] // (1024 ** 2)} MB ({info['memory']['percent']}%)")

    # Disk
    print("\nDisk:")
    for disk in info['disk']:
        print(f"  Device: {disk['device']}")
        print(f"    Mountpoint: {disk['mountpoint']}")
        print(f"    Filesystem: {disk['fstype']}")
        print(f"    Total: {disk['total'] // (1024 ** 3)} GB")
        print(f"    Used: {disk['used'] // (1024 ** 3)} GB ({disk['percent']}%)")
        print(f"    Free: {disk['free'] // (1024 ** 3)} GB")

    # Network
    print("\nNetwork:")
    for net in info['network']:
        print(f"  Interface: {net['interface']}")
        print(f"    Addresses: {', '.join(net['addresses'])}")
        print(f"    Bytes Sent: {net['bytes_sent']}")
        print(f"    Bytes Received: {net['bytes_recv']}")

if __name__ == '__main__':
    info = get_system_info()
    print_system_info(info)
