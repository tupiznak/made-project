import pytest
import mongoengine.errors

from database.models import Paper
from database.operations import PaperOperations


@pytest.fixture
def db():
    PaperOperations.flush()


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


def test_chunk(db):
    p1 = PaperOperations.create(Paper(_id='q', title='gtrgdtg', abstract='grtgrt'))
    p2 = PaperOperations.create(Paper(_id='q2', title='gtrgdtg', abstract='grtgrt'))
    p3 = PaperOperations.create(Paper(_id='q22', title='gtrgdtg', abstract='grtgrt'))
    p4 = PaperOperations.create(Paper(_id='222', title='gtrgdtg', abstract='grtgrt'))
    assert len(PaperOperations.get_chunk(chunk_size=2)) == 2
    assert len(PaperOperations.get_chunk(chunk_size=20)) == 4
    assert PaperOperations.get_chunk(id_list=['q22', 'q']) == [p3, p1]
    with pytest.raises(mongoengine.errors.DoesNotExist):
        assert PaperOperations.get_chunk(id_list=['q22', 'qer']) == [p3, p1]
