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
        self.__connection: sqlite3.Connection
        self.__cursor: sqlite3.Cursor

        with open(DATABASE_USAGE_LOG, 'a') as f:
            # log l'utilisation de la base de données ainsi que la date et l'heure
            f.write(f'{self.__usage},{datetime.datetime.now()}\n')

    def connect(self) -> None:
        """
            Connecte la base de données
        """
        try:
            self.__connection = sqlite3.connect(self.__database)
            debug(f'Connected to database')
        except Exception as e:
            debug(f'Failed to connect to database')
            debug_verbose(e)
            exit(11)
        try:
            self.__cursor = self.__connection.cursor()
            debug(f'Created cursor')
        except Exception as e:
            debug(f'Failed to create cursor')
            debug_verbose(e)
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
        except Exception as e:
            debug(f'Failed to auth {login} with username')
            debug_verbose(e)
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
        except Exception as e:
            debug(f'Failed to auth {login} with mail')
            debug_verbose(e)
        return _return

db = Database('Test')
db.connect()
debug(db.auth_username('test', 'test'))