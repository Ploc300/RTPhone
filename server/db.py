# ===== Import =====
import dotenv, os, sqlite3
from server import debug

# ========== Constant ==========
DATABASE: str = os.getenv('DATABASE')
DEBUG: bool = bool(os.getenv('DEBUG'))

# ========== Classes ==========
class Database:
    def __init__(self) -> bool:
        """
            Initialise la base de données
        """
        self.__database: str = DATABASE
        self.__con: sqlite3.Connection
        self.__cur: sqlite3.Cursor
        self.connect()

    def connect(self) -> None:
        """
            Connecte la base de données
        """
        try:
            self.__con = sqlite3.connect(self.__database)
        except Exception as e:
            debug(f'Failed to connect to database')
            exit(11)
        try:
            self.__cur = self.__con.cursor()
        except Exception as e:
            debug(f'Failed to create cursor')
            exit(12)

    def auth_username(login: str, password: str) -> bool:
        """
            Authentifie un utilisateur avec son username et son mot de passe

            :param login: le login de l'utilisateur
            :param password: le mot de passe de l'utilisateur
            :return: True si l'utilisateur est authentifié, False sinon
        """
        _return: bool = False
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE username="{login}" AND password="{password}"')
            _return = True if self.__cur.fetchone() else False
        except Exception as e:
            debug(f'Failed to auth {login} with username')
        return _return
        

