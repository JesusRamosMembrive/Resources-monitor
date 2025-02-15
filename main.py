import threading
from testZeroMQ.ClientZeroMQ import ResourceMonitor
from MeasureComponents.cpu_measure import CPUMeasure
from MeasureComponents.memory_measure import MemoryMeasure

from Logger.logger_config import apply_logger_config
logger = apply_logger_config()

if __name__ == "__main__":
    monitor = ResourceMonitor(port=5555, poll_interval=0.1)
    monitor.start()

    cpu_measure = CPUMeasure(monitor)
    memory_measure = MemoryMeasure(monitor)

    cpu_thread = threading.Thread(target=cpu_measure.collect_data)
    memory_thread = threading.Thread(target=memory_measure.collect_data)
    cpu_thread.start()
    memory_thread.start()

    # El hilo principal espera a que el usuario presione "q"
    while True:
        key = input("Presione 'q' para salir: ").strip().lower()
        if key == "q":
            break

    # Se activa la señal de parada en cada uno de los módulos
    cpu_measure.stop_event.set()
    memory_measure.stop_event.set()

    # Se detiene el monitor y se espera a que los hilos terminen
    monitor.stop()
    cpu_thread.join()
    memory_thread.join()

    logger.info("Programa finalizado de forma controlada.")
