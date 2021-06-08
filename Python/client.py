import socket
from datetime import datetime

def menu(client):
    client.sendall(b'send')
    option = int(input("[1]Enviar mensaje\n[2]Cambiar frecuencia\n[3]Desconectar\n"))
    return option

def time_evaluator(initial_time):
    last_time = datetime.now()
    time_seconds = (last_time - initial_time).seconds
    initial_time = datetime.now()
    return time_seconds


ACK = 0
HEADER= 64
PORT = 7000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE="!DISCONNECT"
SERVER="192.168.43.218"

ADDR= (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

status = client.connect(ADDR)
print(f"Status: {status}")

print("[STARTING] client is started")
initial_time = datetime.now()
while True:
    option = menu()
    if option == 1:
        msg = input("Mensaje: ")
        client.sendall(msg.encode())
        while ACK != 'ACK':
            ACK = client.recv(HEADER).decode()
        print("Server ACK")
            
    elif option == 3:
        client.sendall(b'DISCONNECT')
        client.close()
        break
    else:
        

