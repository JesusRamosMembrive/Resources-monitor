import psutil
from constants import Topics
from Logger.logger_config import apply_logger_config
logger = apply_logger_config()

class DiskMeasure:
    @staticmethod
    def collect_data() -> dict:
        disk_status = psutil.disk_usage('/')

        disk_status_formatted = {
            "total": round(disk_status.total / (1024 ** 3), 2),
            "used": round(disk_status.used / (1024 ** 3), 2),
            "free": round(disk_status.free / (1024 ** 3), 2),
            "percent": disk_status.percent,
        }

        data = {"disk_capacity": disk_status_formatted}
        logger.info(f"Data disk measure: {data}")
        event = {Topics.disk_usage.value: data}
        return event
