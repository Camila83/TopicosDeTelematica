import socket as s
import json
import time

class Client():
    
    def __init__(self, port, host):
        self.socketPort = port
        self.dataPort = port + 10
        self.socket = s.socket()
        self.host = host
        self.path = "localFiles"

    def clientStart(self):
        try:
            self.socket.connect((self.host,self.socketPort))
        except:
            print(s.error())
            return
        print("Connected to the server " + self.host)
        
        self.commandMenu()
    def receiveData(self):
        response = self.socket.recv(1024)
        data = json.loads(response.decode('utf-8'))
        print(data)
    
    def sendGet(self):
        dataPacket = {"method" : "GET"}
        validData = json.dumps(dataPacket).encode('utf-8')
        self.socket.sendall(validData)

    def sendPost(self, data):
        dataPacket = {
            "method" : "POST",
            "value" : data
                    }
        validData = json.dumps(dataPacket).encode('utf-8')
        self.socket.sendall(validData)
    
    def sendFileDownload(self, fileName):
        dataPacket = {
            "method" : "DWL",
            "value" : fileName
            }
        validData = json.dumps(dataPacket).encode('utf-8')    
        self.socket.sendall(validData)
        print("Envia lo que el server necesita.")

        time.sleep(1)

        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataSock.connect((self.host, self.dataPort))
        
        with open(self.path+"/"+fileName, "wb") as file:
            data = dataSock.recv(1024)
            while (data):
                file.write(data)
                data = dataSock.recv(1024)
        dataSock.close()
        return "Archivo descargado exitosamente."
    
    def sendFileUpload(self, fileName): 
        dataPacket = {
            "method" : "UPL",
            "value" : fileName
            }
        validData = json.dumps(dataPacket).encode('utf-8')    
        self.socket.sendall(validData)

        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataSock.connect((self.host, self.dataPort))
        
        with open(self.path+"/"+fileName, "rb") as file:
            data = file.read(1024)
            while (data):
                dataSock.sendall(data)
                data = file.read(1024)
        dataSock.close()
        return "Archivo subido exitosamente."
        
    
    
    def commandMenu(self):
        entryPoint = input("Bienvenido al server, seleccione alguna de las siguientes opciones. \n1. Enviar una GET request. \n2. Enviar una POST request. \n3. Recibir un archivo tipo PDF. \n4. Enviar un archivo. \n")
        if(entryPoint is not None):
            if(entryPoint == "1"):
                self.sendGet()
                self.receiveData()
            elif(entryPoint == "2"):
                data = input("Ingrese un texto. Ejemplo; \"Buenos dias\"")
                self.sendPost(data)
                self.receiveData()
            elif(entryPoint == "3"):
                data = input("Ingrese el nombre del archivo que desea descargar. \n")
                self.sendFileDownload(data)
            elif(entryPoint == "4"):
                data = input("Ingrese el nombre del archivo que desea subir. \n")
                self.sendFileUpload(data)
        