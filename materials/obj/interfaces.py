#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union

from service import CheckerInDictionary
from service import InvalidValue
from service import Dictionarer

from materials.obj.constants import WORKPIECE, HEAT_TREATMENT


class IWorkpiece(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с типом поверхности заготовки

        Parameters:
            workpiece : (str, int) : тип поверхности заготовки.

        Сostants:
            WORKPIECE : Описание типов поверхности заготовки
        """
    WORKPIECE: ClassVar[dict] = WORKPIECE

    def __init__(self, workpiece: Union[str, int, float]) -> None:
        self._workpiece = None
        self.workpiece = workpiece

    @property
    def workpiece(self) -> None:
        return self._workpiece

    @workpiece.setter
    def workpiece(self, any_workpiece) -> None:
        err_message = f'Неверное значение типа поверхности инструмента. Значение должно быть из {self.WORKPIECE}.\n ' \
                      f'Передано {any_workpiece}.'
        any_workpiece = self._check_in_dict(any_workpiece, self.WORKPIECE, err_message)
        self._workpiece = any_workpiece if isinstance(any_workpiece, str) else self.WORKPIECE[any_workpiece]

    def _parameters(self) -> dict:
        return {"workpiece": self._workpiece}


class IHrc(Dictionarer):
    """ Интерфейс работы с твердостью после термообработки

    Parameters:
        hrc : (int >= 0) : твердость после термообработки по системе HRC.
    """
    def __init__(self, hrc: Union[int, float]) -> None:
        self._hrc = None
        self.hrc = hrc

    @property
    def hrc(self) -> None:
        return self._hrc

    @hrc.setter
    def hrc(self, any_hrc) -> None:
        if not isinstance(any_hrc, int) or any_hrc < 0:
            raise InvalidValue(f'Количество должно быть целым положительным числом (передано {any_hrc})')
        self._hrc = any_hrc

    def _parameters(self) -> dict:
        return {"hrc": self._hrc}


class IHeatTreatment(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с типом термообработки

        Parameters:
            heat_treatment : (str, int) : Тип термообработки.

        Сostants:
            WORKPIECE : Описание типов поверхности заготовки
        """
    HEAT_TREATMENT: ClassVar[dict] = HEAT_TREATMENT

    def __init__(self, heat_treatment: Union[str, int, float]) -> None:
        self._heat_treatment = None
        self.heat_treatment = heat_treatment

    @property
    def heat_treatment(self) -> None:
        return self._heat_treatment

    @heat_treatment.setter
    def heat_treatment(self, any_heat_treatment) -> None:
        err_message = f'Неверное значение типа поверхности инструмента. Значение должно быть из ' \
                      f'{self.HEAT_TREATMENT}.\n Передано {any_heat_treatment}.'
        any_heat_treatment = self._check_in_dict(any_heat_treatment, self.HEAT_TREATMENT, err_message)
        self._heat_treatment = any_heat_treatment if isinstance(any_heat_treatment, str) \
            else self.HEAT_TREATMENT[any_heat_treatment]

    def _parameters(self) -> dict:
        return {"heat_treatment": self._heat_treatment}

