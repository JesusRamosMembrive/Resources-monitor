import logging

def apply_logger_config() -> logging.Logger:
    logging.basicConfig(
        filename="ResourcesMonitor.log",
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.DEBUG
    )
    return logging.getLogger(__name__)
