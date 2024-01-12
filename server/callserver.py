# ========== Import ==========
from debug import debug, debug_verbose
from json import loads, dumps
from threading import Thread
import socket, time, pyaudio

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
        print(buffer)
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

class CallRequest:
    def __init__(self, users: set, source: str) -> None:
        """
            Initialise la requête d'appel

            :param users: Liste des utilisateurs a appeler
            :param source: Adresse de l'utilisateur source

            :return: None
        """
        self.__users: set = users
        self.__source: str = source
        self.__port: int = 5003
        self.__socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(('', self.__port))

    def send(self, msg: str, dest: str) -> None:
        """
            Envoi un message au client

            :param msg: le message à envoyer

            :return: None
        """
        try:  # Encodage du message
            encoded_msg = msg.encode("utf-8")
            debug(INFO.format(info=f'callserver.py: Message successfully encoded'))
        except UnicodeEncodeError as e:
            debug(ERROR.format(error=f'callserver.py: Failed to encode message'))
            debug_verbose(f'callserver.py: {e}')

        try:  # Envoi du message
            self.__socket.sendto(encoded_msg, (dest, self.__port))
            debug(INFO.format(info=f'callserver.py: Message successfully sent'))
        except socket.error as e:
            debug(ERROR.format(error=f'callserver.py: Failed to send message'))
            debug_verbose(f'callserver.py: {e}')
        

    def receive(self) -> tuple:
        """
            Recoit un message du client

            :return: le message reçu
        """
        _return = None
        try:  # Réception du message
            msg, addr = self.__socket.recvfrom(1024)
            debug(INFO.format(info=f'callserver.py: Message successfully received'))
            try:
                _return = (msg.decode("utf-8"), addr)
                debug(INFO.format(info=f'callserver.py: Message successfully decoded'))
            except UnicodeDecodeError as e:
                debug(ERROR.format(error=f'callserver.py: Failed to decode message'))
                debug_verbose(f'callserver.py: {e}')
        except socket.error as e:
            debug(ERROR.format(error=f'server.py: Failed to receive message'))
            debug_verbose(f'callserver.py: {e}')
        return _return
    
    def requests(self) -> set:
        for user in self.__users:
            if user != self.__source:
                tmp_users: set = self.__users.copy()
                tmp_users.remove(user)
                data: dict = {'users': tmp_users}
                self.send(f'14 {dumps(data)}', user)
        
        answers: set = set()
        start: float = time.time()
        index = 1
        while time.time() - start < 10 and index < len(self.__users):
            msg, addr = self.receive()
            code, data = msg.split(' ', 1)
            if addr in self.__users:
                match code:
                    case '15':
                        debug(INFO.format(info=f'callserver.py: {addr} accepted the call'))
                        answers.add(addr)
                    case 16:
                        debug(INFO.format(info=f'callserver.py: {addr} refused the call'))
            index += 1
        self.close()
        return answers
    
    def close(self) -> None:
        """
            Ferme le socket

            :return: None
        """
        self.__socket.close()
             
                
    
        
        
    



            

# ========== Main ==========


