import zmq
from time import sleep
from constants import Topics


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:6000")
#Se define el valor inicial de un contador
c = 1
while True:
    socket.send(Topics.disk_usage.value.encode())
    sleep(1)
    msg_in = socket.recv()
    print(f"Mensaje recibido: {msg_in}")
    c += 1
    if c == 15:
        break
    else:
        continue