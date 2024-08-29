import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_dbm(request):
    dbm = Mock()
    dbm.db = Mock()
    setattr(dbm.db, request.param, Mock())
    return dbm
