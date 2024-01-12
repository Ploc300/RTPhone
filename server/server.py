# ========== Import ==========
import socket, pyaudio, dotenv, os, base64, threading
from threading import Thread
from authentification import auth, generate_token, check_token
from debug import debug, debug_verbose
from db import Database
from json import loads, dumps
import token_handler # the file automatically run the function to delete outdated token
from callserver import CallServer, CallRequest


# ========== Constant ==========
dotenv.load_dotenv()
POSSIBLE_CODE: list = [str(i) if i > 10 else '0'+str(i) for i in range(0, 100)]

KILL_ALL_THREAD: bool = False

# ========== Color ==========
ERROR: str = '\033[91m[ERROR]\033[0m {error}'
WARNING: str = '\033[93m[WARNING]\033[0m {warning}'
SUCCESS: str = '\033[92m[SUCCESS]\033[0m {success}'
DEBUG: str = '\033[94m[DEBUG]\033[0m {debug}'
INFO: str = '\033[96m[INFO]\033[0m {info}'

# ========== Function ==========


# ========== Class ==========
class ListeningService:
    """
        Classe permettant de créer un serveur d'écoute sur un port donné
    """

    def __init__(self, port: int, max_client: int) -> None:
        """
            Initialise le serveur:
                - Création du socket
                - Bind du socket
                - Mise en écoute du socket

            :param port: le port du serveur
            :param max_client: le nombre maximum de client

            :return: None
        """
        self.__port: int = port
        self.__max_client: int = max_client
        self.__running: bool = True

        try:  # Initialisation du socket
            self.__socket: socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.settimeout(0.5)
            debug(SUCCESS.format(success=f'server.py: Server socket created'))
        except socket.error as e:
            debug(ERROR.format(error=f'server.py: Failed to create server socket'))
            debug_verbose(f'server.py: {e}')

        try:  # Bind du socket
            self.__socket.bind(('', self.__port))
            debug(SUCCESS.format(success=f'server.py: Server socket binded'))
        except socket.error as e:
            debug(ERROR.format(error=f'server.py: Failed to bind server socket'))
            debug_verbose(f'server.py: {e}')

        try:  # Mise en écoute du socket
            self.__socket.listen(self.__max_client)
            debug(SUCCESS.format(success=f'server.py: Socket listening'))
        except socket.error as e:
            debug(ERROR.format(error=f'server.py: Failed to listen socket'))
            debug_verbose(f'server.py: {e}')

    def wait(self) -> socket:
        """
            Attente des clients

            :return: le socket d'échange avec le client
        """
        debug(INFO.format(info=f'server.py: Waiting for client'))
        if self.__running and not KILL_ALL_THREAD:
            try:  # Attente des clients
                try:
                    socket_echange, _ = self.__socket.accept()
                    debug(SUCCESS.format(success=f'server.py: Client accepted'))
                    return socket_echange
                except socket.timeout:
                    return None
            except socket.error as e:
                if self.__running:
                    debug(ERROR.format(error=f'server.py: Failed to accept client'))
                    debug_verbose(f'server.py: {e}')
                    #  was causing the server to never stop correctly

    def close(self) -> None:
        """
        Ferme le socket

        :return: None
        """
        self.__running = False
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
            debug(INFO.format(info=f'server.py: Server socket closed'))
        except OSError as e:
            if e.errno == 10057:  # Ignore error if the socket is already closed
                pass
            else:
                debug(ERROR.format(error=f'server.py: Failed to close server socket'))
                debug_verbose(f'server.py: {e}')


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

            :return: None
        """
        super().__init__()
        try:  # Initialisation du socket
            self.__socket_echange: socket = socket_echange
            debug(SUCCESS.format(success=f'server.py: Socket created'))
        except socket.error as e:
            debug(ERROR.format(error=f'server.py: Failed to create socket for client'))
            debug_verbose(f'server.py: {e}')

    def send(self, msg: str) -> None:
        """
            Envoi un message au client

            :param msg: le message à envoyer

            :return: None
        """
        try:  # Encodage du message
            encoded_msg = msg.encode("utf-8")
            debug(INFO.format(info=f'server.py: Message successfully encoded'))
        except UnicodeEncodeError as e:
            debug(ERROR.format(error=f'server.py: Failed to encode message'))
            debug_verbose(f'server.py: {e}')

        try:  # Envoi du message
            self.__socket_echange.send(encoded_msg)
            debug(INFO.format(info=f'server.py: Message successfully sent'))
        except socket.error as e:
            debug(ERROR.format(error=f'server.py: Failed to send message'))
            debug_verbose(f'server.py: {e}')

    def receive(self) -> str:
        """
            Recoit un message du client

            :return: le message reçu
        """
        try:  # Réception du message
            msg: bytes = self.__socket_echange.recv(1024)
            debug(INFO.format(info=f'server.py: Message successfully received'))
            try:
                return msg.decode("utf-8")
            except UnicodeDecodeError as e:
                debug(ERROR.format(error=f'server.py: Failed to decode message'))
                debug_verbose(f'server.py: {e}')
                return '98 Failed to decode message'
        except socket.error as e:
            debug(ERROR.format(error=f'server.py: Failed to receive message'))
            debug_verbose(f'server.py: {e}')

    def run(self) -> None:
        """
            Fonction principale du client

            :return: None
        """
        message: str
        buffer: str
        code: str = '99'
        while code != '00' and not KILL_ALL_THREAD:  # Tant que le client n'a pas envoyé le code de fin
            buffer: str = self.receive()
            try:
                # Récupération du code et du message
                code, message = buffer[0:2], buffer[3:]
                debug(INFO.format(info=f'server.py: Found code and data'))
            except Exception as e:
                debug(ERROR.format(
                    error=f'server.py: Failed to split code and message'))
                debug_verbose(f'server.py: {e}')
                data: dict = {'message': 'Data is missing'}
                self.send(f'09 {dumps(data)}')
            try:
                message = loads(message)  # Décodage du message
                debug(INFO.format(
                    info=f'server.py: Code: {code} | Message: {message}'))
            except Exception as e:
                debug(ERROR.format(error=f'server.py: Failed to decode message'))
                debug_verbose(f'server.py: {e}')
                data = {'message': 'Data is not JSON format'}
                self.send(f'07 {dumps(data)}')

            if code in POSSIBLE_CODE:  # Si le code est valide
                match code:
                    case '99':  # Initialisation du client
                        debug(INFO.format(
                            info=f'server.py: Initializing client connection'))
                    case '98': # Message is not UTF-8
                        debug(INFO.format(
                            info=f'server.py: Message is not UTF-8'))
                        data: dict = {'message': 'Message is not UTF-8'}
                        self.send('98 {dumps(data)}')

                    case '01':  # Authentification
                        debug(INFO.format(info=f'server.py: Authenticating client'))
                        try:
                            if auth(message['username'], message['password']):
                                debug(INFO.format(
                                    info=f'server.py: Client authenticated'))
                                data: dict = {'token': base64.b64encode(generate_token(
                                    message['username'], message['password'])).decode('utf-8')}
                                db = Database("Add client IP")
                                db.add_client_ip_token(
                                    message['username'], self.__socket_echange.getpeername()[0], data['token'])
                                self.send(f'03 {dumps(data)}')
                            else:
                                debug(ERROR.format(
                                    error=f'server.py: Failed to authenticate client'))
                                data: dict = {'message': 'Authentification failed'}
                                self.send(f'04 {dumps(data)}')
                        except Exception as e:
                            debug(ERROR.format(
                                error=f'server.py: Failed to authenticate client'))
                            debug_verbose(f'server.py: {e}')
                            data: dict = {'message': 'Authentification failed'}
                            self.send(f'04 {dumps(data)}')

                    case '02':  # Demande de son numéro de telephone
                        debug(INFO.format(
                            info=f'server.py: Client asked for phone number'))
                        try:
                            token_validity = check_token(message['token'])
                            debug_verbose(
                                f'server.py: Token validity: {token_validity}')
                        except Exception as e:
                            data: dict = {'message': 'Token is missing'}
                            self.send(f'08 {dumps(data)}')
                            debug_verbose(f'server.py: {e}')
                            continue
                        if token_validity:
                            debug(INFO.format(
                                info=f'server.py: Client token is valid'))
                            db = Database("Retrieve Phone Number")
                            data: dict = {'username': message['username'], 'phone_number': db.get_phone_number(
                                message['username'])}
                            self.send(f'05 {dumps(data)}')
                        else:
                            data: dict = {'message': 'Token is invalid'}
                            self.send(f'10 {dumps(data)}')
                    case '06':  # Demande des clients connecter
                        db = Database('STATUS')
                        debug(INFO.format(info='client'))
                        db.connected_client()

                    case '11':  # Demande d'appel
                        debug(INFO.format(info=f'server.py: Client asked for call'))
                        try:
                            token_validity = check_token(message['token'])
                            debug_verbose(
                                f'server.py: Token validity: {token_validity}')
                        except Exception as e:
                            data = {'message': 'Token is missing'}
                            self.send(f'08 {dumps(data)}')
                            debug_verbose(f'server.py: {e}')
                            continue
                        if token_validity:
                            debug(INFO.format(
                                info=f'server.py: Client token is valid'))
                            users_set: set = set()
                            for user in message['users']:
                                users_set.add(user)
                            debug_verbose(f'server.py: Users to call: {users_set} , {self.__socket_echange.getpeername()[0]}')
                            users_ok: set = CallRequest(users_set, self.__socket_echange.getpeername()[0]).requests()
                            CallServer(users_ok).start()

                        else:
                            data = {'message': 'Token is invalid'}
                            self.send(f'10 {dumps(data)}')

                    
                    case '12': # 
                        db = Database('Retrieve contacts')
                        debug(INFO.format(info='Retrieve contacts'))
                        db.get_contact()

                    case '13': # 
                        db = Database('Add contact')
                        debug(INFO.format(info='Add contact'))
                        db.add_contact()

                    
                    case _:
                        pass
            else:
                debug(ERROR.format(error=f'server.py: Unknown code'))
                try:
                    self.send('00 Unknown code')
                except Exception as e:
                    debug(ERROR.format(
                        error=f'server.py: Failed to send termination message'))

        self.close()

    def close(self) -> None:
        """
            Arrêt du client

            :return: None
        """
        db = Database("Client logout")
        try:
            db.remove_client_ip(self.__socket_echange.getpeername()[0])
        except Exception as e:
            debug(ERROR.format(error=f'server.py: Failed to remove client IP'))
            debug_verbose(f'server.py: {e}')
        data: dict = {'message': 'Server closed'}
        self.send(f'00 {dumps(data)}')
        self.__socket_echange.close()
        debug(INFO.format(info=f'server.py: Client disconnected'))


class ClientManager:
    """
    Classe permettant de gérer les clients
    """

    def __init__(self) -> None:
        """
        Initialise le gestionnaire de client

        :return: None
        """
        self.__list_client: list = []

    def add_client(self, client_handler: ClientHandler) -> None:
        """
        Ajoute un client à la liste des clients

        :param client_handler: le client à ajouter

        :return: None
        """
        self.remove_dead_client()
        try:
            self.__list_client.append(client_handler)
            debug(INFO.format(info=f'server.py: New client added'))
        except Exception as e:
            debug(ERROR.format(error=f'server.py: Failed to add client'))
            debug_verbose(f'server.py: {e}')

    def get_number_client(self) -> int:
        """
        Retourne le nombre de client

        :return: le nombre de client
        """
        self.remove_dead_client()
        return len(self.__list_client)

    def remove_dead_client(self) -> None:
        """
        Supprime les clients morts

        :return: None
        """
        for client_handler in self.__list_client:
            if not client_handler.is_alive():
                self.__list_client.remove(client_handler)
                debug(INFO.format(info=f'server.py: Client removed'))

    def get_clients(self) -> list:
        """
        Retourne la liste des clients

        :return: la liste des clients
        """
        self.remove_dead_client()
        return self.__list_client

    def close(self) -> None:
        """
        Arrêt du gestionnaire de client

        :return: None
        """
        self.remove_dead_client()
        for client_handler in self.__list_client:
            client_handler.close()
        debug(INFO.format(info=f'server.py: Client manager closed'))


def stop_everything(listeningSocket: ListeningService, clientManager: ClientManager) -> None:
    """
    Arrêt du serveur

    :return: None
    """
    debug(INFO.format(info=f'server.py: Stopping server'))
    clientManager.close()
    debug_verbose(f'server.py: Client manager closed')
    listeningSocket.close()
    debug_verbose(f'server.py: Listening socket closed')
    debug(INFO.format(info=f'server.py: Server stopped'))
    # kill all threads
    KILL_ALL_THREAD = True
    token_handler.stop_timer()
    


# ========== Main ==========

