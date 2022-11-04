from datetime import datetime

import database.connection
import mongoengine.errors
import pytest
from database.models.author import Author, HistoryObject
from database.models.paper import Paper
from database.operations.author import AuthorOperations
from database.operations.paper import PaperOperations


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
                                         org='grtgrt', papers=[]))
    # a1: papers=['pid4']
    a2 = author_operations.create(Author(_id='q2', name='gtrgdtg',
                                         org='xa',
                                         gid='sdaf', oid='123', papers=[]))
    # a2: papers=['pid3']
    a3 = author_operations.create(Author(_id='q22', name='gtrgdtg',
                                         org='grtgrt', oid='123', papers=[]))
    # a3: papers=[]
    a4 = author_operations.create(Author(_id='222', name='gg',
                                         org='wer', papers=[],
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


@pytest.fixture
def some_authors_papers_data(author_operations, paper_operations):
    ppr_1 = paper_operations.create(Paper(_id='pid1', title='title1', abstract='abs5',
                                          year=1971, n_citation=3,
                                          authors=['id1', 'id2']))
    ppr_2 = paper_operations.create(Paper(_id='pid2', title='title2', abstract='abs5',
                                          year=1972, n_citation=0,
                                          authors=['id1', 'id6']))
    ppr_3 = paper_operations.create(Paper(_id='pid3', title='title3', abstract='abs5',
                                          year=1973, n_citation=6,
                                          authors=['id1', 'id13']))
    ppr_4 = paper_operations.create(Paper(_id='pid4', title='title4', abstract='abs5',
                                          year=1974, n_citation=1,
                                          authors=['id0', 'id1', 'idN']))
    ppr_5 = paper_operations.create(Paper(_id='pid5', title='title5', abstract='abs5',
                                          year=1975, n_citation=5,
                                          authors=['id15', 'id2', 'id1']))
    # АВТОРЫ
    author_1 = author_operations.create(Author(_id='id1', name='Nikolay Lobachevsky',
                                               org='Lebedev Physical Institute',
                                               papers=['pid1', 'pid2', 'pid3', 'pid4', 'pid5']))
    author_2 = author_operations.create(Author(_id='id2', name='Pafnuty Chebyshev',
                                               org='St Petersburg University',
                                               gid='gid2', oid='123', papers=['pid3', 'pid1', 'pid5']))
    return ppr_1, ppr_2, ppr_3, ppr_4, ppr_5, author_1, author_2


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


def test_like(author_operations, paper_operations, some_data, some_papers_data):
    author, _, _, _ = some_data
    paper_1, paper_2, _, _, _ = some_papers_data
    author_operations.like(paper_id=paper_1.id, _id=author.id)
    time_like_1 = datetime.now().timestamp()
    author_operations.like(paper_id=paper_2.id, _id=author.id)
    time_like_2 = datetime.now().timestamp()
    history_res = [HistoryObject(event='like', time=time_like_1, description=paper_1.id),
                   HistoryObject(event='like', time=time_like_2, description=paper_2.id)]
    ao_likes = author_operations.get_liked_papers(author.id)
    ao_hist = author_operations.get_history(author.id)
    assert ao_likes == [paper_2.id, paper_1.id]
    for i in range(len(history_res)):
        assert ao_hist[i].event == history_res[i].event
        assert ao_hist[i].description == history_res[i].description
        assert history_res[i].time - ao_hist[i].time <= 1


def test_like_missing_paper(author_operations, paper_operations):
    author = Author(_id='qwertyu', name='gtrgdtg', org='grtgrt', oid='123', papers=['asdf', 'zxcv'],
                    history=[])
    missing_paper_id = 'missing'
    with pytest.raises(mongoengine.errors.DoesNotExist) as excinfo:
        author_operations.like(missing_paper_id, author.id)
    assert "Paper matching query does not exist." in str(excinfo.value)


def test_delete_like(author_operations, paper_operations, some_data, some_papers_data):
    author, _, _, _ = some_data
    paper_1, paper_2, _, _, _ = some_papers_data
    author_operations.like(paper_id=paper_1.id, _id=author.id)
    time_like_1 = datetime.now().timestamp()
    author_operations.like(paper_id=paper_2.id, _id=author.id)
    time_like_2 = datetime.now().timestamp()
    author_operations.delete_like(paper_id=paper_1.id, _id=author.id)
    time_del_like_1 = datetime.now().timestamp()
    history_res = [HistoryObject(event='like', time=time_like_1, description=paper_1.id),
                   HistoryObject(event='like', time=time_like_2, description=paper_2.id),
                   HistoryObject(event='unlike', time=time_del_like_1, description=paper_1.id), ]
    ao_likes = author_operations.get_liked_papers(author.id)
    ao_hist = author_operations.get_history(author.id)
    assert ao_likes == [paper_2.id]
    for i in range(len(history_res)):
        assert ao_hist[i].event == history_res[i].event
        assert ao_hist[i].description == history_res[i].description
        assert history_res[i].time - ao_hist[i].time <= 1


def test_h_index(author_operations, paper_operations, some_authors_papers_data):
    author_id = "id1"  # id автора, для которого потом проверим точное занчение индекса Хирша
    # СТАТЬИ
    ppr_1, ppr_2, ppr_3, ppr_4, ppr_5, author_1, author_2 = some_authors_papers_data
    assert set(paper_operations.get_papers_by_author(author_id=author_id)) == \
           {ppr_1, ppr_2, ppr_3, ppr_4, ppr_5}  # корректный поиск статей автора

    # корректность возвращаемого индекса
    for author in [author_1, author_2]:  # пробегаемся по всем авторам
        this_h_index = author_operations.compute_h_index(author.id)  # вычисляем h-index
        assert this_h_index >= 0 and isinstance(this_h_index, int)  # проверяем целочисленность

    # несуществующий автор
    not_existing_author_id = "authorID"
    with pytest.raises(mongoengine.errors.DoesNotExist) as _:
        author_operations.compute_h_index(not_existing_author_id)  # выбрасывается ошибка!

    # Точное значение индекса Хирша:
    # пусть лист цитирований состоит из 5 значений [3, 0, 6, 1, 5]:
    # 1. ученый имеет 3 статьи с количеством цитирований хотя бы 3 каждая
    # 2. оставшиеся две имеют не более, чем 3 цитирования каждая
    # Ответ: искомый индекс Хирша = 3
    assert author_operations.compute_h_index(author_id=author_id) == 3


def test_set_h_index(author_operations, paper_operations, some_authors_papers_data):
    author_id = "id1"  # id автора, для которого потом проверим точное занчение индекса Хирша
    # СТАТЬИ
    ppr_1, ppr_2, ppr_3, ppr_4, ppr_5, author_1, author_2 = some_authors_papers_data
    author_without_papers = author_operations.create(Author(_id='id3', name='cvb', papers=[]))
    for author in [author_1, author_2, author_without_papers]:  # пробегаемся по всем авторам
        author_operations.set_h_index(author.id)  # устанавливаем h-index
    author_1_from_db = author_operations.get_by_id(author_1.id)
    author_2_from_db = author_operations.get_by_id(author_2.id)
    author_without_papers_from_db = author_operations.get_by_id(author_without_papers.id)
    assert author_1_from_db.h_index == 3
    assert author_2_from_db.h_index == 3
    assert author_without_papers_from_db.h_index == 0

    # несуществующий автор
    not_existing_author_id = "authorID"
    with pytest.raises(mongoengine.errors.DoesNotExist) as _:
        author_operations.set_h_index(not_existing_author_id)  # выбрасывается ошибка!


def test_get_top_h_index_authors(author_operations, some_authors_papers_data):
    ppr_1, ppr_2, ppr_3, ppr_4, ppr_5, author_1, author_2 = some_authors_papers_data
    author_without_papers = author_operations.create(Author(_id='id3', name='cvb', papers=[]))
    for author in [author_1, author_2, author_without_papers]:  # пробегаемся по всем авторам
        author_operations.set_h_index(author.id)  # устанавливаем h-index
    assert author_operations.get_top_h_index_authors(1) == ['id1']
    assert author_operations.get_top_h_index_authors(3) == ['id1', 'id2', 'id3']
