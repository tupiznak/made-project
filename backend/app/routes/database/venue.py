from fastapi import APIRouter

from database.operations.venue import VenueOperations
from database.models.venue import Venue

venue_router = APIRouter(prefix='/venue')
venue_operations = VenueOperations()


@venue_router.post("/create", tags=['venue'])
async def create_database_venue(venue: Venue):
    """
     ## Запрос позволяет создавать событие в базе данных со следующими параметрами:

    - **_id**: Уникальный идентификатор события (тип string)
    - **name_d**: Наименование события (тип string)
    - **raw**: Краткое наименование события (тип string)
    - **type**: Тип события (тип int)
    """
    return venue_operations.create(venue)


@venue_router.post("/read", tags=['venue'])
async def read_database_venue(_id: str):
    """
     ## Запрос позволяет получать событие из базы данных со следующими параметрами:

    - **_id**: Уникальный идентификатор события (тип string)
    - **name_d**: Наименование события (тип string)
    - **raw**: Краткое наименование события (тип string)
    - **type**: Тип события (тип int)

        ------------------------
     ### Для получения события необходимо передать обязательный параметр:
     - **_id**: Уникальный идентификатор события (тип string)
    """
    return venue_operations.get_by_id(_id=_id)


@venue_router.post("/update", tags=['venue'])
async def update_database_venue(venue: Venue):
    """
     ## Запрос позволяет изменять событие в базе данных.
        Для изменения события необходимо передать следующие параметры:

    - **_id**: Уникальный идентификатор события (тип string)
    - **name_d**: Наименование события (тип string)
    - **raw**: Краткое наименование события (тип string)
    - **type**: Тип события (тип int)

    """
    return venue_operations.full_update(venue)


@venue_router.post("/update/name", tags=['venue'])
async def update_name_database_venue(_id: str, name_d: str):
    """
     ## Запрос позволяет изменять название события в базе данных.
        Для изменения названия конкретного события необходимо передать два обязательных параметра:

        - **_id**: Уникальный идентификатор события (тип string)
        - **name_d**: Новое название события (тип string)
    """
    return venue_operations.change_name_d(_id, name_d)


@venue_router.post("/delete", tags=['venue'])
async def delete_database_venue(_id: str):
    """
     ## Запрос позволяет удалять событие из базы данных.
        Для удаления конкретного события из базы данных необходимо передать обязательный параметр:
        - **_id**: Уникальный идентификатор события (тип string)
    """
    return venue_operations.delete(_id)


@venue_router.get("/", tags=['venue'])
async def read_database_venue(chunk_size: int = 10):
    """
     ## Запрос позволяет получить несколько событий из базы данных.
        Для получения нужного количества событий необходимо передать необязательный параметр:
        - **chunk_size**: количество событий в выдаче (тип int)

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return venue_operations.get_chunk(chunk_size=chunk_size)


@venue_router.post("/filter", tags=['venue'])
async def filter_database_venues(venue_filter: dict, exclude_venue: dict = None, chunk_size: int = 10):
    """
     ## Запрос позволяет получить несколько событий из базы данных по определённым условиям.
        Для получения событий с заданными параметрами необходимо передать значение параметров в фильтры:
        - **venue_filter**: фильтр параметров, значение которых должно быть включено в выдачу,
        - **exclude_venue**: фильтр параметров, значение которых должно быть исключено из выдачи.

        Для получения нужного количества статей необходимо передать необязательный параметр:
        - **chunk_size**: количество событий в выдаче (тип int)

     ### В ответ на запрос возвращается *chunk_size* событий, параметры которых включают параметры из *paper_filter* и
     ### исключают параметры из *exclude_paper*

        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return venue_operations.filter(venue_filter=venue_filter, exclude_venue=exclude_venue, chunk_size=chunk_size)


@venue_router.get("/total_size", tags=['venue'])
async def total_size_database_venues():
    """
     ## Запрос позволяет получить количество событий в базе данных на данный момент.
    """
    return venue_operations.total_size()


@venue_router.get("/type", tags=['venue'])
async def type_database_venues(type_id: int, chunk_size: int = 10):
    """
     ## Запрос позволяет получить несколько событий из базы данных по их типу.
     Для получения событий по их типу, необходимо передать один обязательный параметр:
        - **type_id**: Тип события (тип string),

        и один необязательный параметр:
        - **chunk_size**: количество событий в выдаче (тип int)


     ### В ответ на запрос возвращается *chunk_size* событий, тип которых соответствует *type_id*
        -------------
        По умолчанию параметр **chunk_size** имеет значение 10
    """
    return venue_operations.get_venues_by_type(type_id=type_id, chunk_size=chunk_size)
