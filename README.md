# Проект MADE, 1ый семестр (команда 4)

## Цель
создание платформы для ученых с рекомендательной системой интересных статей и потенциальных соавторов для будущих публикаций зарегистрированному пользователю (автору).

## Dataset

_**Citation Network Dataset**_ – [aminer.cn](https://www.aminer.cn/citation)

## Требования
Вам нужен `Python 3.9` (или более поздняя версия) для работы с пректом. Все требования к пакетам прописаны в `backend/requirements.txt`

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
    │   ├── build.sh            <- script for building DB
    │   │
    │   ├── run.sh              <- script for running DB
    │   │
    │   └── stop.sh             <- script to close DB   
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
