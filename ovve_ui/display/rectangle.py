"""

"""
from typing import Any, Optional, Tuple, Union

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PySide2.QtWidgets import QAbstractButton, QWidget

from display.ui_settings import DisplayRectSettings


class DisplayRect(QWidget):
    def __init__(self,
                 label: str,
                 value: Union[int, float],
                 unit: str,
                 rect_settings: DisplayRectSettings,
                 parent: Optional[Any] = None,
                 size: Optional[Tuple[int, int]] = None):
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.rect_settings = rect_settings
        self.size = size if size is not None else rect_settings.default_size

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        label_font = self.rect_settings.labelFont
        value_font = self.rect_settings.valueFont
        unit_font = self.rect_settings.unitFont

        painter.setBrush(self.rect_settings.getFillBrush())
        painter.drawRect(0, 0, *self.size)
        painter.setPen(self.rect_settings.getLabelPen())
        painter.setFont(label_font)
        painter.drawText(*self.rect_settings.getLabelCoords(), self.label)
        painter.setPen(self.rect_settings.getValuePen())
        painter.setFont(value_font)
        painter.drawText(*self.rect_settings.getValueCoords(), str(self.value))
        painter.setFont(unit_font)
        painter.setPen(self.rect_settings.getUnitPen())
        painter.drawText(*self.rect_settings.getUnitCoords(), str(self.unit))

    def sizeHint(self) -> QSize:
        return QSize(*self.size)

    def updateValue(self, value: Union[int, float]) -> None:
        self.value = value
        self.update()
