# Проект MADE, 1ый семестр (команда 4)

## Цель
создание платформы для ученых с рекомендательной системой интересных статей и потенциальных соавторов для будущих публикаций зарегистрированному пользователю (автору).

## Dataset

_**Citation Network Dataset**_ – [aminer.cn](https://www.aminer.cn/citation)

## Требования
Для работы над проектом нужен `Python 3.9` (или более поздняя версия).

## Структура проекта

    made-project
    │
    ├── backend                 <- backend development
    │   │
    │   ├── app
    │   │
    │   ├── database            <- DB objects and their operations discriptions
    │   │   │
    │   │   ├── db_objects
    │   │   │
    │   │   ├── models
    │   │   │
    │   │   ├── operations
    │   │   │
    │   │   └── test            <- tests for database objects operations  
    │   │
    │   ├── ml                  <- ml part researches
    │   │   │
    │   │   ├── analyse         <- notebooks of the first stage EDA
    │   │
    │   └── requirements.txt    <- requirements
    │
    ├── docker
    │   │
    │   ├── build.sh            <- script for building all dockers
    │   │
    │   ├── run.sh              <- script for running all dockers
    │   │
    │   └── stop.sh             <- script to close all dockers   
    │
    ├── frontend                <- frontend development
    │   │
    │   └── site                <- site development
    │       │
    │       └── ...
    │
    ├── logs                    <- logging folder
    │   │
    │   ├── grafana
    │   │
    │   ├── mongodb-grafana
    │
    └── README.md               <- user guide README

## Подключение к БД
Из директории `/docker` последовательно запустить скрипты `build.sh` и `run.sh`.

После завершения работы с БД запустить скрипт `stop.sh`.

Участие в [проекте](https://docs.google.com/spreadsheets/d/1rfngbj1W42-KzUHuT28uXmEwZg7bM-FE)

| Спринт | Иванов Евгений | Куцко Яна | Шевченко Евгений | Притугин Михаил | Удинский Евгений | Сахно Денис |
| ------ | -------------- | --------- | ---------------- | --------------- | ---------------- | ----------- |
| 1      | архитектура репы, докеры, композ, архитектура бэка, fastapi, mongodb, mongo atlas, vercel backend, vercel front, архитектура фронта, vue3.js, vuetify, CI (github), Kanban (github), prometheus, grafana, скрипт наполнения БД и преобразование исходных данных (jsonl) | [EDA](https://github.com/tupiznak/made-project/blob/develop/backend/ml/analyze/2.ipynb) | наполнял код бэка тестами, ф-ями, доками | [EDA](https://github.com/tupiznak/made-project/blob/develop/backend/ml/analyze/3.ipynb) | [EDA](https://github.com/tupiznak/made-project/blob/develop/backend/ml/analyze/1.ipynb) | преза |
| 2     | пара метрик в графану, ф-ии в бэке, докер для дева и прода, форма с лайками статей и фильтрации статей на фронте, поиск по абстракту, просмотр всех pr | форма авторизации, регистрации, профиля автора на фронте | логика лайков в бэке (история пользователя), ф-ии в бэк | - | - | - |
| 3     | граф соавторов на plotly, индексы в БД, необходимые ф-ии в бэке, скрипт разделения train/test на разные коллекции, просмотр всех pr | форма аналитики в вебе | логика дизлайков в бэке, ф-ии в бэке, ф-я топа цитирования, улучшение работы Хирша, наполнение БД Хиршом | LDA модель для выделения тегов из статей | - | ф-я Хирша в бэке |

