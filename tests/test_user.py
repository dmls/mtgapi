import bcrypt
from dotenv import load_dotenv
import os
import pytest
from unittest.mock import Mock

from mtgapi import User
from tests import mock_dbm

load_dotenv()

@pytest.mark.parametrize('mock_dbm', ['users'], indirect = True)
class TestUser:
    def get_password_hash(self, password):
        return bcrypt.hashpw(
            password.encode('utf-8'),
            os.environ.get('PASSWORD_SALT').encode('utf-8')
        )

    def test_hash_password(self, mock_dbm):
        user = User(mock_dbm)

        password = 'password'
        expected_hash = self.get_password_hash(password)
        hashed = user.hash_password(password)

        assert hashed == expected_hash

    def test_validate_password(self, mock_dbm, monkeypatch):
        user = User(mock_dbm)

        email = 'user@example.com'
        password = 'password'
        expected_hash = self.get_password_hash(password).decode('utf-8')

        monkeypatch.setattr(user, 'get_user', (
            lambda email: {'email': email, 'password': expected_hash}
        ))

        monkeypatch.setattr(user, 'hash_password', (
            lambda pwd: expected_hash if pwd == password else 'wrong_hash'
        ))

        assert user.validate_password(email, password) is True
        assert user.validate_password(email, 'wrong_password') is False

        monkeypatch.setattr(user, 'get_user', lambda email: None)
        assert user.validate_password(email, password) is False
