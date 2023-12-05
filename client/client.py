# ========== Import ==========
import socket
from threading import Thread
import pyaudio
import sys
import json
import time

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

"""""""""""""""""""""""""""""""""""""""""""""
   _     _      _     _      _     _   
  (c).-.(c)    (c).-.(c)    (c).-.(c)  
   / ._. \      / ._. \      / ._. \   
 __\( Y )/__  __\( Y )/__  __\( Y )/__ 
(_.-/'-'\-._)(_.-/'-'\-._)(_.-/'-'\-._)
   || U ||      || D ||      || P ||   
 _.' `-' '._  _.' `-' '._  _.' `-' '._ 
(.-./`-'\.-.)(.-./`-'\.-.)(.-./`-'\.-.)
 `-'     `-'  `-'     `-'  `-'     `-' 
"""""""""""""""""""""""""""""""""""""""""""""


class Client_udp(Thread):
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
                super().__init__()
                self.__ip_serveur = ip_serveur
                self.__port_serveur = port_serveur
                self.__socket_echange = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.__FORMAT = pyaudio.paInt16 # 16 bits
                self.__CHANNELS = 1
                self.__FREQUENCE = 44100
                self.__NB_ECHANTILLONS = 2048
                self.__TEMPS_ENREGISTREMENT = 3
                self.__audio = pyaudio.PyAudio()
                self.__appel = False
                self.__stream_emeteur = self.__audio.open(format= self.__FORMAT, channels= self.__CHANNELS, rate= self.__FREQUENCE, input=True)
                self.__stream_recepteur = self.__audio.open(format= self.__FORMAT, channels= self.__CHANNELS, rate= self.__FREQUENCE, output=True, frames_per_buffer= self.__NB_ECHANTILLONS)

    def envoie(self):
            self.__appel = True
            while self.__appel:
                    data = self.__stream_emeteur.read(self.__NB_ECHANTILLONS)
                    # envoi du donnees
                    self.__socket_echange.sendto(data,(self.__ip_serveur, self.__port_serveur))
    def reception(self):
            self.__socket_echange.bind(('', self.__port_serveur))
            self.__appel = True
            while self.__appel:
                    data, addr = self.__socket_echange.recvfrom(4096)
                    self.__stream_recepteur.write(data)
        
    def run(self):
            try:
                    print("debut de l'appel")
                    Thread(target=self.envoie).start()
                    Thread(target=self.reception).start()
            except KeyboardInterrupt:
                    # fermeture de la connexion
                    self.__socket_echange.close()
                    print("Connexion fermée")
    def stop(self):
        self.__appel = False
        self.__socket_echange.close()
        print("Connexion fermée")

##interface graphique

     
# ========== Main ==========
def main():
    # declaration des variables
    ip_serveur: str = '127.0.0.1'
    port_serveur: int = 5000
    client: Client_udp = None
    client = Client_udp(ip_serveur, port_serveur)
    client.start()



if __name__ == '__main__':
    main()



