from abc import ABC, abstractmethod


class PasswordManager(ABC):
    @abstractmethod
    def is_password_matching_hash(self, raw_password: str, password_hash: str) -> bool:
        pass
    
    @abstractmethod
    def generate_password_hash(self, raw_password: str) -> str:
        pass
