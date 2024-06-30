import bcrypt
from dotenv import load_dotenv
import os
import pytest
from unittest.mock import Mock, MagicMock

from mtgapi import User
from tests import mock_dbm

load_dotenv()

@pytest.mark.parametrize('mock_dbm', ['users'], indirect = True)
class TestUser:
    @pytest.fixture(autouse = True)
    def setup(self, mock_dbm):
        self.email = 'user@example.com'
        self.password = 'password'

        user = User(mock_dbm)
        self.expected_password_hash = user.hash_password(self.password).decode('utf-8')

    def get_password_hash(self, password):
        return bcrypt.hashpw(
            password.encode('utf-8'),
            os.environ.get('PASSWORD_SALT').encode('utf-8')
        )

    def test_hash_password(self, mock_dbm):
        user = User(mock_dbm)
        hashed = user.hash_password(self.password)

        assert hashed.decode('utf-8') == self.expected_password_hash

    def test_validate_password(self, mock_dbm, monkeypatch):
        user = User(mock_dbm)

        monkeypatch.setattr(user, 'get_user', (
            lambda email: {'email': email, 'password': self.expected_password_hash}
        ))

        monkeypatch.setattr(user, 'hash_password', (
            lambda pwd: self.expected_password_hash if pwd == self.password else 'wrong_hash'
        ))

        assert user.validate_password(self.email, self.password) is True
        assert user.validate_password(self.email, 'wrong_password') is False

        monkeypatch.setattr(user, 'get_user', lambda email: None)
        assert user.validate_password(self.email, self.password) is False

    def test_create(self, mock_dbm, monkeypatch):
        user = User(mock_dbm)
        collection = MagicMock()
        monkeypatch.setattr(user.dbm.db, 'users', collection)

        # Test valid email & password
        monkeypatch.setattr(user, 'get_user', lambda email: None)

        result = user.create(self.email, self.password)
        collection.insert_one.assert_called_once_with({
            'email': self.email,
            'password': user.hash_password('password')
        })

        assert result == collection.insert_one.return_value
