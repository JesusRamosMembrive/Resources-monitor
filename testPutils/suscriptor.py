import zmq
from time import sleep
from constants import Topics


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt(zmq.SUBSCRIBE, Topics.memory_usage.value.encode())
#Se define el valor inicial de un contador
c = 1
while True:
    mensaje = socket.recv().decode('utf-8')
    print(f"Mensaje numero {c} recibido en el suscriptor: {mensaje}")
    sleep(1)
    c += 1
    if c == 15:
        break
    else:
        continue