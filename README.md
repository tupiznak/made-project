# MADE project (team 4)

## Main goal
is to create a platform for scientists with recommendation algorithms of interesting articles and perspective co-author for future articles to registered author (user).

## Dataset

_**Citation Network Dataset**_ – [aminer.cn](https://www.aminer.cn/citation)

## Requirements
You need `Python 3.9` or later for running the project. All packages requirements are described in `backend/requirements.txt`

## Organization
Project is organized as follows:

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

## Running database
Go to `/docker` and run scripts `build.sh` and `run.sh` sequentially.

After finishin your work with database run `stop.sh`.
