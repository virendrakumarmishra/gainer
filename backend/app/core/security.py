import secrets
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


class Security:
    def __init__(self):
        self.hasher = PasswordHash((Argon2Hasher(),))

    # --- Password Hashing & Verification ---
    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.hasher.verify(plain_password, hashed_password)

    # --- Session Token Generator ---
    def generate_session_id(self) -> str:
        return secrets.token_urlsafe(48)


# Global singleton instance
security = Security()