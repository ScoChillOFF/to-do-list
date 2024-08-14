from abc import ABC, abstractmethod

import bcrypt


class PasswordManager(ABC):
    @abstractmethod
    def is_password_matching_hash(self, raw_password: str, password_hash: str) -> bool:
        pass
    
    @abstractmethod
    def generate_password_hash(self, raw_password: str) -> str:
        pass


class PasswordManagerBcrypt(PasswordManager):
    def is_password_matching_hash(self, raw_password: str, password_hash: str) -> bool:
        raw_password_bytes = raw_password.encode("utf-8")
        password_hash_bytes = password_hash.encode("utf-8")
        return bcrypt.checkpw(raw_password_bytes, password_hash_bytes)

    def generate_password_hash(self, raw_password: str) -> str:
        raw_password_bytes = raw_password.encode("utf-8")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(raw_password_bytes, salt)
        return password_hash.decode("utf-8")
