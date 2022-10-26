import mongoengine.errors
import pytest

import database.connection
from database.models.author import Author
from database.operations.author import AuthorOperations
# for h-index testing
from database.models.paper import Paper
from database.operations.paper import PaperOperations
from database.test.test_paper_operations import paper_operations

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
    # OLD DATA
    # a1 = author_operations.create(Author(_id='q', name='gtrgdtg', org='grtgrt'))  # this
    # a2 = author_operations.create(Author(_id='q2', name='gtrgdtg', org='xa', gid='sdaf', oid='123'))
    # a3 = author_operations.create(Author(_id='q22', name='gtrgdtg', org='grtgrt', oid='123'))
    # a4 = author_operations.create(Author(_id='222', name='gg', org='wer', gid='sdaf', oid='32'))
    a1 = author_operations.create(Author(_id='id1', name='Nikolay Lobachevsky', 
                                         org='Lebedev Physical Institute', papers=['pid4']))  # Kazan
    a2 = author_operations.create(Author(_id='id2', name='Pafnuty Chebyshev', 
                                         org='St Petersburg University',
                                         gid='gid2', oid='123', papers=['pid3']))
    a3 = author_operations.create(Author(_id='id3', name='Pavel Cherenkov',
                                         org='Lebedev Physical Institute',
                                         oid='123'))
    a4 = author_operations.create(Author(_id='id4', name='Nikolay Zhukovsky', 
                                         org='Moscow State University', 
                                         gid='gid2', oid='32', papers=['pid1', 'pid2']))
    return a1, a2, a3, a4


@pytest.fixture
def some_papers_data(paper_operations):  # papers data for h-index test
    p1 = paper_operations.create(Paper(_id='pid1', title='title1',
                                       n_citation=13))
    p2 = paper_operations.create(Paper(_id='pid2', title='title2',
                                       year=1960, n_citation = 520))
    p3 = paper_operations.create(Paper(_id='pid3', title='title3'))
    p4 = paper_operations.create(Paper(_id='pid4', title='title4',
                                       year=1952, n_citation = None))
    return p1, p2, p3, p4


def test_crud(author_operations):
    author = Author(_id='id1', name='Nikolai Lobachevsky',
                    org='Moscow State University', oid='123')
    author_operations.model_to_db(author_operations.to_model(author_operations.model_to_db(author)))

    author_operations.create(author)
    with pytest.raises(mongoengine.errors.NotUniqueError):
        author_operations.create(author)
    assert author_operations.get_by_id(_id=author.id) == author

    author.org = 'St Petersburg University'
    author_operations.full_update(author)

    author.name = 'Nikolay Lobachevsky'
    author_operations.change_name(_id=author.id, name=author.name)
    assert author_operations.get_by_id(author.id) == author

    with pytest.raises(mongoengine.errors.DoesNotExist):
        author_operations.change_name(_id='id50', name='Alexander Mozhaysky')

    author_operations.delete(author.id)
    with pytest.raises(mongoengine.errors.DoesNotExist):
        author_operations.delete(author.id)


def test_chunk(author_operations, some_data):
    a1, a2, a3, a4 = some_data
    assert len(author_operations.get_chunk(chunk_size=2)) == 2
    assert len(author_operations.get_chunk(chunk_size=20)) == 4
    assert author_operations.get_chunk(id_list=['id3', 'id1']) == [a3, a1]
    with pytest.raises(mongoengine.errors.DoesNotExist):
        assert author_operations.get_chunk(id_list=['id3', 'id50']) == [a3, a1]


def test_filter(author_operations, some_data):
    assert author_operations.filter(dict(name='Nikolay Zhukovsky')) == [some_data[3]]
    assert set(author_operations.filter(dict(gid='gid2'))) == {some_data[1], some_data[3]}
    # assert set(author_operations.filter(dict(gid='sdaf'))) == {some_data[1], some_data[3]}
    assert author_operations.filter(dict(gid='gid2', name='Nikolay Zhukovsky')) == [some_data[3]]
    assert author_operations.filter(dict(gid='gid2'), exclude_author=dict(name='Nikolay Zhukovsky')) == [some_data[1]]


def test_count(author_operations, some_data):
    assert author_operations.total_size() == 4


def test_authors_by_org(author_operations, some_data):
    assert set(author_operations.get_authors_by_org(org_id='Lebedev Physical Institute', chunk_size=10)) == \
           {some_data[0], some_data[2]}


def test_h_index(author_operations, some_data, paper_operations, some_papers_data):
    for author in some_data:  # going through all authors
        this_h_index = author_operations.compute_h_index(author.id)  # h-index computation
    assert this_h_index >= 0 and isinstance(this_h_index, int)
