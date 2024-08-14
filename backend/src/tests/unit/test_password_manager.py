import bcrypt

from app.services.utils.password_manager import PasswordManagerBcrypt


class TestIsPasswordMatchingHash:
    def test_successful(self):
        password_manager = PasswordManagerBcrypt()
        raw_password = "somepassw"
        password_hash = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        assert password_manager.is_password_matching_hash(raw_password, password_hash)

    def test_unsuccessful(self):
        password_manager = PasswordManagerBcrypt()
        password_hash = bcrypt.hashpw(b"somepassw", bcrypt.gensalt()).decode("utf-8")
        wrong_raw_password = "Somepassw"

        assert not password_manager.is_password_matching_hash(wrong_raw_password, password_hash)


class TestGeneratePasswordHash:
    def test_generate(self):
        password_manager = PasswordManagerBcrypt()
        password_hash_1 = password_manager.generate_password_hash("somepassw")
        password_hash_2 = password_manager.generate_password_hash("Somepassw")

        assert all([password_hash_1 != password_hash_2,
                    isinstance(password_hash_1, str),
                    isinstance(password_hash_2, str)])
