import pytest
from unittest.mock import Mock

from mtgapi import Importer, sample_card

@pytest.fixture
def mock_dbm():
    dbm = Mock()
    dbm.db = Mock()
    dbm.db.cards = Mock()

    return dbm

def test_import_cards(mock_dbm, monkeypatch):
    importer = Importer(mock_dbm)

    # Simulate Card.all() returning a list of mock cards.
    sample_cards = [sample_card]
    monkeypatch.setattr(
        'mtgapi.importer.Card',
        Mock(all = Mock(return_value = sample_cards))
    )
    importer.dbm.Card.all = Mock(return_value = sample_cards)

    importer.import_cards()

    for card in sample_cards:
        mock_dbm.db.cards.insert_one.assert_called_once_with(vars(card))
