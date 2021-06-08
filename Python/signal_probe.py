import threading
import queue
import time
queue_socket = queue.Queue()
queue_client = queue.Queue()

def storeInQueue():
    name = input("Name: ")
    queue_socket.put(name)

def receiving_socket():
    time.sleep(3)
    queue_client.put(1)
t = threading.Thread(target=storeInQueue)
t.start()

my_data = queue_socket.get()
print(my_data)
