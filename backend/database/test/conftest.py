import pytest
import database.connection
from database.models.author import Author
from database.models.paper import Paper
from database.operations.author import AuthorOperations
from database.operations.paper import PaperOperations


@pytest.fixture
def db():
    database.connection.disconnect_database('citations')
    database.connection.client, database.connection.citations_db = \
        database.connection.new_connection(db_name='citations_test', alias='citations')


@pytest.fixture
def author_operations(db):
    author_operations = AuthorOperations(database.connection.citations_db)
    author_operations.flush()
    return author_operations


@pytest.fixture
def paper_operations(db):
    paper_operations = PaperOperations(database.connection.citations_db)
    paper_operations.flush()
    return paper_operations


@pytest.fixture
def some_authors_data(author_operations):
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
