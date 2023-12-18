# ========== Import ==========
from debug import debug, debug_verbose
from json import loads, dumps
from threading import Thread
import socket
import pyaudio


# ========== Constant ==========

# ========== Color ==========
ERROR: str = '\033[91m[ERROR]\033[0m {error}'
WARNING: str = '\033[93m[WARNING]\033[0m {warning}'
SUCCESS: str = '\033[92m[SUCCESS]\033[0m {success}'
DEBUG: str = '\033[94m[DEBUG]\033[0m {debug}'
INFO: str = '\033[96m[INFO]\033[0m {info}'


# ========== Function ==========


# ========== Class ==========
class CallServer:
    def __init__(self, clients: set) -> None:
        """
            Initialise le serveur d'appel

            :param clients: Liste des clients connectés

            :return: None
        """
        self.__port: int = 5001

        self.__clients: set = clients
        self.__receiving_socket: socket.socket = None
        self.__receiving_thread: Thread = None

        self.__sending_socket: socket.socket = None
        self.__sending_thread: Thread = None

        self.__sample_rate: int = 44100
        self.frames_per_buffer: int = 4096

        self.__audio_input: pyaudio.Stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.__sample_rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer
        )
        self.__audio_output: pyaudio.Stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.__sample_rate,
            output=True,
            frames_per_buffer=self.frames_per_buffer
        )

        self.__communication_status: bool = False

    def send(self, data: bytes, source: str) -> None:
        """
            Envoie les données à tous les clients connectés

            :param data: Données à envoyer
            :param source: Adresse du client source

            :return: None
        """
        if not self.__sending_socket is None:
            for client in self.__clients:
                if client != source:
                    self.__sending_socket.sendto(data, client)

    def receive(self) -> bytes:
        """
            Recoit les données d'un client

            :return: Données reçues
        """
        buffer: bytes = b''
        if not self.__receiving_socket is None:
            buffer, addr = self.__receiving_socket.recvfrom(self.frames_per_buffer*2)
            if not addr in self.__clients:
                buffer = b''
        return buffer
    
    def audio_input(self) -> None:
        """
            Recoit les données audio du client

            :return: None
        """
        while self.__communication_status:
            buffer: bytes = self.__audio_input.read(self.frames_per_buffer)
            self.send(buffer, self.__receiving_socket.getsockname())

    def audio_output(self) -> None:
        """
            Envoie les données audio aux clients

            :return: None
        """
        while self.__communication_status:
            buffer: bytes = self.receive()
            self.__audio_output.write(buffer, self.frames_per_buffer)

    def init_sockets(self) -> None:
        """
            Initialise les sockets

            :return: None
        """
        self.__receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receiving_socket.bind(('', self.__port))
        self.__sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def init_threads(self) -> None:
        """
            Initialise les threads

            :return: None
        """
        self.__receiving_thread = Thread(target=self.audio_input)
        self.__sending_thread = Thread(target=self.audio_output)

    def start(self) -> None:
        """
            Lance le serveur d'appel

            :return: None
        """
        self.__communication_status = True
        self.init_sockets()
        self.init_threads()
        self.__receiving_thread.start()
        self.__sending_thread.start()

    def stop(self) -> None:
        """
            Arrête le serveur d'appel

            :return: None
        """
        self.__communication_status = False
        self.__receiving_socket.close()
        self.__sending_socket.close()




    

        
    

# ========== Main ==========
if __name__ == '__main__':
    clients: set = set()
    clients.add(('127.0.0.1', 5002))
    server = CallServer(clients)
    server.start()
    input('Press enter to stop')
    server.stop()

