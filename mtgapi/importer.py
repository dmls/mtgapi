from mtgsdk import Card
from pprint import pprint
from mtgapi.db_manager import DBManager

class Importer:
    def __init__(self, dbm):
        self.dbm = dbm

    def import_cards(self):
        cards = Card.all()
        for card in cards:
            data = vars(card)
            collection = self.dbm.db.cards
            result = collection.insert_one(data)
            pprint(result)

def main():
    dbm = DBManager()
    importer = Importer(dbm)
    importer.import_cards()

if __name__ == '__main__':
    main()
