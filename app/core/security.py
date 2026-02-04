from cryptography.fernet import Fernet
from app.core.config import settings

# Defines a helper class for encryption and decryption using Fernet symmetric encryption.
# Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key.
class EncryptionHelper:
    # Initializes the EncryptionHelper with a key.
    # The key is used to create a Fernet instance, which handles the actual encryption/decryption.
    def __init__(self, key: str):
        self.fernet = Fernet(key.encode())

    # Encrypts a given string data.
    # The data is first encoded to bytes, then encrypted by Fernet, and finally decoded back to a string.
    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    # Decrypts a given encrypted string data.
    # The encrypted data is encoded to bytes, decrypted by Fernet, and then decoded back to a string.
    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()

# Creates a global instance of EncryptionHelper using the SECRET_KEY from application settings.
# This instance can be used throughout the application for consistent encryption/decryption.
encryption_helper = EncryptionHelper(settings.SECRET_KEY)