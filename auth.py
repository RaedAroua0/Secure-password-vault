import os
import hashlib
import getpass
import base64
import time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

DATA_FOLDER = "data"
MASTER_HASH_FILE = "data/master.hash"

# =========================
# SETUP DATA FOLDER
# =========================

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# =========================
# HASH PASSWORD
# =========================

def hash_master_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# CREATE MASTER PASSWORD
# =========================

def setup_master_password():
    print("\n[ MASTER PASSWORD CONFIGURATION ]\n")

    while True:
        password = getpass.getpass("Create master password : ")
        confirm = getpass.getpass("Confirm : ")

        if password != confirm:
            print("\n[!] The passwords do not match.\n")
        elif len(password) < 8:
            print("\n[!] Minimum 8 characters.\n")
        else:
            break

    hashed = hash_master_password(password)

    with open(MASTER_HASH_FILE, "w") as f:
        f.write(hashed)

    return password

# =========================
# VERIFY MASTER PASSWORD
# =========================

def verify_master_password():
    print("\n[ LOGIN ]\n")

    with open(MASTER_HASH_FILE, "r") as f:
        stored_hash = f.read()

    while True:
        password = getpass.getpass("Master password : ")
        hashed = hash_master_password(password)

        if hashed == stored_hash:
            print("\n[+] Welcome.\n")
            time.sleep(1.5)
            return password
        else:
            print("\n[!] Bad password.\n")

# =========================
# DERIVE ENCRYPTION KEY
# =========================

def derive_key(master_password):
    password_bytes = master_password.encode()

    salt = b"fixed_salt_for_demo"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key