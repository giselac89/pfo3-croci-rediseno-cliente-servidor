import socket
import threading

HOST = "localhost"
PORT = 5000

def enviar_tarea(numero):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(str(numero).encode())
    resultado = s.recv(1024).decode()        
    print(f"Tarea {numero} -> {resultado}")
    s.close()

if __name__ == "__main__":
    entrada = input("Para calcular el cuadrado de los números, ingresalos separados por espacio: ")
    numeros = entrada.split()                

    hilos = []
    for n in numeros:
        t = threading.Thread(target=enviar_tarea, args=(n,))
        t.start()                            
        hilos.append(t)

    for t in hilos:
        t.join()                             

    print("Todas las tareas fueron completadas")