"""

"""
from typing import Any, Optional, Tuple, Union

from PyQt5.Qt import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QAbstractButton

from display.ui_settings import FancyButtonSettings, SimpleButtonSettings


class FancyDisplayButton(QAbstractButton):
    def __init__(self,
                 label: str,
                 value: Union[int, float],
                 unit: str,
                 button_settings: FancyButtonSettings,
                 parent: Optional[Any] = None,
                 size: Optional[Tuple[int, int]] = None):
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.button_settings = button_settings
        self.size = size if size is not None else button_settings.default_size

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        label_font = self.button_settings.labelFont
        value_font = self.button_settings.valueFont
        unit_font = self.button_settings.unitFont

        painter.setBrush(self.button_settings.getFillBrush())
        painter.drawRect(0, 0, *self.size)
        painter.setPen(self.button_settings.getLabelPen())
        painter.setFont(label_font)
        painter.drawText(*self.button_settings.getLabelCoords(), self.label)
        painter.setPen(self.button_settings.getValuePen())
        painter.setFont(value_font)
        painter.drawText(*self.button_settings.getValueCoords(),
                         str(self.value))
        painter.setFont(unit_font)
        painter.setPen(self.button_settings.getUnitPen())
        painter.drawText(*self.button_settings.getUnitCoords(), str(self.unit))

    def sizeHint(self) -> QSize:
        return QSize(*self.size)

    def updateValue(self, value: Union[int, float]) -> None:
        self.value = value
        self.update()


class SimpleDisplayButton(QAbstractButton):
    def __init__(self,
                 value: Union[int, float],
                 button_settings: SimpleButtonSettings,
                 parent: Optional[Any] = None,
                 size: Optional[Tuple[int, int]] = None):
        super().__init__(parent)
        self.value = value
        self.button_settings = button_settings
        self.size = size if size is not None else button_settings.default_size

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        value_font = self.button_settings.valueFont

        painter.setBrush(self.button_settings.getFillBrush())
        painter.drawRect(0, 0, *self.size)
        painter.setPen(self.button_settings.getValuePen())
        painter.setFont(value_font)
        painter.drawText(*self.button_settings.getValueCoords(),
                         str(self.value))

    def sizeHint(self) -> QSize:
        return QSize(*self.size)

    def updateValue(self, value: Union[int, float]) -> None:
        self.value = value
        self.update()
