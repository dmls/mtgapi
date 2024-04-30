from mtgsdk import Card
from pprint import pprint
from db import DB

class Importer:
    def __init__(self, db):
        self.db = db

    def import_cards(self):
        cards = Card.all()
        for card in cards:
            data = vars(card)
            collection = self.db.db.cards
            result = collection.insert_one(data)
            pprint(result)

def main():
    db = DB()
    importer = Importer(db)
    importer.import_cards()

if __name__ == '__main__':
    main()
