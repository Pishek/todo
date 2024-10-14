# Todo Application

This project consists of two main applications:

1. **todo** - A Django Rest Framework (DRF) based application.
2. **todo_monitor** - Kafka consumers based on `aiokafka` and `SQLAlchemy 2.0`.

## Technology Stack

### todo
- **Framework**: Django Rest Framework (DRF)
- **Kafka Producer**: Confluent Kafka

### todo_monitor
- **Database**: postgres, SQLAlchemy 2.0
- **Kafka Consumer**: aiokafka
- **Data Validation**: Pydantic 2.0

## Functionality Overview

### todo Application
- User authentication (registration, login, and logout).
- Task creation and management.
- When a task is completed, a message is produced and sent to a Kafka topic.

### todo_monitor Application
There are two consumer groups:

- **Group 1**: Contains one consumer that reads messages from a Kafka topic and logs information about the completed task.
- **Group 2**: Contains two consumers that track the number of tasks completed or failed by the user.


### env
в docker-compose.yaml в сервисе db задать имя для баз данных, затем перейти к файлам .envexample и apps/todo_monitor/.envexample проставить  соответсвующие имена бд, если необходимо.

### swagger
http://localhost:8000/docs/

### Start the project
```bash
make start
