from io import StringIO

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database.operations.author import AuthorOperations

from database.models.author import Author
from ml.analyze.graph_coauthors import plot_authors_graph
author_router = APIRouter(prefix='/author')
author_operations = AuthorOperations()


@author_router.post("/create", tags=['author'])
async def create_database_author(author: Author):
    """
     ## Запрос позволяет создавать автора в базе данных со следующими параметрами:

    - **_id**: Уникальный идентификатор автора (тип string)
    - **name**: Имя автора (тип string)
    - **org**: Название организации в которой состоит автор (тип string)
    - **gid**: Уникальный идентификатор автора gid (тип int)
    - **oid**: Уникальный идентификатор автора oid (тип int)
    - **orgid**: Уникальный идентификатор организации автора (тип string)
    - **papers**: Список уникальных идентификаторов статей данного автора (тип list)
    - **history**: История действий пользователя (тип list)
    """
    return author_operations.create(author)


@author_router.post("/read", tags=['author'])
async def read_database_author(_id: str):
    """
     ## Запрос позволяет получать автора из базы данных со следующими параметрами:

    - **_id**: Уникальный идентификатор автора (тип string)
    - **name**: Имя автора (тип string)
    - **org**: Название организации в которой состоит автор (тип string)
    - **gid**: Уникальный идентификатор автора gid (тип int)
    - **oid**: Уникальный идентификатор автора oid (тип int)
    - **orgid**: Уникальный идентификатор организации автора (тип string)
    - **papers**: Список уникальных идентификаторов статей данного автора (тип list)
    - **history**: История действий пользователя (тип list)

        ------------------------
     ### Для получения автора из базы данных необходимо передать обязательный параметр:
     - **_id**: Уникальный идентификатор автора (тип string)
    """
    return author_operations.get_by_id(_id)


@author_router.post("/update", tags=['author'])
async def update_database_author(author: Author):
    """
     ## Запрос позволяет изменять информацию об авторе в базе данных.
        Для изменения статьи необходимо передать следующие параметры:

    - **_id**: Уникальный идентификатор автора (тип string)
    - **name**: Имя автора (тип string)
    - **org**: Название организации в которой состоит автор (тип string)
    - **gid**: Уникальный идентификатор автора gid (тип int)
    - **oid**: Уникальный идентификатор автора oid (тип int)
    - **orgid**: Уникальный идентификатор организации автора (тип string)
    - **papers**: Список уникальных идентификаторов статей данного автора (тип list)
    - **history**: История действий пользователя (тип list)

    """
    return author_operations.full_update(author)


@author_router.post("/update/name", tags=['author'])
async def update_name_database_author(_id: str, name: str):
    """
     ## Запрос позволяет изменять имя автора из базы данных.
        Для изменения имени конкретного автора необходимо передать два обязательных параметра:

        - **_id**: Уникальный идентификатор автора (тип string)
        - **name**: Новое имя автора (тип string)
    """
    return author_operations.change_name(_id=_id, name=name)


@author_router.post("/delete", tags=['author'])
async def delete_database_author(_id: str):
    """
     ## Запрос позволяет удалять автора из базы данных.
        Для удаления конкретного автора из базы данных необходимо передать обязательный параметр:
        - **_id**: Уникальный идентификатор автора (тип string)
    """
    return author_operations.delete(_id)


@author_router.get("/", tags=['author'])
async def read_database_authors(chunk_size: int = 10):
    """
     ## Запрос позволяет получить несколько авторов из базы данных.
        Для получения нужного количества авторов необходимо передать необязательный параметр:
        - **chunk_size**: количество авторов в выдаче (тип int)

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return author_operations.get_chunk(chunk_size=chunk_size)


@author_router.post("/filter", tags=['author'])
async def filter_database_authors(author_filter: dict, exclude_author: dict = None, chunk_size: int = 10):
    """
     ## Запрос позволяет получить несколько авторов из базы данных по определённым условиям.
        Для получения авторов с заданными параметрами необходимо передать значение параметров в фильтры:
        - **author_filter**: фильтр параметров, значение которых должно быть включено в выдачу,
        - **exclude_author**: фильтр параметров, значение которых должно быть исключено из выдачи.

        Для получения нужного количества авторов необходимо передать необязательный параметр:
        - **chunk_size**: количество авторов (тип int)

     ### В ответ на запрос возвращается *chunk_size* авторов, параметры которых включают параметры из *author_filter* и
     ### исключают параметры из *exclude_author*

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return author_operations.filter(author_filter=author_filter, exclude_author=exclude_author, chunk_size=chunk_size)


@author_router.get("/total_size", tags=['author'])
async def total_size_database_authors():
    """
     ## Запрос позволяет получить количество авторов в базе данных на данный момент.
    """
    return author_operations.total_size()


@author_router.get("/org", tags=['author'])
async def orgs_database_authors(org_id: str, chunk_size: int = 10):
    """
     ## Запрос позволяет получить несколько авторов из конкретной организации.
     Для получения авторов из конкретной организации, необходимо передать один обязательный параметр:
        - **org_id**: Название организации (тип string),

        и один необязательный параметр:
        - **chunk_size**: максимальное количество авторов в выдаче (тип int)


     ### В ответ на запрос возвращается *chunk_size* авторов из организации *org_id*
        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return author_operations.get_authors_by_org(org_id=org_id, chunk_size=chunk_size)


@author_router.post("/update/like", tags=['author'])
async def update_like_database_author(_id: str, paper_id: str):
    """
     ## Запрос позволяет добавить запись в базе данных о том что автору понравилась статья.
        Для добавления лайка у автора необходимо передать два обязательных параметра:

        - **_id**: Уникальный идентификатор автора (тип string)
        - **paper_id**: Уникальный идентификатор статьи, которая понравилась автору (тип string)
    """
    return author_operations.like(paper_id=paper_id, _id=_id)


@author_router.post("/update/unlike", tags=['author'])
async def update_unlike_database_author(_id: str, paper_id: str):
    """
     ## Запрос позволяет удалить запись в базе данных о том что автору понравилась статья.
        Для удаления лайка у автора необходимо передать два обязательных параметра:

        - **_id**: Уникальный идентификатор автора (тип string)
        - **paper_id**: Уникальный идентификатор статьи, которая понравилась автору (тип string)
    """
    return author_operations.delete_like(paper_id=paper_id, _id=_id)


@author_router.get("/coauthors_graph", tags=['author'], response_class=HTMLResponse)
async def coauthors_graph(author_id: str):
    """
     ## Запрос возвращает html с полным графом соавторов.
    """
    buff = StringIO()
    fig = plot_authors_graph(author_operations
                             .create_graph_coauthors_by_author(author_id=author_id))
    fig.write_html(buff, include_plotlyjs='cdn')
    return HTMLResponse(content=buff.getvalue(), status_code=200)


@author_router.get("/history", tags=['author'])
async def get_history_database_author(_id: str):
    """
     ## Запрос позволяет получить историю действий автора из базы данных.
        Для получения истории действий автора необходимо передать один обязательный параметр:

        - **_id**: Уникальный идентификатор автора (тип string)

        ### В ответ на запрос возвращается список объектов, представляющих собой действия пользователя
    """
    return author_operations.get_history(_id)


@author_router.get("/liked_papers", tags=['author'])
async def get_author_liked_papers(_id: str):
    """
     ## Запрос позволяет получить из базы данных список статей, понравившихся автору.
        Для получения списка статей, понравившихся автору, необходимо передать один обязательный параметр:

        - **_id**: Уникальный идентификатор автора (тип string)

        ### В ответ на запрос возвращается список статей, понравившихся автору
    """
    return author_operations.get_liked_papers(_id)


@author_router.get("/get_top_authors", tags=['author'])
async def get_author_liked_papers(top_n: int = 10):
    """
     ## Запрос позволяет получить из базы данных топ авторов по индексу Хирша.
        Для получения топа авторов можно передать один необязательный параметр:

        - **top_n**: Количество авторов в топе (тип string)

        ### В ответ на запрос возвращается список авторов в порядке убывания индекса Хирша

        По умолчанию параметр **top_n** имеет значение 10
    """
    return author_operations.get_top_h_index_authors(top_n=top_n)
