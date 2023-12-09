# ===== Import =====self.__cursor
import dotenv, os, sqlite3, datetime
from debug import debug, debug_verbose

# ========== Constant ==========
dotenv.load_dotenv()
DATABASE: str = os.getenv('DATABASE')
DATABASE_USAGE_LOG: str = os.getenv('DATABASE_USAGE_LOG')

# ========== Classes ==========
class Database:
    def __init__(self, usage: str) -> bool:
        """
            Initialise la base de données et log l'utilisation
        """
        self.__database: str = DATABASE
        self.__usage: str = usage
        self.__connection: sqlite3.Connection = None
        self.__cursor: sqlite3.Cursor = None
        debug(f'db.py: Created database for: {usage}')

        try:
            with open(DATABASE_USAGE_LOG, 'a') as f:
                # log l'utilisation de la base de données ainsi que la date et l'heure
                f.write(f'{self.__usage},{datetime.datetime.now()}\n')
                debug(f'db.py: Logged database usage')
        except Exception as e:
            debug(f'db.py: Failed to log database usage')
            debug_verbose(f'db.py: {e}')
            exit(-1)
        self.connect()

    def connect(self) -> None:
        """
            Connecte la base de données
        """
        try:
            self.__connection = sqlite3.connect(self.__database)
            debug(f'db.py: Connected to database')
        except Exception as e:
            debug(f'db.py: Failed to connect to database')
            debug_verbose(f'db.py: {e}')
            exit(11)
        try:
            self.__cursor = self.__connection.cursor()
            debug(f'db.py: Created cursor')
        except Exception as e:
            debug(f'db.py: Failed to create cursor')
            debug_verbose(f'db.py: {e}')
            exit(12)

    def auth_username(self, login: str, password: str) -> bool:
        """
            Authentifie un utilisateur avec son username et son mot de passe

            :param login: le login de l'utilisateur
            :param password: le mot de passe de l'utilisateur
            :return: True si l'utilisateur est authentifié, False sinon
        """
        _return: bool = False
        try:
            self.__cursor.execute(f'SELECT * FROM users WHERE name="{login}" AND password="{password}"')
            _return = True if self.__cursor.fetchone() else False
            debug(f'db.py: Auth {login} with username')
        except Exception as e:
            debug(f'db.py: Failed to auth {login} with username')
            debug_verbose(f'db.py: {e}')
        return _return

    def auth_mail(self, login: str, password: str) -> bool:
        """
            Authentifie un utilisateur avec son mail et son mot de passe

            :param login: le login de l'utilisateur
            :param password: le mot de passe de l'utilisateur
            :return: True si l'utilisateur est authentifié, False sinon
        """
        _return: bool = False
        try:
            self.__cursor.execute(f'SELECT * FROM users WHERE email="{login}" AND password="{password}"')
            _return = True if self.__cursor.fetchone() else False
            debug(f'db.py: Auth {login} with mail')
        except Exception as e:
            debug(f'db.py: Failed to auth {login} with mail')
            debug_verbose(f'db.py: {e}')
        return _return
    
    def add_token(self, token: bytes, tag: bytes, nonce: bytes) -> bool:
        _return: bool = False
        try:
            self.__cursor.execute('INSERT INTO tokens VALUES (?, ?, ?)', (token, tag, nonce))
            debug(f'db.py: Added token')
            try:
                self.__connection.commit()
                debug(f'db.py: Committed token')
                _return = True
            except Exception as e:
                debug(f'db.py: Failed to commit token')
                debug_verbose(f'db.py: {e}')
        except Exception as e:
            debug(f'db.py: Failed to add token')
            debug_verbose(f'db.py: {e}')
        return _return
    
    def retrieve_token(self, token: bytes) -> (bool, tuple):
        _return: bool = False
        try:
            self.__cursor.execute('SELECT * FROM tokens WHERE token=?', (token,))
            result = self.__cursor.fetchone()
            debug(f'db.py: Retrieved token')
        except Exception as e:
            debug(f'db.py: Failed to retrieve token')
            debug_verbose(f'db.py: {e}')
        return result
    
    def remove_token(self, token: bytes) -> bool:
        _return: bool = False
        try:
            self.__cursor.execute('DELETE FROM tokens WHERE token=?', (token,))
            debug(f'db.py: Removed token')
            try:
                self.__connection.commit()
                debug(f'db.py: Committed token')
                _return = True
            except Exception as e:
                debug(f'db.py: Failed to commit token')
                debug_verbose(f'db.py: {e}')
        except Exception as e:
            debug(f'db.py: Failed to remove token')
            debug_verbose(f'db.py: {e}')
        return _return
    
    def get_phone_number(self, username: str) -> str:
        _return: str = ''
        try:
            self.__cursor.execute('SELECT phone FROM users WHERE name=?', (username,))
            _return = self.__cursor.fetchone()[0]
            debug(f'db.py: Got phone number')
        except Exception as e:
            debug(f'db.py: Failed to get phone number')
            debug_verbose(f'db.py: {e}')
        return _return
        