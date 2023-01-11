#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import datetime

from materials.obj.notifier import Notifier
from materials.obj.constants import DECODING


class FilePrinter(Notifier):
    """ Выводит результат в файл"""
    def __init__(self):
        # Настройки по умолчанию. Расположение лога определять вне класса.
        self.prefix = datetime.datetime.now().strftime('%H-%M %d-%m-%Y')
        self.path = f"{__file__}".replace("obj\\file_printer.py", f"logs\\{self.prefix}_log.txt")

    def log(self, obj, message=None, path=None):
        if isinstance(path, type(None)):
            path = self.path
        with open(path, 'a+', encoding='UTF8') as f:
            f.write(f"{message}\n")
            for key, val in obj.__dict__.items():
                f.write(f"{DECODING[key].format(obj=val)}\n") if key in DECODING else f.write(f"{key} = {val}\n")
            return path
