import zmq
import queue
import threading
from constants import Topics
from Logger.logger_config import apply_logger_config
import json
import time
from MeasureComponents.disk_usage_measure import DiskMeasure

logger = apply_logger_config()

class ZeroMQManager:
    def __init__(self, port=5555, single_query_port=6000, poll_interval=0.1):
        """
        Inicializa el monitor de recursos.

        Args:
            port (int): Puerto para el socket de publicación (PUB).
            single_query_port (int): Puerto para el socket de consulta (REP).
            poll_interval (float): Intervalo (en segundos) para revisar la cola de mensajes.
        """
        self.publisher_thread: [threading.Thread] = None
        self.query_thread: [threading.Thread] = None
        self.port: int = port
        self.single_query_port: int = single_query_port
        self.poll_interval: float = poll_interval  # Tiempo entre comprobaciones de la cola
        self.context: zmq.Context = zmq.Context()

        # Socket de publicación para datos continuos
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"tcp://*:{self.port}")

        # Socket REP para consultas puntuales
        self.rep_socket = self.context.socket(zmq.REP)
        self.rep_socket.bind(f"tcp://*:{self.single_query_port}")

        # Definición de topics permitidos
        self.events: list = [
            Topics.cpu_usage.value,
            Topics.memory_usage.value,
            Topics.disk_usage.value,
            Topics.network_usage.value,
        ]
        # Cola de mensajes (cada mensaje es un diccionario con {topic: datos})
        self.msg_queue: queue.Queue = queue.Queue()
        self.running: bool = False
        logger.info("Monitor de recursos inicializado.")

    def enqueue_event(self, event: dict) -> None:
        """
        Permite a otros módulos encolar un evento.

        El evento debe ser un diccionario donde la clave es un topic permitido
        y el valor son los datos asociados.
        """
        logger.info(f"Encolando evento: {event}")
        if not isinstance(event, dict):
            raise ValueError("El evento debe ser un diccionario.")
        for key, value in event.items():
            logger.info(f"key: {key}")
            logger.info(f"{value=}")
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
        Método que publica los eventos en el socket de ZeroMQ.
        :return:
        """
        while self.running:
            try:
                event = self.msg_queue.get(timeout=self.poll_interval)
            except queue.Empty:
                continue
            self.pub_socket.send_string(self.format_event(event))

    def handle_queries(self):
        """
        Método que maneja las solicitudes de consulta de un cliente.
        :return:
        """
        while self.running:
            try:
                # Espera una solicitud de un cliente
                request = self.rep_socket.recv_string(flags=zmq.NOBLOCK)
            except zmq.Again:
                # No hay solicitud, espera un poco y continúa
                time.sleep(self.poll_interval)
                continue

            response_data = self.evalue_query(request)
            # Envía la respuesta
            self.rep_socket.send_json(response_data)

    def evalue_query(self, request: str) -> dict:
        """
        Evalúa una solicitud de consulta y devuelve una respuesta.
        :param request:
        :return:
        """
        logger.info(f"Solicitud recibida: {request}")
        match request:
            case Topics.disk_usage.value:
                response_data = DiskMeasure().collect_data()
            case _:
                response_data = {"error": "Solicitud desconocida"}
        return response_data

    def format_event(self, event: dict) -> str:
        """
        Formatea un evento para enviarlo por ZeroMQ.
        :param event:
        :return:
        """
        # Formatea el evento para enviarlo (agrega timestamp, topic, etc.)
        # Se asume que event es del tipo {topic: data}
        topic = list(event.keys())[0]
        data = event[topic]
        message = f"{topic} " + json.dumps({"data": data})
        return message

    def start(self) -> None:
        """
        Inicia el monitor y el hilo encargado de publicar los mensajes.
        """
        self.running = True
        self.publisher_thread = threading.Thread(target=self.publish_events)
        self.publisher_thread.start()
        self.query_thread = threading.Thread(target=self.handle_queries)
        self.query_thread.start()

    def stop(self) -> None:
        """
        Detiene el monitor y cierra los recursos (socket y contexto de ZeroMQ).
        """
        self.running = False
        if self.publisher_thread:
            self.publisher_thread.join()
        if self.query_thread:
            self.query_thread.join()
        self.pub_socket.close()
        self.rep_socket.close()
        self.context.term()




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
if __name__ == "__main__":
    monitor = ZeroMQManager(port=5555, poll_interval=0.1)
    monitor.start()
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
