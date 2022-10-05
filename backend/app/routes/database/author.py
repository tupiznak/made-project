from fastapi import APIRouter

from database.operations.author import AuthorOperations
from database.models.author import Author

author_router = APIRouter(prefix='/author')
author_operations = AuthorOperations()


@author_router.post("/create", tags=['author'])
async def create_database_author(author: Author):
    """
     ## Запрос позвляет создавать автора в базе данных со следующими параметрами:

    - **_id**: Уникальный идентификатор автора (тип string)
    - **name**: Имя автора (тип string)
    - **org**: Название организации в которой состоит автор (тип string)
    - **gid**: Уникальный идентификатор автора gid (тип int)
    - **oid**: Уникальный идентификатор автора oid (тип int)
    - **orgid**: Уникальный идентификатор организации автора (тип string)
    - **papers**: Список уникальных идентификаторов статей данного автора (тип list)
    """
    return author_operations.create(author)


@author_router.post("/read", tags=['author'])
async def read_database_author(_id: str):
    """
     ## Запрос позвляет получать автора из базы данных со следующими параметрами:

    - **_id**: Уникальный идентификатор автора (тип string)
    - **name**: Имя автора (тип string)
    - **org**: Название организации в которой состоит автор (тип string)
    - **gid**: Уникальный идентификатор автора gid (тип int)
    - **oid**: Уникальный идентификатор автора oid (тип int)
    - **orgid**: Уникальный идентификатор организации автора (тип string)
    - **papers**: Список уникальных идентификаторов статей данного автора (тип list)

        ------------------------
     ### Для получения автора из базы данных необходимо передать обязательный параметр:
     - **_id**: Уникальный идентификатор автора (тип string)
    """
    return author_operations.get_by_id(_id=_id)


@author_router.post("/update", tags=['author'])
async def update_database_author(author: Author):
    """
     ## Запрос позвляет изменять информацию об авторе в базе данных.
        Для изменения статьи необходимо передать следующие параметры:

    - **_id**: Уникальный идентификатор автора (тип string)
    - **name**: Имя автора (тип string)
    - **org**: Название организации в которой состоит автор (тип string)
    - **gid**: Уникальный идентификатор автора gid (тип int)
    - **oid**: Уникальный идентификатор автора oid (тип int)
    - **orgid**: Уникальный идентификатор организации автора (тип string)
    - **papers**: Список уникальных идентификаторов статей данного автора (тип list)

    """
    return author_operations.full_update(author)


@author_router.post("/update/name", tags=['author'])
async def update_name_database_author(_id: str, name: str):
    """
     ## Запрос позвляет изменять имя автора из базы данных.
        Для изменения имени конкретного автора необходимо передать два обязательных параметра:

        - **_id**: Уникальный идентификатор автора (тип string)
        - **name**: Новое имя автора (тип string)
    """
    return author_operations.change_name(_id, name)


@author_router.post("/delete", tags=['author'])
async def delete_database_author(_id: str):
    """
     ## Запрос позвляет удалять автора из базы данных.
        Для удаления конкретного автора из базы данных необходимо передать обязательный параметр:
        - **_id**: Уникальный идентификатор автора (тип string)
    """
    return author_operations.delete(_id)


@author_router.get("/", tags=['author'])
async def read_database_authors(chunk_size: int = 10):
    """
     ## Запрос позвляет получить несколько авторов из базы данных.
        Для получения нужного количества авторов необходимо передать необязательный параметр:
        - **chunk_size**: количество авторов в выдаче (тип int)

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return author_operations.get_chunk(chunk_size=chunk_size)


@author_router.post("/filter", tags=['author'])
async def filter_database_authors(author_filter: dict, exclude_author: dict = None, chunk_size: int = 10):
    """
     ## Запрос позвляет получить несколько авторов из базы данных по определённым условиям.
        Для получения авторов с заданными параметрами необходимо передать значение параметров в фильтры:
        - **authir_filter**: фильтр параметров, значение которых должно быть включено в выдачу,
        - **exclude_author**: фильтр параметров, значение которых должно быть исключено из выдачи.

        Для получения нужного количества авторов необходимо передать необязательный параметр:
        - **chunk_size**: количество авторов (тип int)

     ### В ответ на запрос выозвращается *chunk_size* авторов, параметры которых включют параметры из *author_filter* и
     ### исключают параметры из *exclude_author*

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return author_operations.filter(author_filter=author_filter, exclude_author=exclude_author, chunk_size=chunk_size)


@author_router.get("/total_size", tags=['author'])
async def total_size_database_authors():
    """
     ## Запрос позвляет получить количество авторов в базе данных на данный момент.
    """
    return author_operations.total_size()


@author_router.get("/org", tags=['author'])
async def orgs_database_authors(org_id: str, chunk_size: int = 10):
    """
     ## Запрос позвляет получить несколько авторов из конкретной организации.
     Для получения авторов из конкретной организации, необходимо передать один обязательный параметр:
        - **org_id**: Название организации (тип string),

        и один необязательный параметр:
        - **chunk_size**: максимальное количество авторов в выдаче (тип int)


     ### В ответ на запрос возвращается *chunk_size* авторов из организации *org_id*
        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return author_operations.get_authors_by_org(org_id=org_id, chunk_size=chunk_size)