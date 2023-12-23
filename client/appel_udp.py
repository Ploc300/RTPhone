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
                    self.__socket_echange.sendto(data,(self.__ip_serveur, self.__port_serveur))
    def reception(self):
            self.__socket_echange.bind(('', 5002))
            self.__appel = True
            while self.__appel:
                    data, addr = self.__socket_echange.recvfrom(4096*2)
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


if __name__ == "__main__":
        ip_serveur = "127.0.0.1"
        port_serveur = 5001
        port_client = 5002
        client = Client_udp(ip_serveur, port_serveur, port_client)
        client.start()
        input('Appuyez sur une touche pour quitter')
        client.stop()
        sys.exit(0)