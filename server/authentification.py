# ===== Import =====
from db import Database
from debug import debug
import time, dotenv, os, json
from Cryptodome.Cipher import AES

# ========== Constant ==========
dotenv.load_dotenv()
BANNED_CHAR: list = [';', ':', '!', '?', ',', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '`', '~', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=', ' ']
ENCRYPTION_KEY: str = str(os.getenv('ENCRYPTION_KEY'))

# ========== Function ==========
def auth(login: str, password: str) -> bool:
    """
        Authentifie un utilisateur avec son login et son mot de passe

        :param login: le login de l'utilisateur
        :param password: le mot de passe de l'utilisateur

        :return: True si l'utilisateur est authentifié, False sinon
    """
    db = Database('Authentification')
    _return: bool = False
    if len(login) > 3 or len(password) > 3: # Vérification de la taille du login et du mot de passe
        if not any([char in BANNED_CHAR for char in login]) or not any([char in BANNED_CHAR for char in password]): # Vérification des caractères interdits
            if '@' in login:
                try: # Authentification avec le mail
                    _return = db.auth_mail(login, password)
                except Exception as e:
                    debug(f'Failed to auth {login} with mail')
            else:
                try: # Authentification avec le username
                    _return = db.auth_username(login, password)
                except Exception as e:
                    debug(f'Failed to auth {login} with username')
    return _return

def generate_token(login: str, password: str) -> bytes:
    token = {
        'login': login,
        'password': password,
        'time_limit': time.time() + 3600
    }
    token_bytes: bytes = json.dumps(token).encode('utf-8')
    
    key = ENCRYPTION_KEY.encode('utf-8')
    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(token_bytes)

    db = Database("Token Creation")
    db.connect()
    db.add_token(ciphertext, tag, nonce)
    return ciphertext

# def check_token(token: bytes) -> bool:
#     key = ENCRYPTION_KEY.encode('utf-8')
#     cipher = AES.new(key, AES.MODE_EAX)

#     plaintext = cipher.decrypt(token)

#     try:
#         cipher.verify()
#         print("authentic:", plaintext)
#     except:
#         print('not authentic')


# ========== Main ==========
if __name__ == '__main__':
    generated_token = generate_token('test', 'test')