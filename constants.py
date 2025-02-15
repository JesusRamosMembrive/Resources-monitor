from enum import Enum, auto


class Topics(Enum):
    cpu_usage = "cpu_usage"
    memory_usage = "memory_usage"
    disk_usage = "disk_usage"
    network_usage = "network_usage"
    general_info = "general_info"
