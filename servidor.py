import socket
import threading
import queue
import time

HOST = "localhost"
PORT = 5000
CANTIDAD_WORKERS = 3

cola = queue.Queue()

# --- Worker: saca tareas de la cola y las procesa ---
def worker(nombre):
    while True:
        datos = cola.get()
        print(f"[{nombre}] procesando tarea: {datos}")
        time.sleep(2)
        print(f"[{nombre}] terminó tarea: {datos}")
        cola.task_done()

# --- Prueba : creamos el pool y enviar tareas a mano ---
if __name__ == "__main__":
    for i in range(CANTIDAD_WORKERS):
        threading.Thread(target=worker, args=(f"Worker {i+1}",), daemon=True).start()
    print(f"Pool de {CANTIDAD_WORKERS} workers listo.")

    for n in range(1, 8):
        cola.put(n)

    cola.join()
    print("Todas las tareas completadas")