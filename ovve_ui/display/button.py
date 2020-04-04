"""

"""
from typing import Any, Optional, Tuple, Union

from PyQt5.Qt import QSize
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAbstractButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget
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

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.label_label = QLabel(self.label)
        self.value_label = QLabel(str(self.value))
        self.unit_label = QLabel(self.unit)

        self.label_label.setFont(self.button_settings.labelFont)
        self.label_label.setAlignment(Qt.AlignCenter)
        self.label_label.setStyleSheet("QLabel {color: " + self.button_settings.labelColor + ";}")
        self.label_label.setMargin(0)
        self.layout.addWidget(self.label_label)

        self.value_label.setFont(self.button_settings.valueFont)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("QLabel {color: " + self.button_settings.valueColor + ";}")
        self.value_label.setMargin(-10)
        self.layout.addWidget(self.value_label)

        self.unit_label.setFont(self.button_settings.unitFont)
        self.unit_label.setAlignment(Qt.AlignCenter)
        self.unit_label.setStyleSheet("QLabel {color: " + self.button_settings.unitColor + "; margin-top: -100px;}")
        self.layout.addWidget(self.unit_label)


        self.setLayout(self.layout)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.setPen(self.button_settings.getBorderPen())
        painter.setBrush(self.button_settings.getFillBrush())
        painter.drawRect(0, 0, *self.size)


    def sizeHint(self) -> QSize:
        return QSize(*self.size)

    def updateValue(self, value: Union[int, float]) -> None:
        self.value = value
        self.value_label.setText(str(value))
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

        self.value_label = QLabel(value)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setGeometry(QRect(0,0, *self.size))

        self.value_label.setFont(self.button_settings.valueFont)
        self.value_label.setStyleSheet("QLabel {color: " + self.button_settings.valueColor + ";}")

        self.layout.addWidget(self.value_label)
        self.layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.layout)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.setBrush(self.button_settings.getFillBrush())
        painter.setPen(self.button_settings.getBorderPen())
        painter.drawRect(0, 0, *self.size)


    def sizeHint(self) -> QSize:
        return QSize(*self.size)

    def updateValue(self, value: Union[int, float]) -> None:
        self.value = value
        self.value_label.setText(str(value))
        self.update()
