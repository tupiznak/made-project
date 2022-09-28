import mongoengine.errors
import pytest

from database.models import Paper
from database.operations import PaperOperations


@pytest.fixture
def db():
    PaperOperations.flush()


@pytest.fixture
def some_data(db):
    p1 = PaperOperations.create(Paper(_id='q', title='gtrgdtg', abstract='grtgrt'))
    p2 = PaperOperations.create(Paper(_id='q2', title='gtrgdtg', abstract='xa', year=2002))
    p3 = PaperOperations.create(Paper(_id='q22', title='gtrgdtg', abstract='grtgrt kjfwe ewr'))
    p4 = PaperOperations.create(Paper(_id='222', title='gg', abstract='wer', year=2002))
    return p1, p2, p3, p4


def test_crud(db):
    paper = Paper(_id='q', title='gtrgdtg', abstract='grtgrt')
    PaperOperations.model_to_db(PaperOperations.to_model(PaperOperations.model_to_db(paper)))

    PaperOperations.create(paper)
    with pytest.raises(mongoengine.errors.NotUniqueError):
        PaperOperations.create(paper)
    assert PaperOperations.get_by_id(_id=paper.id) == paper

    paper.abstract = 'ewwe'
    PaperOperations.full_update(paper)

    paper.title = 'ww'
    PaperOperations.change_title(_id=paper.id, title=paper.title)
    assert PaperOperations.get_by_id(paper.id) == paper

    with pytest.raises(mongoengine.errors.DoesNotExist):
        PaperOperations.change_title(_id='3242ewr', title='ewsf')

    PaperOperations.delete(paper.id)
    with pytest.raises(mongoengine.errors.DoesNotExist):
        PaperOperations.delete(paper.id)


def test_chunk(some_data):
    p1, p2, p3, p4 = some_data
    assert len(PaperOperations.get_chunk(chunk_size=2)) == 2
    assert len(PaperOperations.get_chunk(chunk_size=20)) == 4
    assert PaperOperations.get_chunk(id_list=['q22', 'q']) == [p3, p1]
    with pytest.raises(mongoengine.errors.DoesNotExist):
        assert PaperOperations.get_chunk(id_list=['q22', 'qer']) == [p3, p1]


def test_filter(some_data):
    assert PaperOperations.filter(dict(title='gg')) == [some_data[3]]
    assert set(PaperOperations.filter(dict(year=2002))) == {some_data[1], some_data[3]}
    assert set(PaperOperations.filter(dict(year=2002))) == {some_data[1], some_data[3]}
    assert PaperOperations.filter(dict(year=2002, title='gg')) == [some_data[3]]
    assert PaperOperations.filter(dict(year=2002), exclude_paper=dict(title='gg')) == [some_data[1]]


def test_sub_str_abstract(some_data):
    assert set(PaperOperations.find_sub_string_in_abstract('we')) == {some_data[2], some_data[3]}
    assert set(PaperOperations.find_sub_string_in_abstract('we', chunk_size=1)) == \
           {some_data[2]} or {some_data[3]}
