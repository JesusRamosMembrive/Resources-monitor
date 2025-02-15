import threading
from dataclasses import dataclass, field
import psutil
from testZeroMQ.ClientZeroMQ import ResourceMonitor
from MeasureComponents.interface_measure_classes import iMeasure
from constants import Topics
from Logger.logger_config import apply_logger_config
logger = apply_logger_config()

@dataclass
class CPUMeasure(iMeasure):
    monitor: ResourceMonitor
    usage_total:float = 0.0
    usage_per_core: list[float] = field(default_factory=list)
    stop_event: threading.Event = field(default_factory=threading.Event)

    def collect_data(self):
        while not self.stop_event.is_set():
            self.usage_per_core = psutil.cpu_percent(percpu=True)
            self.usage_total = psutil.cpu_percent(percpu=False)
            data = {"usage_total": self.usage_total, "usage_per_core": self.usage_per_core}
            logger.info(f"Data cpu measure: {data}")
            event = {Topics.cpu_usage.value: data}
            self.monitor.enqueue_event(event)
            self.stop_event.wait(1)

# if __name__ == "__main__":
#     import time
#     monitor = ResourceMonitor(port=5555, poll_interval=0.1)
#     monitor.start()
#     cpu_measure = CPUMeasure(monitor)
#     try:
#         while True:
#             cpu_measure.collect_data()
#             time.sleep(0.2)
#     except KeyboardInterrupt:
#         monitor.stop()
#         print("Monitor detenido.")




