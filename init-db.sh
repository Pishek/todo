#!/bin/bash
set -e

# Создаем вторую базу данных для sqlalchemy
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $DB_SECOND_NAME;
EOSQL