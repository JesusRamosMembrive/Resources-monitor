from dataclasses import dataclass, field
import psutil
from testZeroMQ.ClientZeroMQ import ResourceMonitor
from MeasureComponents.interface_measure_classes import iMeasure
from constants import Topics
from collections import namedtuple
import threading

from Logger.logger_config import apply_logger_config
logger = apply_logger_config()

@dataclass
class MemoryMeasure(iMeasure):
    monitor: ResourceMonitor
    memory_obj: namedtuple = field(default_factory=list)
    stop_event: threading.Event = field(default_factory=threading.Event)


    def collect_data(self):
        while not self.stop_event.is_set():
            self.memory_obj = psutil.virtual_memory()
            data = {"total": self.memory_obj.total,
                    "available": self.memory_obj.available,
                    "percent": self.memory_obj.percent,
                    "used": self.memory_obj.used,
                    "free": self.memory_obj.free}
            logger.info(f"Data memory measure: {data}")
            event = {Topics.memory_usage.value: data}
            self.monitor.enqueue_event(event)
            event = {Topics.cpu_usage.value: data}
            self.monitor.enqueue_event(event)
            self.stop_event.wait(1)


# if __name__ == "__main__":
#     import time
#     monitor = ResourceMonitor(port=5555, poll_interval=0.1)
#     monitor.start()
#     cpu_measure = MemoryMeasure(monitor)
#     try:
#         while True:
#             cpu_measure.collect_data()
#             time.sleep(1)
#     except KeyboardInterrupt:
#         monitor.stop()
#         print("Monitor detenido.")

