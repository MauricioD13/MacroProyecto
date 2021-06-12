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

def write_memory(memory_address,data,i2c):
    try:
        i2c.writeto_mem(memory_address,0x0000,bytes([int(data)]),addrsize = 8)
    except:
        i2c.writeto_mem(0x51,0x0000,bytes([int(data)]),addrsize = 16)

def read_memory(memory_address):
    
    msg = i2c.readfrom_mem(memory_address,0x0000,1,addrsize = 8)
 
def init_rtc(i2c):
    
    i2c.writeto_mem(0x68,0x00,b'\x00')
    i2c.writeto_mem(0x68,0x01,b'\x00')
    i2c.writeto_mem(0x68,0x02,b'\x07')
    i2c.writeto_mem(0x68,0x03,b'\x05')
    i2c.writeto_mem(0x68,0x04,b'\x0B')
    i2c.writeto_mem(0x68,0x05,b'\x06')
    i2c.writeto_mem(0x68,0x06,b'\x15')
    #i2c.writeto_mem(0x68,0x07,b'\x13')    
    
    

if __name__ == '__main__':

    i2c = I2C(scl=Pin(22),sda=Pin(21), freq=400000)
   
    while True:
        option = int(input('Opcion: '))
        if(option == 1):
            init_rtc(i2c)
        elif option == 2:
            msg = i2c.readfrom_mem(0x68,0x00,8)
            i2c.stop()
            print(msg)
        elif option == 3:
            msg = i2c.readfrom(0x60,2)
            print(msg)
        else:
            i2c.writeto(0x60,b'\x17')
            
    
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