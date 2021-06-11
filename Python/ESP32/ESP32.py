from machine import Pin,I2C,SPI
from time import sleep
import network
import socket
from machine import Timer
counter  = 0
class Slave:
    def __init__(self, address, frequency):
        self. address_slave = address
        self.frequency = frequency
        self.i2c = I2C(scl=Pin(22),sda=Pin(21), freq= self.frequency)    
        self.msg = None
        self.address_write = 0x0000
        self.address_read = 0x0000
        
    def write(self, data):
        try:
            self.i2c.writeto_mem(self.address_slave,self.address_memory,bytes([data]),addrsize = 16)
        except:
            self.msg = 'ERROR:01'
    def read(self,amount):
        try:
            self.msg = i2c.readfrom_mem(memory_address,self.address_read,amount,addrsize = 16)
        except:
            self.msg = 'ERROR:02'
    
class ESP_I2C:
    def __init__(self, socket, ADDR,PIC,MEM,RTC):
        self.incoming_msg = 0
        self.msg = None
        self.scan_time = 1000 #Default 1 sec
        self.send_msg = False
        self.counter = 0
        self.send_time = 60
        self.save_time = 1800
        self.connected = False
        self.ADDR = ADDR
        self.socket = socket
        self.PIC = PIC
        self.MEM = MEM
        self.RTC = RTC
        
    def handler_I2C(self, t): ## Every second
        # Revisar PIC (esclavo), traer dato
        self.counter += 1
        if (self.counter%self.send_time) == 0:
            #PIC.msg = PIC.read()
            pass
        if(self.counter >= self.save_time):
            #RTC.msg = RTC.read() 
            #MEM.write(RTC.msg + PIC.msg)
            self.counter = 0
        
        if self.connected == False:  
                self.socket.connect(self.ADDR)
                self.connected = True
                print("[SOCKET START] Successful")
                
        if(self.connected == True):
            self.socket.sendall('REQ')
            self.msg = self.socket.recv(1024)
            if self.msg.decode() != 'ACK':  
                print(self.msg)
        
        
    def append_slave(self,slave):
        self.slaves.append(slave)
          
class ESP_WiFi:
    def __init__(self):
        self.port = 0
        self.server_address = 0
        self.socket = 0
        self.connections = False
    def init_wifi(self, SSID, PW):
        station = network.WLAN(network.STA_IF)
        access_point = network.WLAN(network.AP_IF)
        station.active(True)
        station.scan()
        station.connect(SSID, PW)
        while station.isconnected() == False:
            pass
        print('Connection successful')
        print(str(station.ifconfig()[0]))
        
    def init_socket(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ADDR = (self.server_address, self.port)
            print("[SOCKET CONNECTING]")

if __name__ == '__main__':
    HEADER= 64
    PORT = 7000
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE="!DISCONNECT"
    SERVER="192.168.43.190"
    memory_address = 0x51
    ADDR = (SERVER,PORT)
    RTC_address = 0xD0
    PIC_address = 0xB0
    current_memory_addr = 0
    #Pin(22,Pin.OUT)
    #Pin(21,Pin.OUT)
    
    
    esp_wifi = ESP_WiFi()
    #esp_wifi.init_wifi('Phone Ki','sancarlo')
    esp_wifi.init_wifi('Joan Muñoz','joancito')
    PIC = Slave(0xD0,400000)
    MEM = Slave(0x50,400000)
    
    MEM.write('1')
    esp_wifi.server_address = '192.168.43.190'
    esp_wifi.port = 7000
    esp_wifi.init_socket()
    esp_i2c = ESP_I2C(esp_wifi.socket,(esp_wifi.server_address,esp_wifi.port))
    timer = Timer(1)
    timer.init(period = 1000, mode = Timer.PERIODIC, callback = esp_i2c.handler_I2C)
    
    
    
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