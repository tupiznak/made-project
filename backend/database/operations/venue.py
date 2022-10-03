from typing import List, Union

import database.db_objects.venue as db
from database.models.venue import *
from database.connection import citations_db
# from mongoengine import QuerySet
from pymongo.database import Database


class VenueOperations:

    def __init__(self, database: Database = citations_db):
        self.db = database

    @property
    def collection(self):
        return self.db['venue']

    def flush(self):
        self.db.drop_collection('venue')

    def to_model(self, db_venue: Union[db.Venue, dict]) -> Venue:
        if isinstance(db_venue, db.Venue):
            return Venue.parse_raw(db_venue.to_json())
        else:
            return Venue.parse_obj(db_venue)

    def replace_id(self, venue: dict):
        venue['_id'] = venue['id']
        del venue['id']
        return venue

    def model_to_db(self, venue: Venue) -> db.Venue:
        return db.Venue(**venue.dict(by_alias=True))

    def create(self, venue: Venue) -> Venue:
        db_venue = self.model_to_db(venue)
        db_venue.save(force_insert=True)
        return venue

    def find(self, _id: str) -> db.Venue:
        return db.Venue.objects.get(_id=_id)

    def get_by_id(self, _id: str) -> Venue:
        db_venue = self.find(_id)
        venue = self.to_model(db_venue)
        return venue

    def full_update(self, venue: Venue) -> Venue:
        db_venue = self.model_to_db(venue)
        db_venue.save()
        return self.to_model(db_venue)

    def change_name_d(self, _id: str, name_d: str) -> Venue:
        db_venue = self.find(_id)
        db_venue.name_d = name_d
        db_venue.save()
        return self.to_model(db_venue)

    def get_chunk(self, id_list: List[str] = None, chunk_size: int = 10) -> List[Venue]:
        if id_list is None:
            cmd = db.Venue.objects.aggregate([{'$sample': {'size': chunk_size}}])
            db_objects = [c for c in cmd]
            venues = [self.to_model(p) for p in db_objects]
        else:
            venues = []
            for i in id_list:
                venues.append(self.get_by_id(i))
        return venues

    def delete(self, _id: str):
        venue = self.get_by_id(_id)
        self.collection.delete_one(dict(_id=venue.id))

    def filter(self, venue_filter: dict, exclude_venue: dict = None, chunk_size: int = 10) -> List[Venue]:
        if exclude_venue is None:
            exclude_venue = {}
        exclude_venue = dict((f'{k}__ne', v) for k, v in exclude_venue.items())
        cmd = db.Venue.objects.filter(**(venue_filter | exclude_venue)) \
            .aggregate([{'$sample': {'size': chunk_size}}])
        db_objects = [c for c in cmd]
        venues = [self.to_model(p) for p in db_objects]
        return venues

    def total_size(self):
        return self.collection.estimated_document_count()

    def get_venues_by_type(self, type_id: int, chunk_size: int = 10) -> List[Venue]:
        query = self.collection.aggregate([
            {
                '$match': {
                    'type': type_id
                }
            },
            {
                '$sample': {
                    'size': chunk_size
                }
            }
        ])
        db_objects = [o for o in query]
        venues = [self.to_model(p) for p in db_objects]
        return venues


if __name__ == '__main__':
    pass
