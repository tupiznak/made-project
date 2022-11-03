import mongoengine.errors
import networkx as nx
import pytest

from database.models.author import Author
from database.models.paper import Paper


def test_crud(paper_operations):
    paper = Paper(_id='q', title='gtrgdtg', abstract='grtgrt', venue='123', authors=['author1', 'author2'])
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


def test_paper_citations(paper_operations, some_data):
    # тест метода get_n_citations(paper_id: str)
    citations_list = [paper_operations.get_n_citations(paper.id) for paper in some_data]
    assert len(citations_list) == len(some_data)
    assert sum(citations_list) >= 0
    assert sum(citations_list) == 3


def test_items_chunk_iter(some_data, paper_operations):
    items_it = paper_operations.items_chunk_iter(chunk_size=2)
    papers = []
    for paper in items_it:
        papers.extend(paper)
    assert len(some_data) == len(papers)
    assert set(some_data) == set(papers)


def test_create_graph_coauthors(paper_operations, author_operations):
    [author_operations.create(Author(_id=i)) for i in range(10)]
    paper_operations.create(Paper(_id='a', authors=[0, 1, 2]))
    paper_operations.create(Paper(_id='b', authors=[0, 5, 6]))
    paper_operations.create(Paper(_id='c', authors=[0, 8, 9]))
    paper_operations.create(Paper(_id='d', authors=[3, 4]))
    graph = paper_operations.create_graph_coauthors()
    need_graph = nx.Graph()
    need_graph.add_nodes_from([0, 1, 2, 5, 6, 8, 9, 3, 4])
    need_graph.add_edges_from([
        [0, 1], [0, 2], [1, 2],
        [0, 5], [0, 6], [5, 6],
        [0, 8], [0, 9], [8, 9],
        [3, 4],
    ])
    assert nx.is_isomorphic(need_graph, graph)


def test_get_papers_by_author(paper_operations, some_data):
    # тест метода get_papers_by_author(author_id)
    assert set(paper_operations.get_papers_by_author(author_id='a-id1')) == \
           {some_data[0], some_data[1]}
    assert set(paper_operations.get_papers_by_author(author_id='a-id2')) == \
           {some_data[0], some_data[2]}
