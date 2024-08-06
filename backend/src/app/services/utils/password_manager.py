from abc import ABC, abstractmethod


class PasswordManager(ABC):
    @abstractmethod
    def is_password_matching_hash(raw_password: str, password_hash: str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def generate_password_hash(raw_password: str) -> str:
        raise NotImplementedError