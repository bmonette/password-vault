from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import os
import json


def derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    """
    Derive a 256-bit key from the master password using PBKDF2.
    """

    password_bytes = password.encode('utf-8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits key
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )

    return kdf.derive(password_bytes)


def encrypt_data(key: bytes, data: dict) -> bytes:
    """
    Encrypts a Python dictionary using AES-256-GCM.
    Returns: nonce + tag + ciphertext
    """

    json_data = json.dumps(data).encode('utf-8')

    # Generate a random 12-byte nonce
    nonce = os.urandom(12)

    # Create AES-GCM cipher
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    ciphertext = encryptor.update(json_data) + encryptor.finalize()

    # Return nonce + tag + ciphertext
    return nonce + encryptor.tag + ciphertext


def decrypt_data(key: bytes, blob: bytes) -> dict:
    """
    Decrypts AES-256-GCM data roduced by encrypt_data().
    Blob format: nonce (12 bytes) + tag (16 bytes) + ciphertext
    """

    nonce = blob[:12]
    tag = blob[12:28]
    ciphertext = blob[28:]

    # Create AES-GCM cipher
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    json_data = decryptor.update(ciphertext) + decryptor.finalize()

    return json.loads(json_data.decode('utf-8'))
