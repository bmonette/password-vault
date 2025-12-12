import os
import json

from crypto_utils import derive_key, encrypt_data, decrypt_data
from models import Account


class Vault:
    """
    Handles loading, saving, encrypting, and decrypting the password vault.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.accounts = []  # List[Account]
        self.salt = None

    def create_new(self, master_password: str):
        """
        Create a brand new vault with a fresh salt.
        """

        self.salt = os.urandom(16)  # new salt
        key = derive_key(master_password, self.salt)

        # Start with an empty vault structure
        data = {"accounts": []}

        encrypted = encrypt_data(key, data)

        # Save format: salt + encrypted blob
        with open(self.filepath, "wb") as f:
            f.write(self.salt + encrypted)

        self.accounts = []

    def load(self, master_password: str):
        """
        Load and decrypt an existing vault.
        Raises ValueError if password is incorrect.
        """

        if not os.path.exists(self.filepath):
            raise FileNotFoundError("Vault file not found.")

        with open(self.filepath, "rb") as f:
            blob = f.read()

        # Extract salt (first 16 bytes)
        self.salt = blob[:16]
        encrypted = blob[16:]

        key = derive_key(master_password, self.salt)

        try:
            data = decrypt_data(key, encrypted)
        except Exception:
            raise ValueError("Incorrect master password.")

        # Convert dicts → Account objects
        self.accounts = [
            Account.from_dict(acc) for acc in data.get("accounts", [])
        ]

    def save(self, master_password: str):
        """
        Encrypt and save the current vault state.
        """

        key = derive_key(master_password, self.salt)

        # Convert Account objects → dicts
        data = {
            "accounts": [acc.to_dict() for acc in self.accounts]
        }

        encrypted = encrypt_data(key, data)

        with open(self.filepath, "wb") as f:
            f.write(self.salt + encrypted)

    def add_account(self, account: Account):
        self.accounts.append(account)

    def delete_account(self, index: int):
        del self.accounts[index]

    def update_account(self, index: int, updated: Account):
        self.accounts[index] = updated
