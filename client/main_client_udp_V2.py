#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys
import pyaudio
import threading

class Appele_udp(threading.Thread):
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
                self.__stream_emeteur = self.__audio.open(format= self.__FORMAT, channels= self.__CHANNELS, rate= self.__FREQUENCE, input=True)
                self.__stream_recepteur = self.__audio.open(format= self.__FORMAT, channels= self.__CHANNELS, rate= self.__FREQUENCE, output=True, frames_per_buffer= self.__NB_ECHANTILLONS)

        def envoie(self):
                while True:
                        data = self.__stream_emeteur.read(self.__NB_ECHANTILLONS)
                        # envoi du donnees
                        self.__socket_echange.sendto(data,(self.__ip_serveur, self.__port_serveur))
        def reception(self):
                self.__socket_echange.bind(('', self.__port_serveur))
                while True:
                        data, addr = self.__socket_echange.recvfrom(4096)
                        self.__stream_recepteur.write(data)
        
        def run(self):
                try:
                        print("debut de l'appel")
                        threading.Thread(target=self.envoie).start()
                        threading.Thread(target=self.reception).start()
                except KeyboardInterrupt:
                        # fermeture de la connexion
                        self.__socket_echange.close()
                        print("Connexion fermée")


if __name__ == "__main__":
        # declaration des variables
        ip_serveur: str = None
        port_serveur: int = None
        appele_udp: Appele_udp
        # initialisation
        ip_serveur = "172.20.10.3"
        port_serveur = 12800
        # instanciation:
        appele_udp = Appele_udp(ip_serveur=ip_serveur, port_serveur=port_serveur)
        appele_udp.start()
        appele_udp.join()

