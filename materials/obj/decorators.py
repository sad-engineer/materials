#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from datetime import datetime
from functools import wraps
import logging


def timeit(message: str):
    def outer(func):
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            time = datetime.now() - start
            print(message.format(time))
            return result
        return wrapper
    return outer


def timeit_property(message: str):
    def outer_property(cls):
        def wrapper(property_name):
            start = datetime.now()
            result = getattr(cls, property_name)
            time = datetime.now() - start
            print(message.format(time))
            return result
        return wrapper
    return outer_property


def logged(cls=None, *, name=""):
    """ Создает обьекты логгера (например: self.debug, self.info, и т.д) для вывода сообщений логирования"""
    def logged_for_init(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            logger_name = name or self.__class__.__name__
            self.log = logging.getLogger(logger_name)
            for method_name in ('debug', 'info', 'warning', 'error',
                                'critical', 'exception'):
                method = getattr(self.log, method_name)
                setattr(self, method_name, method)
            return func(self, *args, **kwargs)
        return wrapper

    def wrap(cls):
        cls.__init__ = logged_for_init(cls.__init__)
        return cls

    return wrap if cls is None else wrap(cls)
