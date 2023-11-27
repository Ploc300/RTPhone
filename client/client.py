# ========== Import ==========
import socket
from threading import Thread
import pyaudio
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
            self.socket_client.connect((self.ip_serveur, self.port_serveur))
        except Exception as ex:
            print("Serveur inaccessible erreur :", ex)
            sys.exit(1)
    
    def envoie(self, msg: str)-> None:
            self.socket_client.send(msg.encode('utf-8'))
    
    def receive(self)-> str: 
        try:
            msg = self.socket_client.recv(1024)
            if msg == None:
                raise Exception
        except Exception as ex:
            print("le serveur nous boycotte, quel connard", ex)
        return msg.decode('utf-8')
    
    def auth(self,nom,mail,mdp)->None:
        if nom :
            hash = {'nom' : nom , 'mdp' : mdp}
            hash = json.dumps(hash)
            self.send(hash)
        else :
            hash = {'mail' : mail , 'mdp' : mdp}
            hash = json.dumps(hash)
            self.send(hash)
    
    def get_phone(self)->None:
        self.send('get_phone')
        phone = self.receive()
        return phone
    
    def change_phone(self)->None:
        self.send('change_phone')
        phone = self.receive()
        return phone

    def get_mail(self)->None:
        self.send('get_mail')
        mail = self.receive()
        return mail

class Client_udp:
    pass
# ========== Main ==========
def main():
    # declaration des variables
    ip_serveur: str = '172.20.10.3'
    port_serveur: int = 5000
    client: Client_tcp = None
    client = Client_tcp(ip_serveur, port_serveur)
    client.connect_tcp()
    client.envoie('bonjour serveur')
    print(client.receive())



if __name__ == '__main__':
    main()



