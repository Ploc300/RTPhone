# ===== Import =====
import dotenv, os

# ========== Constant ==========
dotenv.load_dotenv()
DEBUG_STATUS: bool = bool(os.getenv('DEBUG'))
DEBUG_VERBOSE_STATUS: bool = bool(os.getenv('DEBUG_VERBOSE'))
DEBUG: str = '\033[94m[DEBUG]\033[0m {debug}'
DEBUG_VERBOSE: str = '\033[94m[DEBUG VERBOSE]\033[0m {debug_verbose}'


# ========== Function ==========
def debug(msg: str) -> None:
    """
        Affiche un message de debug
    """
    if DEBUG_STATUS: print(f'{DEBUG.format(debug=msg)}')

def debug_verbose(msg: str) -> None:
    """
        Affiche un message de debug verbose
    """
    if DEBUG_VERBOSE_STATUS: print(f'{DEBUG_VERBOSE.format(debug_verbose=msg)}')

