import socket
import threading #Usar varios hilos en un mismo programa, para que el servidor pueda atender varios pedidos


HEADER = 64 # Tamaño del primer mensaje que se recibirá
PORT = 7000
SERVER= socket.gethostbyname(socket.gethostname()) #gethostname devuelve el nombre del pc en que se esta corriendo el script
#gethostbyname sabiendo cual es el nombre de la maquina esta funcion devuelve la direccion de IP del pc

FORMAT='utf-8' #Formato para la conversion del mensaje recibido
DISCONNECT_MESSAGE="!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#El primer parametro es la familia del protocolo qeu se va a estudiar
#El segundo parametro indica que los datos seran enviados de manera stream
    #tambien hace referencia a una conexion TCP/IP

ADDR =(SERVER,PORT) #Debe ser una tupla para usar el socket

server.bind(ADDR)# Se une el socket a la direccion del pc

def handle_client(conn,addr): # Esta funcion estar en paralelo 
    print(f"[NEW CONNECTION] {addr} connected.\n")
    connected=True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT) #Blocking code
        #Parametro: tamaño del mensaje
        #El primer mensaje que será recibido contendra informacion sobre el tamaño de los siguientes mensajes
        if msg:
            print(f"[ADDRESS: {addr}]\n MESSAGE: {msg}")
        conn.sendall(b'Hello we are connected:1')
        value = int(input("Valor: "))
        conn.sendall(bytes([value]))
    conn.close()    
        
        
        
def start(): #Nuevas conexiones
    
    server.listen() #Escuchar para nuevas conexiones
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr=server.accept() 
        #El metodo accept() devuelve la direccion donde esta el socket del cliente y tambien el objeto, i.e, el socket
        handle_client(conn, addr)
        #thread= threading.Thread(target=handle_client, args=(conn,addr))
        #Primer parametro es la funcion a la que quiero llamar
        #Segundo parametro son los argumentos que se le pasan a la funcion que se esta llamando
        #thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")  # Cantidad de procesos con vida 
        
    
print("[STARTING] server is starting...")
start()

