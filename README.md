# Secure Password Vault
A local encrypted password manager written in Python. Stores and manages credentials securely using AES-based encryption and a master password system — no plaintext secrets ever touch disk.

---

## Features

- Secure password storage with AES encryption (Fernet)
- Master password authentication 
- PBKDF2 key derivation with SHA-256
- Password generator
- Password strength analysis
- Entropy calculation
- Estimated crack time analysis
- Local JSON database (fully offline)
- Clean terminal interface

---

## Technologies Used

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Encryption | Fernet (AES-128-CBC + HMAC-SHA256) |
| Key Derivation | PBKDF2HMAC + SHA-256 |
| Master Password Verification | SHA-256 hash |
| Storage | JSON |
| Dependencies | `cryptography` |

---

## Project Structure

```text
password-vault/
│
├── main.py           # Menu, password management, navigation
├── auth.py           # Master password, hashing, authentication, key derivation
├── security.py       # Strength analysis, entropy, crack time estimation
├── requirements.txt
├── README.md
│
└── data/
    ├── vault.json    # Encrypted vault entries
    └── master.hash   # SHA-256 hash of the master password
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/RaedAroua0/Secure-password-vault.git
cd Secure-password-vault
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** If you are using an older version of the `cryptography` library (< 3.x), `PBKDF2HMAC` requires an explicit `backend` argument. Add the following to `auth.py`:
> ```python
> from cryptography.hazmat.backends import default_backend
> # then pass backend=default_backend() to PBKDF2HMAC(...)
> ```

Run the application:

```bash
python main.py
```

---

## Usage

```text
=============================================
        SECURE PASSWORD VAULT
=============================================
1. Add Password
2. View Password
3. Security Audit
4. Quit
```

On first launch, you will be prompted to create a master password. This password is **never stored in plaintext** — only its SHA-256 hash is kept for verification. All vault entries are encrypted using a key derived from it via PBKDF2, which is computed at runtime and never written to disk.

---

## Security Details

### Master Password

- Verified against a **SHA-256 hash** stored in `data/master.hash`
- Never stored in plaintext
- **Note:** SHA-256 is a general-purpose hash function, not designed specifically for password hashing. A production system should use a dedicated algorithm such as **bcrypt** or **Argon2**, which are intentionally slow and resistant to brute-force attacks. This project uses SHA-256 for simplicity and educational purposes.

### Encryption

- Encryption key derived via **PBKDF2HMAC** (SHA-256, 100,000 iterations) from the master password
- Vault entries encrypted with **Fernet** (AES-128-CBC + HMAC-SHA256)
- Key is derived at runtime — never persisted to disk

### Password Security Analysis

The built-in auditor evaluates:

- Character set diversity (lowercase, uppercase, digits, symbols)
- Entropy (bits)
- Estimated brute-force crack time

---

## Disclaimer

This project is made for **educational and portfolio purposes**. It is **not** intended for production-level secret management.

Known limitations compared to production-grade solutions:
- Master password is verified with SHA-256 instead of bcrypt/Argon2
- Decrypted passwords are displayed in plaintext in the terminal
- No session timeout or clipboard auto-clear

For sensitive credentials, use a production-grade solution such as [Bitwarden](https://bitwarden.com), [1Password](https://1password.com), or [HashiCorp Vault](https://www.vaultproject.io).

---

## Author

Developed by **AROUA Raed** — [GitHub](https://github.com/RaedAroua0)
