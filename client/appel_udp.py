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
## ========== Import ==========
import socket
from threading import Thread
import pyaudio
import sys
import time
## ========== Class ==========

class Client_udp(Thread):
        def __init__(self, ip_serveur: str, port_serveur: int, port_client: int) -> None:
                super().__init__()
                self.__ip_serveur = ip_serveur
                self.__port_serveur = port_serveur
                self.__port_client = port_client
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
                        data = self.__stream_emeteur.read(self.__NB_ECHANTILLONS*2)
                        # envoi du donnees
                        try:
                                self.__socket_echange.sendto(data,(self.__ip_serveur, self.__port_serveur))
                        except OSError:
                                pass
        
        def reception(self):
                self.__socket_echange.bind(('', 5002))
                self.__appel = True
                while self.__appel:
                        try:
                                data, _ = self.__socket_echange.recvfrom(4096*2)
                        except ConnectionResetError:
                                data = b''
                        if data != b'':
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

        def racroche(self):
                self.__socket_echange.sendto(b'42',(self.__ip_serveur, self.__port_serveur))
                self.__appel = False
                self.__socket_echange.close()
                print("Connexion fermée")


if __name__ == "__main__":
        serveur = '127.0.0.1'
        port = 5001
        client = Client_udp(serveur, port, 5002)
        client.start()
        input("Appuyer sur une touche pour raccrocher")
        client.racroche()

