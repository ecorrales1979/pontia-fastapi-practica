from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

password_hash = PasswordHash([BcryptHasher()])


class SecurityUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera un hash seguro de la contraseña."""
        return password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña ingresada coincide con el hash almacenado."""
        return password_hash.verify(plain_password, hashed_password)
