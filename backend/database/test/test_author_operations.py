from datetime import datetime

import mongoengine.errors
import mongoengine.errors
import networkx as nx
import pytest

from database.models.author import Author, HistoryObject
from database.models.paper import Paper
from ml.analyze.graph_coauthors import plot_authors_graph


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


def test_chunk(author_operations, some_authors_data):
    a1, a2, a3, a4 = some_authors_data
    assert len(author_operations.get_chunk(chunk_size=2)) == 2
    assert len(author_operations.get_chunk(chunk_size=20)) == 4
    assert author_operations.get_chunk(id_list=['q22', 'q']) == [a3, a1]
    with pytest.raises(mongoengine.errors.DoesNotExist):
        assert author_operations.get_chunk(id_list=['q22', 'qer']) == [a3, a1]


def test_filter(author_operations, some_authors_data):
    assert author_operations.filter(dict(name='gg')) == [some_authors_data[3]]
    assert set(author_operations.filter(dict(gid='sdaf'))) == {some_authors_data[1], some_authors_data[3]}
    assert set(author_operations.filter(dict(gid='sdaf'))) == {some_authors_data[1], some_authors_data[3]}
    assert author_operations.filter(dict(gid='sdaf', name='gg')) == [some_authors_data[3]]
    assert author_operations.filter(dict(gid='sdaf'), exclude_author=dict(name='gg')) == [some_authors_data[1]]


def test_count(author_operations, some_authors_data):
    assert author_operations.total_size() == 4


def test_authors_by_org(author_operations, some_authors_data):
    assert set(author_operations.get_authors_by_org(org_id='grtgrt', chunk_size=10)) == \
           {some_authors_data[0], some_authors_data[2]}


def test_like(author_operations, paper_operations, some_authors_data, some_papers_data):
    author, _, _, _ = some_authors_data
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


def test_create_graph_coauthors(paper_operations, author_operations):
    [author_operations.create(Author(_id=i)) for i in range(10)]
    paper_operations.create(Paper(_id='a', authors=[0, 1, 2]))
    paper_operations.create(Paper(_id='b', authors=[0, 5, 6]))
    paper_operations.create(Paper(_id='c', authors=[0, 8, 9]))
    paper_operations.create(Paper(_id='d', authors=[3, 4]))
    graph = author_operations.create_graph_coauthors_by_author('0')
    need_graph = nx.Graph()
    need_graph.add_nodes_from([0, 1, 2, 5, 6, 8, 9])
    need_graph.add_edges_from([
        [0, 1], [0, 2],
        [0, 5], [0, 6],
        [0, 8], [0, 9],
    ])
    plot_authors_graph(graph)  # .show()
    assert nx.is_isomorphic(need_graph, graph)


def test_delete_like(author_operations, paper_operations, some_authors_data, some_papers_data):
    author, _, _, _ = some_authors_data
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


def test_set_h_index(author_operations, some_authors_papers_data):
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
