from cryptography.fernet import Fernet
from app.core.config import settings


class EncryptionHelper:
    def __init__(self, key: str):
        self.fernet = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()


encryption_helper = EncryptionHelper(settings.SECRET_KEY)
