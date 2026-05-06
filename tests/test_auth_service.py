import pytest
from app.core.security import verify_password, get_password_hash

def test_password_hashing():
    password = "superpassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_pass", hashed) is False