import socket
import threading

host = 'localhost'
port = 8000

nombre = input("Ingrese su nombre: ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje == 'NOMBRE':
                cliente.send(nombre.encode('utf-8'))
            else:
                print(mensaje)
        except:
            print("Cerrando la conexión con el servidor...")
            cliente.close()
            break

def escribir():
    while True:
        try:
            mensaje = input("")
            cliente.send(mensaje.encode('utf-8'))
        except KeyboardInterrupt:
            cliente.close()
            break

receive_thread = threading.Thread(target=recibir)
receive_thread.start()
escribir()
