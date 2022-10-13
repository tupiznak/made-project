import mongoengine.errors
import pytest
from datetime import datetime

import database.connection
from database.models.author import Author, HistoryObject
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


def test_like(author_operations):
    author = Author(_id='qwertyu', name='gtrgdtg', org='grtgrt', oid='123')
    author_operations.create(author)
    paper_id_1 = 'qwerty'
    paper_id_2 = 'zxc'
    author_operations.like(paper_id_1, author.id)
    time_like_1 = datetime.now().timestamp()
    author_operations.like(paper_id_2, author.id)
    time_like_2 = datetime.now().timestamp()
    history = [HistoryObject(event='like', time=time_like_1, description=paper_id_1),
               HistoryObject(event='like', time=time_like_2, description=paper_id_2)]
    ao_likes = author_operations.get_liked_papers(author.id)
    ao_hist = author_operations.get_history(author.id)
    assert ao_likes == [paper_id_1, paper_id_2]
    assert [ao_hist[0].event, ao_hist[1].event] == [history[0].event, history[0].event]
    assert [ao_hist[0].description, ao_hist[1].description] == [history[0].description, history[1].description]
    assert history[0].time - ao_hist[0].time <= 1
    assert history[1].time - ao_hist[1].time <= 1
