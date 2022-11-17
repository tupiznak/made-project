import mongoengine.errors
import pytest

from database.models.venue import Venue


def test_crud(venue_operations):
    venue = Venue(_id='q', name_d='gtrgdtg', raw='grtgrt', type=123)
    venue_operations.model_to_db(venue_operations.to_model(venue_operations.model_to_db(venue)))

    venue_operations.create(venue)
    with pytest.raises(mongoengine.errors.NotUniqueError):
        venue_operations.create(venue)
    assert venue_operations.get_by_id(_id=venue.id) == venue

    venue.raw = 'ewwe'
    venue_operations.full_update(venue)

    venue.name_d = 'ww'
    venue_operations.change_name_d(_id=venue.id, name_d=venue.name_d)
    assert venue_operations.get_by_id(venue.id) == venue

    with pytest.raises(mongoengine.errors.DoesNotExist):
        venue_operations.change_name_d(_id='3242ewr', name_d='ewsf')

    venue_operations.delete(venue.id)
    with pytest.raises(mongoengine.errors.DoesNotExist):
        venue_operations.delete(venue.id)


def test_chunk(venue_operations, some_venue_data):
    v1, v2, v3, v4 = some_venue_data
    assert len(venue_operations.get_chunk(chunk_size=2)) == 2
    assert len(venue_operations.get_chunk(chunk_size=20)) == 4
    assert venue_operations.get_chunk(id_list=['q22', 'q']) == [v3, v1]
    with pytest.raises(mongoengine.errors.DoesNotExist):
        assert venue_operations.get_chunk(id_list=['q22', 'qer']) == [v3, v1]


def test_filter(venue_operations, some_venue_data):
    assert venue_operations.filter(dict(name_d='gg')) == [some_venue_data[3]]
    assert set(venue_operations.filter(dict(type=123))) == {some_venue_data[1], some_venue_data[2]}
    assert set(venue_operations.filter(dict(type=123))) == {some_venue_data[1], some_venue_data[2]}
    assert venue_operations.filter(dict(type=123, raw='xa')) == [some_venue_data[1]]
    assert venue_operations.filter(dict(type=123), exclude_venue=dict(raw='grtgrt kjfwe ewr')) == [some_venue_data[1]]


def test_count(venue_operations, some_venue_data):
    assert venue_operations.total_size() == 4


def test_venues_by_type(venue_operations, some_venue_data):
    assert set(venue_operations.get_venues_by_type(type_id=123, chunk_size=10)) == \
           {some_venue_data[2], some_venue_data[1]}
