import bcrypt
from dotenv import load_dotenv
import os
import pytest
from unittest.mock import Mock

from mtgapi import User
from tests import mock_dbm

load_dotenv()

@pytest.mark.parametrize('mock_dbm', ['users'], indirect = True)

def test_hash_password(mock_dbm, monkeypatch):
    user = User(mock_dbm)

    password = 'password'

    expected_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        os.environ.get('PASSWORD_SALT').encode('utf-8')
    )

    hashed = user.hash_password(password)

    assert hashed == expected_hash
