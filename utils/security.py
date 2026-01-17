# Password hashing using PBKDF2 (no external native deps). Returns hex strings.
import hashlib
import os
import binascii
from typing import Tuple

ITERATIONS = 200_000
SALT_BYTES = 16
HASH_NAME = "sha256"


def _derive(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, ITERATIONS, dklen=32)


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    dk = _derive(password, salt)
    return f"{binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"


def verify_password(stored: str, password: str) -> bool:
    try:
        salt_hex, dk_hex = stored.split("$")
        salt = binascii.unhexlify(salt_hex)
        expected = binascii.unhexlify(dk_hex)
        test = _derive(password, salt)
        return hashlib.compare_digest(test, expected)
    except Exception:
        return False