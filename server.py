import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 8000

server.bind((host, port))
server.listen(5)
print(f"El servidor se está ejecutando en el puerto: {port}")

clientes = []
nombres = []

# Diccionario de respuestas predeterminadas
respuestas = {
    "hola": "¡Hola! ¿En qué puedo ayudarte?\nOpciones:\n1. Información sobre el servidor.\n2. Estado de la conexión.\n3. Salir.",
    "en qué puedo ayudarte": "¡Hola! ¿En qué puedo ayudarte?\nOpciones:\n1. Información sobre el servidor.\n2. Estado de la conexión.\n3. Salir.",
    "adiós": "¡Hasta luego! Que tengas un buen día.",
    "gracias": "De nada, siempre a tu servicio.",
    "cómo estás": "Soy solo un servidor, pero estoy funcionando perfectamente. ¿Y tú?",
    "1": "Este es un servidor de chat que te permite comunicarte con otros usuarios conectados.",
    "2": "La conexión está activa y funcionando correctamente.",
    "3": "Si deseas salir, simplemente cierra la aplicación. ¡Hasta luego!"
}

def enviarMensaje(mensaje):
    for cliente in clientes:
        cliente.send(mensaje)

def manejar(cliente, nombre):
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8').lower()
            if mensaje:
                # Enviar el mensaje a todos los clientes
                enviarMensaje(f"{nombre}: {mensaje}".encode('utf-8'))

                # Buscar una respuesta predeterminada
                respuesta = None
                for clave, resp in respuestas.items():
                    if mensaje == clave:
                        respuesta = resp
                        break
                
                # Responder al cliente con la respuesta predeterminada si se encuentra
                if respuesta:
                    cliente.send(f"Servidor: {respuesta}".encode('utf-8'))
                else:
                    cliente.send("Servidor: No tengo una respuesta para eso, pero estoy aquí para escuchar.".encode('utf-8'))
        except:
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            nombre = nombres[index]
            nombres.remove(nombre)
            enviarMensaje(f"{nombre} se desconectó del servidor.".encode('utf-8'))
            break

def recibir():
    while True:
        cliente, address = server.accept()
        cliente.send("NOMBRE".encode('utf-8'))
        nombre = cliente.recv(1024).decode('utf-8')
        nombres.append(nombre)

        print(f"El usuario {nombre} se conectó al servidor! {address}")
        enviarMensaje(f"{nombre} entró al chat.".encode('utf-8'))
        clientes.append(cliente)    
        cliente.send("Conectado a un servidor".encode('utf-8'))

        thread = threading.Thread(target=manejar, args=(cliente, nombre))
        thread.start()

recibir()
