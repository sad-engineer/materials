#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from materials.obj.terminal_printer import TerminalPrinter as _Terminal


class Logger:
    """ Передает в конкретный логгер объект вывода """
    @staticmethod
    def log(obj, notifier=_Terminal, message=None, path=None):
        return notifier().log(obj, message, path)
