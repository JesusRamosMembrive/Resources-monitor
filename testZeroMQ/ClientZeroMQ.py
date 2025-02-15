import zmq
import time
import json
import queue
import threading
import random
from constants import Topics

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ResourceMonitor(metaclass=Singleton):
    def __init__(self, port=5555, poll_interval=0.1):
        """
        Inicializa el monitor de recursos.

        Args:
            port (int): Puerto en el que se abrirá el socket ZeroMQ.
            poll_interval (float): Intervalo (en segundos) para revisar la cola de mensajes.
        """
        self.publisher_thread:[threading.Thread] = None
        self.port:int  = port
        self.poll_interval:float = poll_interval  # Tiempo entre comprobaciones de la cola
        self.context:[zmq.Context] = zmq.Context()
        self.socket:[zmq.Context] = self.context.socket(zmq.PUB)
        # self.socket.bind(f"tcp://*:{self.port}")
        self.socket.bind(f"tcp://*:{self.port}")
        # Definición de topics permitidos
        self.events:list = [Topics.cpu_usage.value,
                       Topics.memory_usage.value,
                       Topics.disk_usage.value,
                       Topics.network_usage.value]
        # Cola de mensajes (cada mensaje es un diccionario con {topic: datos})
        self.msg_queue:[queue] = queue.Queue()
        self.running:bool = False

    def enqueue_event(self, event: dict) -> None:
        """
        Permite a otros módulos encolar un evento.

        El evento debe ser un diccionario donde la clave es un topic permitido
        y el valor son los datos asociados.
        """
        print(f"Encolando evento: {event}")
        if not isinstance(event, dict):
            raise ValueError("El evento debe ser un diccionario.")
        for key, value in event.items():
            print(f"key: {key}")
            print(f"{value=}")
            if key not in self.events:
                raise ValueError(f"El topic '{key}' no está en la lista permitida: {self.events}")
        self.msg_queue.put(event)

    def gather_event(self) ->  dict | None:
        """
        Intenta obtener un evento de la cola sin bloquear.
        Retorna None si la cola está vacía.
        """
        try:
            event = self.msg_queue.get_nowait()
        except queue.Empty:
            return None
        return event

    def publish_events(self):
        """
        Bucle principal que publica los eventos contenidos en la cola.
        Si la cola está vacía, espera el intervalo especificado.
        """
        while self.running:
            event = self.gather_event()
            if event:
                for topic, data in event.items():
                    message = f"{topic} " + json.dumps({"data": data})
                    self.socket.send_string(message)
                    print(f"Publicado: {message}")
            else:
                time.sleep(self.poll_interval)

    def start(self) -> None:
        """
        Inicia el monitor y el hilo encargado de publicar los mensajes.
        """
        self.running = True
        print(f"Iniciando ResourceMonitor en el puerto {self.port}...")
        self.publisher_thread = threading.Thread(target=self.publish_events)
        self.publisher_thread.start()

    def stop(self) -> None:
        """
        Detiene el monitor y cierra los recursos (socket y contexto de ZeroMQ).
        """
        self.running = False
        self.publisher_thread.join()
        self.socket.close()
        self.context.term()
        print("ResourceMonitor detenido.")

# --- Simulación de módulos que generan eventos ---
#
# def simulate_module(topic, interval, data_func, monitor: ResourceMonitor):
#     """
#     Función que simula un módulo que, cada 'interval' segundos,
#     genera datos y encola un mensaje en el monitor.
#     """
#     while monitor.running:
#         data = data_func()
#         event = {topic: data}
#         monitor.enqueue_event(event)
#         time.sleep(interval)
#
# # Funciones simuladas para generar datos de ejemplo
# def cpu_data():
#     return {"usage": random.randint(0, 100)}
#
# def memory_data():
#     return {"usage": random.randint(0, 100)}
#
# def disk_data():
#     return {"read": random.randint(0, 1000), "write": random.randint(0, 1000)}
#
# def network_data():
#     return {"in": random.randint(0, 1000), "out": random.randint(0, 1000)}
#
# if __name__ == "__main__":
#     monitor = ResourceMonitor(port=5555, poll_interval=0.1)
#     monitor.start()
#
#     # Se inician hilos para simular cada módulo con frecuencias distintas
#     modules = [
#         threading.Thread(target=simulate_module, args=("cpu", 1.0, cpu_data, monitor)),
#         threading.Thread(target=simulate_module, args=("memory", 1.5, memory_data, monitor)),
#         threading.Thread(target=simulate_module, args=("disk", 2.0, disk_data, monitor)),
#         threading.Thread(target=simulate_module, args=("network", 2.5, network_data, monitor)),
#     ]
#     for t in modules:
#         t.start()
#
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         monitor.stop()
#         for t in modules:
#             t.join()
