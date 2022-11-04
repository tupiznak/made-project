from database.connection import citations_db
from pymongo.database import Database

from .author import AuthorOperations
from .paper import PaperOperations

from .venue import VenueOperations


class Operations:

    def __init__(self, database: Database = citations_db):
        self.db = database
        self.author = AuthorOperations(self)
        self.paper = PaperOperations(self)
        self.venue = VenueOperations(self)
