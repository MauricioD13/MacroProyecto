import queue
queue_socket = queue.Queue()
queue_client = queue.Queue()

def storeInQueue():
    i = 0
    name = input("Name: ")
    queue_socket.put(name)
print("Aqui estoy")
i = 0
print(queue_socket.empty())
queue_socket.put(1)
my_data = queue_socket.get()#Blocking code
print(my_data)

i+=1