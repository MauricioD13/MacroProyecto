from machine import Pin,I2C,SPI
from time import sleep
import network
import socket
from machine import Timer

counter = 0
HEADER= 64
PORT = 7000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE="!DISCONNECT"
SERVER="192.168.43.218"
memory_address = 0x51
RTC_address = 0xD0
PIC_address = 0xB0
current_memory_addr = 0
Pin(22,Pin.OUT)
Pin(21,Pin.OUT)

#TIMER

def handle_client(conn,addr):
    print("[NEW CONNECTION] connected:",(addr))
    connected=True
    while connected:
            msg = conn.recv(HEADER).decode(FORMAT) #Blocking code
            
            if msg != 'DISCONNECT':
                if msg == '1':
                    
                conn.sendall(b'ACK')
            else:
                print("DISCONNECTING")
                connected = False
                conn.close()
            
        #value = int(input("Valor: "))
        #conn.sendall(bytes([value]))

def handler_I2C(t): ## Every second
    # Revisar PIC (esclavo), traer dato
    
    
    counter +=1
    command_I2C = read_PIC()
    if command_I2C == 1: #Default
        if counter == 60:
            #Data from PIC, send to client
            
        elif counter == 1800:
            #Write data into memory
            counter = 0
            
    elif command_I2C == 2: #Event
        if counter == 60:
            #Write data into memory

def server_start(): #Nuevas conexiones
    
    server.listen(10) #Escuchar para nuevas conexiones
    #print("[LISTENING] Server is listening on {SERVER}".format(SERVER))
    i2c = init_i2c()
    while True:
        
        conn, addr=server.accept() 
        #El metodo accept() devuelve la direccion donde esta el socket del cliente y tambien el objeto, i.e, el socket
        msg = handle_client(conn, addr)
        print(msg)
        #write_memory(memory_address,msg,i2c)
                   
  
def init_socket():
      
    ADDR= (SERVER, PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR =(SERVER,PORT) #Debe ser una tupla para usar el socket

    server.bind(ADDR)# Se une el socket a la direccion del pc
    return server

def init_wifi():
    station = network.WLAN(network.STA_IF)
    access_point = network.WLAN(network.AP_IF)

    station.active(True)
    station.scan()
    station.connect('Redmi','12341234')
    while station.isconnected() == False:
        pass
    print('Connection succesfull')
    print(str(station.ifconfig()[0]))
def init_i2c():
    
    i2c = I2C(scl=Pin(22),sda=Pin(21), freq=400000)
    
    return i2c

def write_memory(memory_address,data,i2c):
    try:
        i2c.writeto_mem(0x51,0x0000,bytes([int(data)]),addrsize = 16)
    except:
        i2c.writeto_mem(0x51,0x0000,bytes([int(data)]),addrsize = 16)
def read_memory(memory_address):
    
    msg = i2c.readfrom_mem(memory_address,0x0000,1,addrsize = 16)
    

if __name__ == '__main__': 
    timer = Timer(1)
    timer.init(period = 1000, mode = Timer.PERIODIC, callback = handler_I2C)  # 16 mHz frequency
    
    #init_wifi()
    
    #server = init_socket()
    
    #print("[STARTING] server is starting...")
    #server_start()
    
    
    """i2c = init_i2c()
    i2c = I2C(scl=Pin(22),sda=Pin(21), freq=400000)
    value = 1
    #i2c.writeto_mem(0x50,0x0000,bytes([value]),addrsize = 16)
    try:
        msg = i2c.readfrom_mem(0x50,0x0000,1,addrsize = 16)
    except OSError:
        print("Error")
        msg = 0
        
    #msg = i2c.readfrom_mem(0x51,0x0000,1,addrsize = 16)
    print(msg)
    
"""
"""
value = int(input("Value: "))
print(value)
i2c.writeto_mem(0x50,0x0000,bytes([value]),addrsize = 16)
print("Value written")

option = int(input("Option: "))

msg = i2c.readfrom_mem(0x50,0x0000,1,addrsize = 16)
print(int.from_bytes(msg,'big'))

"""