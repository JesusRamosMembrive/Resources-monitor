import psutil
import time


import psutil
# print(psutil.Process().environ())


# print(f"{psutil.cpu_times(percpu=False)=}")
# print(f"{psutil.cpu_times(percpu=True)=}")
# print(f"{psutil.cpu_percent(percpu=True)=}")
# print(f"{psutil.cpu_count(logical=False)=}")
# print(f"{psutil.cpu_count(logical=True)=}")
# print(f"{psutil.cpu_stats()=}") # No parece interesante
# print(f"{psutil.cpu_freq(percpu=True)=}")
# print(f"{psutil.getloadavg()=}")
# print(f"{psutil.virtual_memory()=}")
# print(f"{psutil.swap_memory()=}")
# print(f"{psutil.disk_usage('/')=}")
# print(f"{psutil.disk_partitions(all=True)=}")
# print(f"{psutil.disk_io_counters(perdisk=True)=}")
# print(f"{psutil.net_io_counters(pernic=True)=}")
# print(f"{psutil.net_connections(kind='inet')=}")
# print(f"{psutil.net_if_addrs()=}")
# print(f"{psutil.net_if_stats()=}")
# print(f"{psutil.boot_time()=}")
# print(f"{psutil.pids()=}")
# print(f"{psutil.pid_exists(1)=}")
# print(f"{psutil.process_iter()=}")
# print(f"{psutil.virtual_memory()=}")
# disk = psutil.disk_usage('/')
# print(type(disk))
# print(f"Total: {disk.total / (1024**3):.2f} GB")
# print(f"Usado: {disk.used / (1024**3):.2f} GB")
# print(f"Libre: {disk.free / (1024**3):.2f} GB")
# print(f"Porcentaje de uso: {disk.percent}%")

# while True:
#     cpu_percent = psutil.cpu_percent(interval=1)
#     print(f"Uso de CPU: {cpu_percent}%")
#     # Puedes ajustar el intervalo o incluir otros datos según necesites
#     mem = psutil.virtual_memory()
#     print(f"Memoria total: {mem.total / (1024 ** 3):.2f} GB")
#     print(f"Memoria disponible: {mem.available / (1024 ** 3):.2f} GB")
#     print(f"Uso de memoria: {mem.percent}%")
#     disk = psutil.disk_usage('/')
#     print(f"Total: {disk.total / (1024**3):.2f} GB")
#     print(f"Usado: {disk.used / (1024**3):.2f} GB")
#     print(f"Libre: {disk.free / (1024**3):.2f} GB")
#     print(f"Porcentaje de uso: {disk.percent}%")
#
#     net = psutil.net_io_counters()
#     print(f"Bytes enviados: {net.bytes_sent}")
#     print(f"Bytes recibidos: {net.bytes_recv}")
#
#     # for proc in psutil.process_iter(['pid', 'name', 'username']):
#     #     try:
#     #         info = proc.info
#     #         print(info)
#     #     except (psutil.NoSuchProcess, psutil.AccessDenied):
#     #         pass  # Algunos procesos pueden haber terminado o no tener permisos suficientes
#
#     time.sleep(1)  # Ajusta el intervalo según tus necesidades