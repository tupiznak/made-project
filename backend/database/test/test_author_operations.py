import mongoengine.errors
import pytest
from datetime import datetime

import database.connection
from database.models.author import Author, HistoryObject
from database.operations.author import AuthorOperations
from database.operations.paper import PaperOperations
from database.models.paper import Paper


@pytest.fixture
def author_operations():
    database.connection.disconnect_database('citations')
    database.connection.client, database.connection.citations_db = \
        database.connection.new_connection(db_name='citations_test', alias='citations')
    author_operations = AuthorOperations(database.connection.citations_db)
    author_operations.flush()
    return author_operations


@pytest.fixture
def paper_operations():
    database.connection.disconnect_database('citations')
    database.connection.client, database.connection.citations_db = \
        database.connection.new_connection(db_name='citations_test', alias='citations')
    paper_operations = PaperOperations(database.connection.citations_db)
    paper_operations.flush()
    return paper_operations


@pytest.fixture
def some_data(author_operations):
    a1 = author_operations.create(Author(_id='q', name='gtrgdtg',
                                         org='grtgrt'))
    # a1: papers=['pid4']
    a2 = author_operations.create(Author(_id='q2', name='gtrgdtg',
                                         org='xa',
                                         gid='sdaf', oid='123'))
    # a2: papers=['pid3']
    a3 = author_operations.create(Author(_id='q22', name='gtrgdtg',
                                         org='grtgrt', oid='123'))
    # a3: papers=[]
    a4 = author_operations.create(Author(_id='222', name='gg',
                                         org='wer',
                                         gid='sdaf', oid='32'))
    # a4: papers=['pid1', 'pid2', 'pid3', 'pid4', 'pid5']
    return a1, a2, a3, a4


@pytest.fixture
def some_papers_data(paper_operations):
    # данные о статьях для тестирования h-index
    p1 = paper_operations.create(Paper(_id='pid1', title='title1',
                                       n_citation=3,
                                       authors=['222', 'q']))
    p2 = paper_operations.create(Paper(_id='pid2', title='title2',
                                       year=1960,
                                       authors=['222']))
    p3 = paper_operations.create(Paper(_id='pid3', title='title3',
                                       n_citation=6,
                                       authors=['222', 'q2']))
    p4 = paper_operations.create(Paper(_id='pid4', title='title4',
                                       year=1952, n_citation=1,
                                       authors=['222']))
    p5 = paper_operations.create(Paper(_id='pid5', title='title5',
                                       year=1982, n_citation=5,
                                       authors=['222']))
    return p1, p2, p3, p4, p5


def test_crud(author_operations):
    author = Author(_id='qwertyu', name='gtrgdtg', org='grtgrt', oid='123',
                    papers=['asdf', 'zxcv'],
                    history=[{"event": "string", "time": 0, "description": "string"}])
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


def test_like(author_operations, paper_operations):
    author = Author(_id='qwertyu', name='gtrgdtg', org='grtgrt', oid='123', papers=['asdf', 'zxcv'],
                    history=[])
    paper_1 = Paper(_id='qwerty', title='asdf', abstract='jkl', year=2012, authors=['ss', 'dd'])
    paper_2 = Paper(_id='zxc', title='asdfs', abstract='jklww', year=2011, authors=['sns', 'ddn'])
    paper_operations.create(paper_1)
    paper_operations.create(paper_2)
    author_operations.create(author)
    author_operations.like(paper_1.id, author.id)
    time_like_1 = datetime.now().timestamp()
    author_operations.like(paper_2.id, author.id)
    time_like_2 = datetime.now().timestamp()
    history = [HistoryObject(event='like', time=time_like_1, description=paper_1.id),
               HistoryObject(event='like', time=time_like_2, description=paper_2.id)]
    ao_likes = author_operations.get_liked_papers(author.id)
    ao_hist = author_operations.get_history(author.id)
    assert ao_likes == [paper_1.id, paper_2.id]
    assert [ao_hist[0].event, ao_hist[1].event] == [history[0].event, history[0].event]
    assert [ao_hist[0].description, ao_hist[1].description] == [history[0].description, history[1].description]
    assert history[0].time - ao_hist[0].time <= 1
    assert history[1].time - ao_hist[1].time <= 1


def test_like_missing_paper(author_operations, paper_operations):
    author = Author(_id='qwertyu', name='gtrgdtg', org='grtgrt', oid='123', papers=['asdf', 'zxcv'],
                    history=[])
    missing_paper_id = 'missing'
    with pytest.raises(database.db_objects.paper.DoesNotExist) as excinfo:
        author_operations.like(missing_paper_id, author.id)
    assert "Paper matching query does not exist." in str(excinfo.value)


def test_h_index(author_operations, paper_operations):
    author_id = "id1"  # id автора, для которого потом проверим точное занчение индекса Хирша
    # СТАТЬИ
    ppr_1 = paper_operations.create(Paper(_id='pid1', title='title1', abstract='abs5',
                                          year=1971, n_citation=3,
                                          authors=[author_id, 'id2']))
    ppr_2 = paper_operations.create(Paper(_id='pid2', title='title2', abstract='abs5',
                                          year=1972, n_citation=0,
                                          authors=[author_id, 'id6']))
    ppr_3 = paper_operations.create(Paper(_id='pid3', title='title3', abstract='abs5',
                                          year=1973, n_citation=6,
                                          authors=[author_id, 'id13']))
    ppr_4 = paper_operations.create(Paper(_id='pid4', title='title4', abstract='abs5',
                                          year=1974, n_citation=1,
                                          authors=['id0', author_id, 'idN']))
    ppr_5 = paper_operations.create(Paper(_id='pid5', title='title5', abstract='abs5',
                                          year=1975, n_citation=5,
                                          authors=['id15', 'id2', author_id]))
    # АВТОРЫ
    author_1 = author_operations.create(Author(_id=author_id, name='Nikolay Lobachevsky',
                                               org='Lebedev Physical Institute'))
    author_2 = author_operations.create(Author(_id='id2', name='Pafnuty Chebyshev',
                                               org='St Petersburg University',
                                               gid='gid2', oid='123', papers=['pid3']))

    assert set(paper_operations.get_papers_by_author(author_id=author_id)) == \
           {ppr_1, ppr_2, ppr_3, ppr_4, ppr_5}  # корректный поиск статей автора

    # корректность возвращаемого индекса
    for author in [author_1, author_2]:  # пробегаемся по всем авторам
        this_h_index = author_operations.compute_h_index(author.id)  # вычисляем h-index
        assert this_h_index >= 0 and isinstance(this_h_index, int)  # проверяем целочисленность

    # несуществующий автор
    not_existing_author_id = "authorID"
    with pytest.raises(database.db_objects.author.DoesNotExist) as excinfo:
        author_operations.compute_h_index(not_existing_author_id)  # выбрасывается ошибка!

    # Точное значение индекса Хирша:
    # пусть лист цитирований состоит из 5 значений [3, 0, 6, 1, 5]:
    # 1. ученый имеет 3 статьи с количеством цитирований хотя бы 3 каждая
    # 2. оставшиеся две имеют не более, чем 3 цитирования каждая
    # Ответ: искомый индекс Хирша = 3
    assert author_operations.compute_h_index(author_id=author_id) == 3


# def test_delete_like(author_operations, paper_operations):
#     author = Author(_id='qwertyu', name='gtrgdtg', org='grtgrt', oid='123', papers=['asdf', 'zxcv'],
#                     history=[])
#     paper_1 = Paper(_id='qwerty', title='asdf', abstract='jkl', year=2012, authors=['ss', 'dd'])
#     paper_2 = Paper(_id='zxc', title='asdfs', abstract='jklww', year=2011, authors=['sns', 'ddn'])
#     paper_operations.create(paper_1)
#     paper_operations.create(paper_2)
#     author_operations.create(author)
#     author_operations.like(paper_id=paper_1.id, _id=author.id)
#     author_operations.like(paper_id=paper_2.id, _id=author.id)
#     time_like_2 = datetime.now().timestamp()
#     author_operations.delete_like(paper_id=paper_1.id, _id=author.id)
#     history = [HistoryObject(event='like', time=time_like_2, description=paper_2.id)]
#     ao_likes = author_operations.get_liked_papers(author.id)
#     ao_hist = author_operations.get_history(author.id)
#     assert ao_likes == [paper_2.id]
#     assert ao_hist[0].event == history[0].event
#     assert ao_hist[0].description == history[0].description
#     assert history[0].time - ao_hist[0].time <= 1
