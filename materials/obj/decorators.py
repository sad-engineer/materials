#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import inspect


def inheritdocstring(cls):
    for base in inspect.getmro(cls):
        if base.__doc__ is not None:
            cls.__doc__ = base.__doc__
            break
    return cls
