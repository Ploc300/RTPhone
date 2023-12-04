# ========== Import ==========
import socket, pyaudio, dotenv, os, json
from threading import Thread
from authentification import auth

# ========== Constant ==========
dotenv.load_dotenv()
DEBUG_STATUS: bool = bool(os.getenv('DEBUG'))
POSSIBLE_CODE: list = [str(i) if i > 10 else '0'+str(i) for i in range(0, 100)]

# ========== Color ==========
ERROR: str = '\033[91m[ERROR]\033[0m {error}'
WARNING: str = '\033[93m[WARNING]\033[0m {warning}'
SUCCESS: str = '\033[92m[SUCCESS]\033[0m {success}'
DEBUG: str = '\033[94m[DEBUG]\033[0m {debug}'
INFO: str = '\033[96m[INFO]\033[0m {info}'



# ========== Function ==========
def debug(msg: str) -> None:
    """
        Affiche un message de debug
    """
    if DEBUG_STATUS: print(f'{DEBUG.format(debug=msg)}')


# ========== Class ==========      
class ListeningService:
    """
        Classe permettant de créer un serveur d'écoute sur un port donné

        :param port: le port du serveur
        :param max_client: le nombre maximum de client
    """
    def __init__(self, port: int, max_client: int) -> None:
        """
            Initialise le serveur:
                - Création du socket
                - Bind du socket
                - Mise en écoute du socket

            :param port: le port du serveur
            :param max_client: le nombre maximum de client
        """
        self.__port: int = port
        self.__max_client: int = max_client

        try: # Initialisation du socket
            self.__socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            debug(SUCCESS.format(success='Server socket created'))
        except Exception as e:
            debug(ERROR.format(error='Failed to create server socket'))
            exit(2)

        try: # Bind du socket
            self.__socket.bind(('', self.__port))
            debug(SUCCESS.format(success='Server socket binded'))
        except Exception as e:
            debug(ERROR.format(error='Failed to bind server socket'))
            exit(3)

        try: # Mise en écoute du socket
            self.__socket.listen(self.__max_client)
            debug(SUCCESS.format(success='Socket listening'))
        except Exception as e:
            debug(ERROR.format(error='Failed to listen socket'))
            exit(4)

    def wait(self) -> socket:
        """
            Attente des clients
            :return: le socket d'échange avec le client
        """
        debug(INFO.format(info='Waiting for client'))
        try: # Attente des clients
            socket_echange, addr = self.__socket.accept()
            return socket_echange
        except Exception as e:
            debug(ERROR.format(error='Failed to accept client'))
            exit(6)
    
class ClientHandler(Thread):
    """
        Classe permettant de gérer un client

        :param socket_echange: le socket d'échange avec le client
    """
    def __init__(self, socket_echange: socket) -> None:
        """
            Initialise le client:
                - Création du socket d'échange

            :param socket_echange: le socket d'échange avec le client
        """
        super().__init__()
        try: # Initialisation du socket
            self.__socket_echange: socket = socket_echange
            debug(SUCCESS.format(success='Socket created'))
        except Exception as e:
            debug(ERROR.format(error='Failed to create socket for client'))
            exit(5)

    def send(self, msg: str) -> None:
        """
            Envoi un message au client

            :param msg: le message à envoyer
        """
        try: # Encodage du message
            encoded_msg = msg.encode("utf-8")
        except Exception as e:
            debug(ERROR.format(error='Failed to encode message'))
            exit(7)
        try: # Envoi du message
            self.__socket_echange.send(msg)
        except Exception as e:
            debug(ERROR.format(error='Failed to send message'))
            exit(8)

    def recevoir(self) -> str:
        """
            Recoit un message du client

            :return: le message reçu
        """
        try: # Réception du message
            msg: bytes = self.__socket_echange.recv(1024)
            return msg.decode("utf-8")
        except Exception as e:
            debug(ERROR.format(error='Failed to receive message'))
            exit(9)
    
    def run(self) -> None:
        """
            Fonction principale du client
        """
        msg_reception: str
        buffer: str
        code: str ='99'
        while not msg_reception[0:2] == '00': # Tant que le client n'a pas envoyé le code de fin
            buffer: str = self.recevoir()
            code, message = buffer[0:2], buffer[3:].loads() # Récupération du code et du message
            if code in POSSIBLE_CODE: # Si le code est valide
                match code:
                    case '99': # Initialisation du client
                        debug(INFO.format(info='Initializing client connection'))
                        break
                    case '01': # Authentification
                        debug(INFO.format(info='Authenticating client'))
                        try:
                            
                            
                        
                        

            else:
                debug(ERROR.format(error='Unknown code'))
                try:
                    self.send('00 Unknown code')
                except Exception as e:
                    debug(ERROR.format(error='Failed to send termination message'))
                exit(10)
        self.arret()

    

    def arret(self) -> None:
        """
            Arrêt du client
        """
        self.__socket_echange.close()
    
class ClientManager:
    """
        Classe permettant de gérer les clients
    """
    def __init__(self) -> None:
        """
            Initialise le gestionnaire de client
        """
        self.__list_client: list = []

    def add_client(self, client: socket) -> None:
        """
            Ajoute un client à la liste des clients
        """
        self.__list_client.append(client)

    def get_number_client(self) -> int:
        """
            Retourne le nombre de client
        """
        return len(self.__list_client)


# ========== Main ==========
def main():
    ListeningService: ListeningService = ListeningService('172.20.10.3', 5000, 10)
    clientManager: ClientManager = ClientManager()

    while True:
        if clientManager.get_number_client() < 10:
            socketClient: socket = ListeningService.wait()

            socket_echange: ClientHandler = ClientHandler(socketClient)

            socket_echange.start()

            clientManager.add_client(socket_echange)
            debug(INFO.format(info='New client added'))




if __name__ == '__main__':
    main()
