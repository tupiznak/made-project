from fastapi import APIRouter

from database.operations.paper import PaperOperations
from database.models.paper import Paper

paper_router = APIRouter(prefix='/paper')
paper_operations = PaperOperations()


@paper_router.post("/create", tags=['paper'])
async def create_database_paper(paper: Paper):
    """
     ## Запрос позвляет создавать статьи в базе данных со следующими параметрами:

    - **_id**: Уникальный идентификатор статьи (тип string)
    - **title**: Название статьи (тип string)
    - **abstract**: Описание текста статьи (тип string)
    - **year**: Год публикации статьи (тип int)
    - **n_citation**: Количество цитирований статьи (тип int)
    - **venue**: Место публикации статьи (тип string)
    - **authors**: Список уникальных идентификаторов авторов статьи (тип list)
    """
    return paper_operations.create(paper)


@paper_router.post("/read", tags=['paper'])
async def read_database_paper(_id: str):
    """
     ## Запрос позвляет получать статьи из базы данных со следующими параметрами:

        - **_id**: Уникальный идентификатор статьи (тип string)
        - **title**: Название статьи (тип string)
        - **abstract**: Описание текста статьи (тип string)
        - **year**: Год публикации статьи (тип int)
        - **n_citation**: Количество цитирований статьи (тип int)
        - **venue**: Место публикации статьи (тип string)
        - **authors**: Список уникальных идентификаторов авторов статьи (тип list)

        ------------------------
     ### Для получения статьи необходимо передать обязательный параметр:
     - **_id**: Уникальный идентификатор статьи (тип string)
    """
    return paper_operations.get_by_id(_id=_id)


@paper_router.post("/update", tags=['paper'])
async def update_database_paper(paper: Paper):
    """
     ## Запрос позвляет изменять статьи в базе данных.
        Для изменения статьи необходимо передать следующие параметры:

        - **_id**: Уникальный идентификатор статьи (тип string)
        - **title**: Название статьи (тип string)
        - **abstract**: Описание текста статьи (тип string)
        - **year**: Год публикации статьи (тип int)
        - **n_citation**: Количество цитирований статьи (тип int)
        - **venue**: Место публикации статьи (тип string)
        - **authors**: Список уникальных идентификаторов авторов статьи (тип list)

    """
    return paper_operations.full_update(paper)


@paper_router.post("/update/title", tags=['paper'])
async def update_title_database_paper(_id: str, title: str):
    """
     ## Запрос позвляет изменять название статьи в базе данных.
        Для изменения названия конкретной статьи необходимо передать два обязательных параметра:

        - **_id**: Уникальный идентификатор статьи (тип string)
        - **title**: Новое название статьи (тип string)
    """
    return paper_operations.change_title(_id, title)


@paper_router.post("/delete", tags=['paper'])
async def delete_database_paper(_id: str):
    """
     ## Запрос позвляет удалять статью из базы данных.
        Для удаления конкретной статьи из базы данных необходимо передать обязательный параметр:
        - **_id**: Уникальный идентификатор статьи (тип string)
    """
    return paper_operations.delete(_id)


@paper_router.get("/", tags=['paper'])
async def read_database_papers(chunk_size: int = 10):
    """
     ## Запрос позвляет получить несколько статей из базы данных.
        Для получения нужного количества статей необходимо передать необязательный параметр:
        - **chunk_size**: количество статей (тип int)

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return paper_operations.get_chunk(chunk_size=chunk_size)


@paper_router.post("/filter", tags=['paper'])
async def filter_database_papers(paper_filter: dict, exclude_paper: dict = None, chunk_size: int = 10):
    """
     ## Запрос позвляет получить несколько статей из базы данных по определённым условиям.
        Для получения статей с заданными параметрами необходимо передать значение параметров в фильтры:
        - **paper_filter**: фильтр параметров, значение которых должно быть включено в выдачу,
        - **exclude_paper**: фильтр параметров, значение которых должно быть исключено из выдачи.

        Для получения нужного количества статей необходимо передать необязательный параметр:
        - **chunk_size**: количество статей (тип int)

     ### В ответ на запрос выозвращается *chunk_size* статей, параметры которых включют параметры из *paper_filter* и
     ### исключают параметры из *exclude_paper*

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return paper_operations.filter(paper_filter=paper_filter, exclude_paper=exclude_paper, chunk_size=chunk_size)


@paper_router.post("/abstract_substring", tags=['paper'])
async def sub_str_in_abstract_database_papers(sub_string: str, chunk_size: int = 10):
    """
     ## Запрос позвляет получить несколько статей из базы данных по подстроке в описании статьи.
        Для получения статей, в описании которых присутствует заданная подстрока, необходимо передать
        один обязательный параметр:
        - **sub_string**: Подстрока, которая должна быть включена в описании статей (тип string),

        и один необязательный параметр:
        - **chunk_size**: количество статей (тип int)


     ### В ответ на запрос выозвращается *chunk_size* статей, включающих подстроку *sub_string* в описании статьи
        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return paper_operations.find_sub_string_in_abstract(sub_str=sub_string, chunk_size=chunk_size)


@paper_router.get("/total_size", tags=['paper'])
async def total_size_database_papers():
    """
     ## Запрос позвляет получить количество статей в базе данных на данный момент.
    """
    return paper_operations.total_size()


@paper_router.get("/venue", tags=['paper'])
async def venues_database_papers(venue_id: str, chunk_size: int = 10):
    """
     ## Запрос позвляет получить несколько статей из базы данных по месту её публикации.
     Для получения статей по месту их публикации, необходимо передать один обязательный параметр:
        - **venue_id**: Место публикации статьи (тип string),

        и один необязательный параметр:
        - **chunk_size**: количество статей (тип int)


     ### В ответ на запрос возвращается *chunk_size* статей, место публикации которых соответствует *venue_id*
        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return paper_operations.get_papers_by_venue(venue_id=venue_id, chunk_size=chunk_size)
