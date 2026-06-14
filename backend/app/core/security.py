import base64
import binascii
import hashlib
import hmac
import json
import os
import secrets
import time


PASSWORD_ITERATIONS = 210_000
TOKEN_TTL_SECONDS = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "28800"))
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-in-production")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), PASSWORD_ITERATIONS
    )
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt}${digest.hex()}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected = encoded_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt), int(iterations)
        )
        return hmac.compare_digest(digest.hex(), expected)
    except (TypeError, ValueError):
        return False


def _encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def create_access_token(user_id: int, username: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }
    encoded_payload = _encode(json.dumps(payload, separators=(",", ":")).encode())
    signature = hmac.new(
        SECRET_KEY.encode(), encoded_payload.encode(), hashlib.sha256
    ).digest()
    return f"{encoded_payload}.{_encode(signature)}"


def decode_access_token(token: str) -> dict | None:
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
        expected_signature = hmac.new(
            SECRET_KEY.encode(), encoded_payload.encode(), hashlib.sha256
        ).digest()
        if not hmac.compare_digest(expected_signature, _decode(encoded_signature)):
            return None
        payload = json.loads(_decode(encoded_payload))
        if int(payload["exp"]) < int(time.time()):
            return None
        return payload
    except (
        binascii.Error,
        KeyError,
        TypeError,
        UnicodeDecodeError,
        ValueError,
        json.JSONDecodeError,
    ):
        return None
