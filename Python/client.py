import socket
from datetime import datetime
#from prettytable import PrettyTable
import threading
import queue

def menu():
    #client.sendall(b'send')
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
queue_client = queue.Queue()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

status = client.connect(ADDR)
print(f"Status: {status}")

print("[STARTING] client is started")
initial_time = datetime.now()
thr1 = threading.Thread(target=menu)
while True:
    client.sendall(b"REQ")