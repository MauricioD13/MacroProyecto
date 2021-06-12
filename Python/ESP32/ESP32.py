from machine import Pin,I2C,SPI
from time import sleep
import network
import socket
from machine import Timer
counter  = 0
def decode_date(msg):
    date = msg.split(',')[0]
    hour_complete = msg.split(',')[1]
    return date, hour_complete
def search_date(init_day,day):
    n = init_day - day
    return ((n-1)*2.5)*128
class Slave:
    def __init__(self, address, frequency):
        self. address_slave = address
        self.frequency = frequency
        self.i2c = I2C(scl=Pin(22),sda=Pin(21), freq= self.frequency)    
        self.msg = None
        self.address_write = 0x0000
        self.address_read = 0x0000
        self.sendto_wifi = False
        self.day = 0
    def init_rtc(self,minute,hour,day,month,year):
        self.day = day
        self.i2c.writeto_mem(0x68,0x00,b'\x00')
        self.i2c.writeto_mem(0x68,0x01,bytes([minute]))
        self.i2c.writeto_mem(0x68,0x02,bytes([hour]))
        self.i2c.writeto_mem(0x68,0x03,b'\x05')
        self.i2c.writeto_mem(0x68,0x04,bytes([day]))
        self.i2c.writeto_mem(0x68,0x05,bytes([month]))
        self.i2c.writeto_mem(0x68,0x06,bytes([year]))
        
    
class ESP_I2C:
    def __init__(self, socket, ADDR,PIC,MEM,RTC):
        self.incoming_msg = 0
        self.msg = None
        self.scan_time = 1000 #Default 1 sec
        self.send_msg = False
        self.counter = 0
        self.send_time = 10
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
            #PIC.msg =  i2c.readfrom(0x60,2)
            PIC.msg = 1
            PIC.sendto_wifi = False
            
        if(self.counter >= self.save_time):
            #RTC.msg = RTC.read() 
            #MEM.write(RTC.msg + PIC.msg)
            self.counter = 0
                
        if(self.connected == True):
            if(PIC.sendto_wifi == True):
                self.socket.sendall(bytearray(PIC.msg))
                PIC.sento_wifi = False
            self.socket.sendall('REQ')
            self.msg = self.socket.recv(1024)
            
            if self.msg.decode() != 'ACK':
                aux_msg = self.msg.decode().split(':')
                if aux_msg[0] == 'COMM1':
                    mem_address = search_date(RTC.day,int(aux_msg[1]))
                elif aux_msg[0] == 'COMM2':
                    self.send_time = int(aux_msg[1])
                elif aux_msg[0] == 'COMM3':
                    self.save_time = int(aux_msg[1])*60
                    
                    
                    
                
            
        
        
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
        
    def init_socket(self,RTC):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ADDR = (self.server_address, self.port)
            print("[SOCKET CONNECTING]")
            self.socket.connect(ADDR)
            print("[SOCKET START] Successful")
            msg = self.socket.recv(1024)
            print(msg)
            date, hour_complete = decode_date(msg.decode())
            aux_hour = hour_complete.split(':')
            aux_date = date.split('/')
            try:
                RTC.init_rtc(aux_hour[1],aux_hour[0],aux_date[0],aux_date[1],aux_date[2])
            except:
                self.socket.sendall(b'Error:RTC falling')
            return True

if __name__ == '__main__':

    connected = False
    #Pin(22,Pin.OUT)
    #Pin(21,Pin.OUT)
    
    
    esp_wifi = ESP_WiFi()
    #esp_wifi.init_wifi('Phone Ki','sancarlo')
    esp_wifi.init_wifi('Cuello Alzate','Zaatar017')
    PIC = Slave(0x60,400000)
    MEM = Slave(0x50,400000)
    RTC = Slave(0x68,100000)
    
    #esp_wifi.server_address = '192.168.43.190'
    esp_wifi.server_address = '192.168.0.7'
    esp_wifi.port = 7000
    connected = esp_wifi.init_socket(RTC)
    esp_i2c = ESP_I2C(esp_wifi.socket,(esp_wifi.server_address,esp_wifi.port), PIC, MEM, RTC)
    esp_i2c.connected = connected
    timer = Timer(1)
    timer.init(period = esp_i2c.scan_time, mode = Timer.PERIODIC, callback = esp_i2c.handler_I2C)
    