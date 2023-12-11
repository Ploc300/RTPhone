# ========== Import ==========
import socket
from threading import Thread
import sys
import json


# ========== Class ==========

class Client_tcp:
    def __init__(self, ip_serveur: str, port_serveur: int)->None:
        self.ip_serveur = ip_serveur
        self.port_serveur = port_serveur
        self.socket_client = None

    def connect_tcp(self)->None:
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.settimeout(5)
            self.socket_client.connect((self.ip_serveur, self.port_serveur))
        except Exception as ex:
            print("le serveur fais dodo  :", ex)
            sys.exit(1)
    
    def envoie(self, msg: str)-> None:
            self.socket_client.send(msg.encode('utf-8'))
    
    def receive(self)-> str: 
        try:
            msg = self.socket_client.recv(1024)
            if msg == None:
                raise Exception
                return msg.decode('utf-8')
            
        except Exception as ex:
            print("le serveur nous boycotte, quel connard :", ex)

    
    def auth(self,nom,mail,mdp)->None:
        if nom :
            hash ={'nom' : nom , 'mdp' : mdp}
            hash = json.dumps(hash)
            self.envoie("01",hash)
        else :
            hash ={'mail' : mail , 'mdp' : mdp}
            hash = json.dumps(hash)
            self.envoie("01",hash)
    
    def get_phone(self)->None:
        self.envoie('02')
        phone = self.receive()
        return phone
    
    def change_phone(self)->None:
        self.send('03')
        phone = self.receive()
        return phone

    def get_mail(self)->None:
        self.send('04')
        mail = self.receive()
        return mail
    
    def get_nom(self)->None:
        self.send('05')
        nom = self.receive()
        return nom





##interface graphique

     
# ========== Main ==========
def main():
    # declaration des variables
    ip_serveur: str = '127.0.0.1'
    port_serveur: int = 5000
    client: Client_tcp
    client = Client_tcp(ip_serveur, port_serveur)
    client.start()
    client.connect_tcp()
    client.envoie('bonjour serveur')
    print(client.receive())
    print(client.get_connected_client())



if __name__ == '__main__':
    main()



