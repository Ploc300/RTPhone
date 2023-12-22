# ========== Import ==========
from debug import debug, debug_verbose
from db import Database
from json import loads, dumps
from authentification import check_token
from base64 import b64encode
from threading import Timer


# ========== Constant ==========

# ========== Color ==========
ERROR: str = '\033[91m[ERROR]\033[0m {error}'
WARNING: str = '\033[93m[WARNING]\033[0m {warning}'
SUCCESS: str = '\033[92m[SUCCESS]\033[0m {success}'
DEBUG: str = '\033[94m[DEBUG]\033[0m {debug}'
INFO: str = '\033[96m[INFO]\033[0m {info}'



# ========== Function ==========
def delete_outdated_token() -> None:
    """
        Supprime les tokens expirés
    """
    db = Database('Outdated Token')
    tokens = db.retrieve_all_tokens()
    for token in tokens:
        check_token(b64encode(token[0]))



# ========== Class ==========
# a class that repeat a function every x seconds
class RepeatedTimer(object):
    """
        Répète une fonction toutes les x secondes
    """
    def __init__(self, interval, function, *args, **kwargs):
        """
            Initialise la classe

            :param interval: l'intervalle de temps entre chaque répétition
            :param function: la fonction à répéter
            :param args: les arguments de la fonction
            :param kwargs: les arguments de la fonction
        """
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running: bool = False
        self.start()

    def _run(self) -> None:
        """
            Lance la fonction
        """
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self) -> None:
        """
            Lance le timer
        """
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self) -> None:
        """
            Arrête le timer
        """
        self._timer.cancel()
        self.is_running = False
        


# ========== Main ==========
RepeatedTimer(60, delete_outdated_token)