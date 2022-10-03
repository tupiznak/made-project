import mongoengine.errors
import pytest

import database.connection
from database.models.author import Author
from database.operations.author import AuthorOperations


@pytest.fixture
def author_operations():
    database.connection.disconnect_database('citations')
    database.connection.client, database.connection.citations_db = \
        database.connection.new_connection(db_name='citations_test', alias='citations')
    author_operations = AuthorOperations(database.connection.citations_db)
    author_operations.flush()
    return author_operations


@pytest.fixture
def some_data(author_operations):
    a1 = author_operations.create(Author(_id='q', name='gtrgdtg', org='grtgrt'))
    a2 = author_operations.create(Author(_id='q2', name='gtrgdtg', org='xa', gid='sdaf', oid='123'))
    a3 = author_operations.create(Author(_id='q22', name='gtrgdtg', org='grtgrt', oid='123'))
    a4 = author_operations.create(Author(_id='222', name='gg', org='wer', gid='sdaf', oid='32'))
    return a1, a2, a3, a4


def test_crud(author_operations):
    author = Author(_id='q', name='gtrgdtg', org='grtgrt', oid='123')
    author_operations.model_to_db(author_operations.to_model(author_operations.model_to_db(author)))

    author_operations.create(author)
    with pytest.raises(mongoengine.errors.NotUniqueError):
        author_operations.create(author)
    assert author_operations.get_by_id(_id=author.id) == author

    author.org = 'ewwe'
    author_operations.full_update(author)

    author.name = 'ww'
    author_operations.change_name(_id=author.id, name=author.name)
    assert author_operations.get_by_id(author.id) == author

    with pytest.raises(mongoengine.errors.DoesNotExist):
        author_operations.change_name(_id='3242ewr', name='ewsf')

    author_operations.delete(author.id)
    with pytest.raises(mongoengine.errors.DoesNotExist):
        author_operations.delete(author.id)


def test_chunk(author_operations, some_data):
    a1, a2, a3, a4 = some_data
    assert len(author_operations.get_chunk(chunk_size=2)) == 2
    assert len(author_operations.get_chunk(chunk_size=20)) == 4
    assert author_operations.get_chunk(id_list=['q22', 'q']) == [a3, a1]
    with pytest.raises(mongoengine.errors.DoesNotExist):
        assert author_operations.get_chunk(id_list=['q22', 'qer']) == [a3, a1]


def test_filter(author_operations, some_data):
    assert author_operations.filter(dict(name='gg')) == [some_data[3]]
    assert set(author_operations.filter(dict(gid='sdaf'))) == {some_data[1], some_data[3]}
    assert set(author_operations.filter(dict(gid='sdaf'))) == {some_data[1], some_data[3]}
    assert author_operations.filter(dict(gid='sdaf', name='gg')) == [some_data[3]]
    assert author_operations.filter(dict(gid='sdaf'), exclude_author=dict(name='gg')) == [some_data[1]]



def test_count(author_operations, some_data):
    assert author_operations.total_size() == 4


def test_authors_by_org(author_operations, some_data):
    assert set(author_operations.get_authors_by_org(org_id='grtgrt', chunk_size=10)) == \
           {some_data[0], some_data[2]}
