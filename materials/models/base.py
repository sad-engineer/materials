#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет базовый класс `Base` для всех моделей базы данных, используемых в проекте. `Base` создается с
помощью функции `declarative_base()` из SQLAlchemy и служит основой для всех таблиц в базе данных.

`Base` используется для определения классов, представляющих таблицы в базе данных. Все модели в проекте должны
наследовать этот базовый класс, чтобы SQLAlchemy мог автоматически управлять созданием, изменением и удалением таблиц.

Использование:
Создание новой модели, наследующей `Base`, может выглядеть следующим образом:

    from .base import Base
    from sqlalchemy import Column, Integer, String

    class ExampleModel(Base):
        __tablename__ = 'example'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String, nullable=False)

Таким образом, каждая модель наследует `Base`, и SQLAlchemy знает, что она представляет таблицу в базе данных.

`Base.metadata.create_all(bind=engine)` используется для создания всех таблиц, определенных моделями, наследующими
`Base`.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
