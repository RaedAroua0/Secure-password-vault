import json
import os
import getpass
import secrets
import string
from cryptography.fernet import Fernet

from auth import (
    setup_master_password,
    verify_master_password,
    derive_key,
    MASTER_HASH_FILE
)

from security import analyze_password


# =========================
# CONFIG
# =========================

DB_FILE = "data/vault.json"

# =========================
# MASTER PASSWORD SETUP
# =========================

if not os.path.exists(MASTER_HASH_FILE):
    master_password = setup_master_password()
else:
    master_password = verify_master_password()

# =========================
# CREATE ENCRYPTION KEY
# =========================

key = derive_key(master_password)
cipher = Fernet(key)

# =========================
# DATABASE SETUP
# =========================

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

# =========================
# FUNCTIONS
# =========================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_data():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def title():
    print("=" * 45)
    print("        SECURE PASSWORD VAULT")
    print("=" * 45)

# =========================
# PASSWORD GENERATOR
# =========================

def generate_password(length=16):
    characters = (string.ascii_letters + string.digits + "?!$%")

    password = "".join(secrets.choice(characters)for i in range(length))
    return password

# =========================
# ADD PASSWORD
# =========================

def add_password():
    clear()
    title()
    print("\n[ ADD NEW PASSWORD ]\n")

    site = input("Website : ")
    email = input("Email    : ")

    # SECTION PASSWORD 
    choice = input("\n Generate password ? (y/n) : ").lower()

    if choice == "y":
        password = generate_password()
        print(f"\n[+] Succesfully generated password : {password}")

    else:
        while True:
            password = getpass.getpass("Password : ")
            confirm_password = getpass.getpass("Confirm password : ")

            if password != confirm_password:
                print("\n[!] The passwords do not match.\n")
            elif len(password) < 4:
                print("\n[!] Password too short.\n")
            else:
                break

    encrypted_password = cipher.encrypt(password.encode()).decode()

    data = load_data()

    data.append({
        "site": site,
        "email": email,
        "password": encrypted_password
    })

    save_data(data)
    print("\n[+] Password securely saved.")
    input("\nPress ENTER to continue...")

# =========================
# SHOW PASSWORDS
# =========================

def show_passwords():
    clear()
    title()
    data = load_data()
    print("\n[ STORED PASSWORD ]\n")

    if not data:
        print("No password stored.\n")
        input("Press ENTER to continue...")
        return

    for i, entry in enumerate(data, start=1):
        decrypted_password = cipher.decrypt(entry["password"].encode()).decode()
        print(f"Entry #{i}")
        print("-" * 30)
        print(f"Website : {entry['site']}")
        print(f"Email    : {entry['email']}")
        print(f"Password : {decrypted_password}")
        print("-" * 30)

    input("\nPress ENTER to continue...")

def security_audit():
    clear()
    title()
    print("\n[ SECURITY AUDIT ]\n")

    password = getpass.getpass("Password to analyze : ")
    analysis = analyze_password(password)

    print("\n[ PASSWORD ANALYSIS ]\n")
    print(f"Score : {analysis['score']}/6")
    print(f"Strength : {analysis['label']}")
    print(f"Entropy : "f"{analysis['entropy']} bits")
    print(f"Estimated crack time : "f"{analysis['crack_time']}")

    input("\nPress ENTER to continue...")

# =========================
# MAIN LOOP
# =========================

while True:
    clear()
    title()

    print("\n1. Add Password")
    print("2. See Password")
    print("3. Security Audit")
    print("4. Quit")

    choice = input("\nChoice : ")

    if choice == "1":
        add_password()
    elif choice == "2":
        show_passwords()
    elif choice == "3":
        security_audit()
    elif choice == "4":
        clear()
        print("Goodbye !\n")
        break
    else:
        print("\n[!] Invalid choice.")
        input("\nPress ENTER to continue...")