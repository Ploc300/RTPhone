# ========== Import ==========
from debug import debug, debug_verbose
from json import loads, dumps
from threading import Thread
import socket, time, pyaudio, dotenv
from db import Database

# ========== Constant ==========
dotenv.load_dotenv()

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

        self.__frames_per_buffer: int = 4096

        self.__communication_status: bool = False

    def send(self, data: bytes, source: str) -> None:
        """
            Envoie les données à tous les clients connectés

            :param data: Données à envoyer
            :param source: Adresse du client source

            :return: None
        """
        print("Sending data")
        if not self.__sending_socket is None:
            for client in self.__clients:
                print(client)
                if client != source:
                    self.__sending_socket.sendto(data, (client, 5002))

    def receive(self) -> bytes:
        """
            Recoit les données d'un client

            :return: Données reçues
        """
        while self.__communication_status:
            buffer: bytes = b''
            if not self.__receiving_socket is None:
                buffer, addr = self.__receiving_socket.recvfrom(self.__frames_per_buffer*2)
                if not addr[0] in self.__clients or buffer == b'':
                    buffer = b'Nothing or not a client'
                else:
                    if buffer == b'42':
                        self.__clients.remove(addr[0])
                        debug(INFO.format(info=f'callserver.py: {addr[0]} disconnected'))
                        if len(self.__clients) == 0:
                            debug(INFO.format(info=f'callserver.py: No more clients connected'))
                            self.stop()
                    else:
                        Thread(target=self.send, args=(buffer, addr[0])).start()
                    debug(f'callserver.py: {addr[0]} sent {len(buffer)} bytes')
                    # debug_verbose(f'callserver.py: {buffer}')
            else:
                debug(ERROR.format(error=f'callserver.py: Failed to receive data'))

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
        self.__receiving_thread = Thread(target=self.receive)

    def start(self) -> None:
        """
            Lance le serveur d'appel

            :return: None
        """
        self.__communication_status = True
        self.init_sockets()
        self.init_threads()
        self.__receiving_thread.start()

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
        self.__users_ip: set = set()
        self.retrieve_users_ip()
        self.__source: str = source
        self.__port: int = 5003
        self.__socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(('', self.__port))

    def retrieve_users_ip(self) -> None:
        db = Database('Retrieve users ip')
        for user in self.__users:
            ip = db.retrieve_user_ip(user)
            if not ip is None and ip != self.__source:
                self.__users_ip.add(db.retrieve_user_ip(user))
        debug(INFO.format(info=f'callserver.py: Users ip successfully retrieved'))
        debug_verbose(f'callserver.py: {self.__users_ip}')

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
        """
            Envoie une requête d'appel à tous les utilisateurs

            :return: Set des utilisateurs ayant accepté l'appel
        """
        for user in self.__users:
            if user != self.__source:
                tmp_users: set = self.__users.copy()
                tmp_users.remove(user)
                data: dict = {'users': tmp_users}
                self.send(f'14 {dumps(list(data))}', user)
        
        answers: set = set()
        answers.add(self.__source)
        start: float = time.time()
        index = 1
        while time.time() - start < 10 and index < len(self.__users): # laisse 10 secondes aux utilisateurs pour répondre
            msg, addr = self.receive()
            code, data = msg.split(' ', 1)
            if addr in self.__users:
                match code:
                    case '15':
                        debug(INFO.format(info=f'callserver.py: {addr} accepted the call'))
                        answers.add(addr)
                    case '16':
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
             
                
def test_appel(ip_list: list, event=None) -> None:
    """
        Teste l'appel

        :return: None
    """
    clients = set()
    for ip in ip_list:
        clients.add(ip)
    appel = CallServer(clients).start()
    input('Press enter to stop')
        
        
    



            

# ========== Main ==========
if __name__ == "__main__":
    clients: set = set()
    clients.add('127.0.0.1') # ip client 1 (ip, port)
    # clients.add(('', 5002)) # ip client 2 (ip, port)
    appel = CallServer(clients).start()
    input('Press enter to stop')
