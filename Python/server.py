import socket
import threading #Usar varios hilos en un mismo programa, para que el servidor pueda atender varios pedidos
import queue
import time
queue_menu = queue.Queue()
HEADER = 64
def menu():
    while True:
        option = int(input("[1]Buscar por fecha\n[2]Cambiar frecuencia de mostrar datos\n[3]Cambiar frecuencia de guardado de datos\n"))
        if option == 1:
            day = int(input("Dia del mes:"))
            command = day
            queue_menu.put('1:'+str(command))
        elif option == 2:
            seg = int(input("Tiempo (# segundos):"))
            queue_menu.put('2:'+str(seg))
        elif option == 3:
            minutes = int(input('Tiempo (# minutos):'))
            queue_menu.put('3:'+str(minutes))
        
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
    connected=True
    print(f"[NEW CONNECTION] {addr} connected.\n")
    date = time.strftime('%x')
    hour = time.strftime('%X')
    conn.sendall((date+','+hour).encode())
    while connected:
        
        msg = conn.recv(1024)
        if msg.decode() == 'REQ':
            if(queue_menu.empty() == False):
                command = queue_menu.get()

                    
                command = 'COMM'+str(command)
                conn.sendall(command.encode())
            else:
                conn.sendall(b'ACK')
        else:
            print(msg)
    conn.close()    
        
        
        
def start(): #Nuevas conexiones
    
    server.listen() #Escuchar para nuevas conexiones
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr=server.accept() 
        #El metodo accept() devuelve la direccion donde esta el socket del cliente y tambien el objeto, i.e, el socket
        thr1 = threading.Thread(target = menu)
        thr1.start()
        handle_client(conn,addr)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")  # Cantidad de procesos con vida 
        
    
print("[STARTING] server is starting...")
start()

