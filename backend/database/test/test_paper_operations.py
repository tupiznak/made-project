import mongoengine.errors
import pytest

import database.connection
from database.models.paper import Paper
from database.operations.paper import PaperOperations


@pytest.fixture
def paper_operations():
    database.connection.disconnect_database('citations')
    database.connection.client, database.connection.citations_db = \
        database.connection.new_connection(db_name='citations_test', alias='citations')
    paper_operations = PaperOperations(database.connection.citations_db)
    paper_operations.flush()
    return paper_operations


@pytest.fixture
def some_data(paper_operations):
    p1 = paper_operations.create(Paper(_id='q', title='gtrgdtg', abstract='grtgrt'))
    p2 = paper_operations.create(Paper(_id='q2', title='gtrgdtg', abstract='xa', year=2002, venue='123'))
    p3 = paper_operations.create(Paper(_id='q22', title='gtrgdtg', abstract='grtgrt kjfwe ewr', venue='123'))
    p4 = paper_operations.create(Paper(_id='222', title='gg', abstract='wer', year=2002, venue='32'))
    return p1, p2, p3, p4


def test_crud(paper_operations):
    paper = Paper(_id='q', title='gtrgdtg', abstract='grtgrt', venue='123')
    paper_operations.model_to_db(paper_operations.to_model(paper_operations.model_to_db(paper)))

    paper_operations.create(paper)
    with pytest.raises(mongoengine.errors.NotUniqueError):
        paper_operations.create(paper)
    assert paper_operations.get_by_id(_id=paper.id) == paper

    paper.abstract = 'ewwe'
    paper_operations.full_update(paper)

    paper.title = 'ww'
    paper_operations.change_title(_id=paper.id, title=paper.title)
    assert paper_operations.get_by_id(paper.id) == paper

    with pytest.raises(mongoengine.errors.DoesNotExist):
        paper_operations.change_title(_id='3242ewr', title='ewsf')

    paper_operations.delete(paper.id)
    with pytest.raises(mongoengine.errors.DoesNotExist):
        paper_operations.delete(paper.id)


def test_chunk(paper_operations, some_data):
    p1, p2, p3, p4 = some_data
    assert len(paper_operations.get_chunk(chunk_size=2)) == 2
    assert len(paper_operations.get_chunk(chunk_size=20)) == 4
    assert paper_operations.get_chunk(id_list=['q22', 'q']) == [p3, p1]
    with pytest.raises(mongoengine.errors.DoesNotExist):
        assert paper_operations.get_chunk(id_list=['q22', 'qer']) == [p3, p1]


def test_filter(paper_operations, some_data):
    assert paper_operations.base_filter(dict(title='gg')) == [some_data[3]]
    assert set(paper_operations.base_filter(dict(year=2002))) == {some_data[1], some_data[3]}
    assert set(paper_operations.base_filter(dict(year=2002))) == {some_data[1], some_data[3]}
    assert paper_operations.base_filter(dict(year=2002, title='gg')) == [some_data[3]]
    assert paper_operations.base_filter(dict(year=2002), exclude_paper=dict(title='gg')) == [some_data[1]]


def test_sub_str_abstract(paper_operations, some_data):
    assert set(paper_operations.find_sub_string_in_abstract('we')) == {some_data[2], some_data[3]}
    assert set(paper_operations.find_sub_string_in_abstract('we', chunk_size=1)) == \
           {some_data[2]} or {some_data[3]}


def test_count(paper_operations, some_data):
    assert paper_operations.total_size() == 4


def test_paper_by_venue(paper_operations, some_data):
    assert set(paper_operations.get_papers_by_venue(venue_id='123', chunk_size=10)) == \
           {some_data[1], some_data[2]}
