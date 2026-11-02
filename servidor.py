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

        try:
            num_tarea, valor = tarea.split(":")        # separa "1:5" en num_tarea="1", valor="5"
            numero = int(valor)
            print(f"[{nombre}] procesando Tarea {num_tarea}: {numero}^2")
            time.sleep(2)                              # simula trabajo pesado
            resultado = numero * numero
            respuesta = f"Tarea {num_tarea}: {numero}^2 = {resultado} (procesado por {nombre})"
            print(f"[{nombre}] terminó Tarea {num_tarea}: {numero}^2 = {resultado}")
        except ValueError:
            respuesta = "Error: enviá un número válido"
            print(f"[{nombre}] tarea inválida: {tarea}")

        conexion.send(respuesta.encode())              
        conexion.close()                               
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
                print(f"[Servidor] {tarea} encolada")
        except KeyboardInterrupt:
            print("Servidor detenido.")


if __name__ == "__main__":
    main()