#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod


class Notifier(ABC):
    """ Абстрактный класс, базовый для всех логгеров или классов вывода результата"""
    @abstractmethod
    def log(self, obj, message, path): return path
