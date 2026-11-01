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
        conexion, direccion, tarea = cola.get()
        print(f"[{nombre}] procesando tarea: {tarea}")
        time.sleep(2)                                  

        try:
            numero = int(tarea)
            resultado = numero * numero                
            respuesta = f"Resultado: {resultado} (procesado por {nombre})"
        except ValueError:
            respuesta = "Error: enviá un número válido"

        conexion.send(respuesta.encode())              
        conexion.close()                               
        print(f"[{nombre}] terminó tarea: {tarea}")
        cola.task_done()


def main():
    # --- Creamos el pool de workers ---
    for i in range(CANTIDAD_WORKERS):
        threading.Thread(target=worker, args=(f"Worker {i+1}",), daemon=True).start()
    print(f"Pool de {CANTIDAD_WORKERS} workers listo.")

    # --- Creamos el socket del servidor ---
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1.0)   #  "despierta" el servidor cada 1 segundo
        print(f"Servidor escuchando en {HOST}:{PORT}")

        try:
            while True:
                try:
                    conexion, direccion = s.accept()
                except socket.timeout:
                    continue

                tarea = conexion.recv(1024).decode()
                cola.put((conexion, direccion, tarea))
                print(f"[Servidor] tarea de {direccion[1]} encolada: {tarea}")
        except KeyboardInterrupt:
            print("Servidor detenido.")


if __name__ == "__main__":
    main()