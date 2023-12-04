# ===== Import =====
import dotenv, os, sqlite3
from server import debug

# ========== Constant ==========
dotenv.load_dotenv()
DATABASE: str = os.getenv('DATABASE')
DEBUG: bool = bool(os.getenv('DEBUG'))

# ========== Classes ==========
class Database:
    def __init__(self):
        """
            Initialise la base de données
        """
        self.__database: str = DATABASE
        self.__con: sqlite3.Connection
        self.__cur: sqlite3.Cursor

    def connect(self) -> None:
        """
            Connecte la base de données
        """
        try:
            self.__con = sqlite3.connect(self.__database)
        except Exception as e:

            
            self.__cur = self.__con.cursor()

