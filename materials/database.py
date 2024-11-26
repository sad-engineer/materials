#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет конфигурацию подключения к базе данных для проекта, используя SQLAlchemy.
Он включает в себя создание движка для взаимодействия с базой данных, создание фабрики сессий для работы с базой данных
и определение базового класса `Base`, от которого наследуются все модели.

Компоненты модуля:
- `DATABASE_URL` (str): Строка подключения к базе данных. В данном случае используется SQLite, файл базы данных
называется `materials1.db`.
- `engine` (Engine): Движок базы данных, создающий подключение к базе данных и позволяющий выполнять SQL-запросы.
- `SessionLocal` (sessionmaker): Фабрика сессий, которая используется для создания объектов сессии, позволяющих
взаимодействовать с базой данных.
- `Base` (declarative_base): Базовый класс для всех моделей базы данных. Все модели проекта наследуют этот класс.

Использование:
Модуль `database.py` предоставляет все необходимые компоненты для подключения и работы с базой данных. Пример
использования для создания новой сессии:

    from materials.database import SessionLocal

    # Создание новой сессии
    db = SessionLocal()
    try:
        # Выполнение операций с базой данных
        ...
    finally:
        # Закрытие сессии после использования
        db.close()

Также модуль определяет движок `engine`, который может быть использован для создания всех таблиц, определенных в
 моделях, например:

    from materials.database import engine, Base
    from materials.models import *  # Импорт всех моделей

    # Создание всех таблиц в базе данных
    Base.metadata.create_all(bind=engine)

Эта команда создаст все таблицы, определенные в моделях, если они еще не существуют в базе данных.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from materials.models import Base

# Чтение значения для echo из переменной окружения
ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() in ["true", "1"]

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///materials.db")

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL, echo=ECHO)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц на основе моделей
Base.metadata.create_all(bind=engine)
