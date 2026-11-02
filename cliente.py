import socket
import threading

HOST = "localhost"
PORT = 5000

def enviar_tarea(num_tarea, numero):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(f"{num_tarea}:{numero}".encode())
    resultado = s.recv(1024).decode()
    print(f"Tarea {num_tarea}: {numero}^2 = {resultado}")
    s.close()

if __name__ == "__main__":
    try:
        entrada = input("Para calcular el cuadrado de los números, ingresalos separados por espacio: ")
        numeros = entrada.split()                

        hilos = []
        for i, n in enumerate(numeros, start=1):
            t = threading.Thread(target=enviar_tarea, args=(i, n))
            t.start()                            
            hilos.append(t)

        for t in hilos:
            t.join()                             

        print("Todas las tareas fueron completadas")
    except KeyboardInterrupt:
        print("\nCliente detenido.")