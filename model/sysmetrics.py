import psutil
import datetime
class sysmetrics:
  

    def __init__(self, cpu_percent=None, cpu_count_logical=None, cpu_count_physical=None, mem_percent=None, mem_total=None, mem_available=None, mem_used=None, mem_free=None, sys_boot_time=None):
        self.cpu_percent = cpu_percent
        self.cpu_count_logical = cpu_count_logical
        self.cpu_count_physical = cpu_count_physical
        self.mem_percent = mem_percent
        self.mem_total = mem_total
        self.mem_available = mem_available
        self.mem_used = mem_used
        self.mem_free = mem_free
        self.sys_boot_time = sys_boot_time

    @staticmethod
    def get_sysmetrics():
        s=None
        try:
            s = sysmetrics(psutil.cpu_percent(), psutil.cpu_count(logical=True), psutil.cpu_count(),psutil.virtual_memory()[2], psutil.virtual_memory()[0], psutil.virtual_memory()[1], psutil.virtual_memory()[3], psutil.virtual_memory()[4], datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%dT%H:%M:%S"))
        except:
            pass
        return s