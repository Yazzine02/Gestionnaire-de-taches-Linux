import psutil

""" Get processes """
def get_processes():
    """ Function to get processes with details"""
    processes=[]
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue 
    return processes
    
""" System metrics """

""" CPU USAGE """
def get_cpu_usage(interval = 1):
    return psutil.cpu_percent(interval)

""" MEMORY USAGE """
def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        'total': memory.total,
        'used': memory.used,
        'free': memory.available,
        'cached': memory.cached,
        'percent': memory.percent
    }

""" DISK USAGE """
def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free,
        'percent': disk_usage.percent
    }
    
""" NETWORK USAGE """
def get_network_usage():
    network_usage = psutil.net_io_counters()
    return {
        'bytes sent': network_usage.bytes_sent,
        'bytes received': network_usage.bytes_recv,
        'packets sent': network_usage.packets_sent,
        'packets received': network_usage.packets_recv,  # Fixed typo
        'errors while receiving': network_usage.errin,
        'errors while sending': network_usage.errout
    }
    
""" Kill process """
def kill_process(pid, force = False):
    try:
        process = psutil.Process(pid)
        if force:
            process.kill()
        else:
            process.terminate()
        return True, ""
    except psutil.NoSuchProcess:
        return False, "No such process exists."
    except psutil.AccessDenied:
        return False, "Permission denied to terminate the process."
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
