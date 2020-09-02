 
# Copyright 2020 LifeMech  Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


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
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label_label = QLabel(self.label)
        self.value_label = QLabel(str(self.value))
        self.unit_label = QLabel(self.unit)

        self.label_label.setFont(self.button_settings.labelFont)
        self.label_label.setAlignment(Qt.AlignCenter)
        self.label_label.setStyleSheet("QLabel {color: " +
                                       self.button_settings.labelColor + ";}")
        self.label_label.setMargin(0)
        self.layout.addWidget(self.label_label)

        self.value_label.setFont(self.button_settings.valueFont)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("QLabel {color: " +
                                       self.button_settings.valueColor + ";}")
        self.value_label.setMargin(-10)
        self.layout.addWidget(self.value_label)
        self.value_label.setFixedWidth(self.size[0])

        self.unit_label.setFont(self.button_settings.unitFont)
        self.unit_label.setAlignment(Qt.AlignCenter)
        self.unit_label.setStyleSheet("QLabel {color: " +
                                      self.button_settings.unitColor +
                                      "; margin-top: -100px;}")
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
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setGeometry(QRect(0, 0, *self.size))

        self.value_label.setFont(self.button_settings.valueFont)
        self.value_label.setStyleSheet("QLabel {color: " +
                                       self.button_settings.valueColor + ";}")
        self.value_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.value_label)
        self.layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.layout)

    def update(self):
        self.value_label.setFont(self.button_settings.valueFont)
        self.value_label.setStyleSheet("QLabel {color: " +
                                       self.button_settings.valueColor + ";}")
        self.value_label.update()
        super().update()

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


class PicButton(QAbstractButton):
    def __init__(self,
                 file: str,
                 size: Optional[Tuple[int, int]] = None,
                 parent: Optional[Any] = None):
        super().__init__(parent)
        self.pixmap = QPixmap(file)
        self.size = size

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setPen(QPen(QColor("#000000")))
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        if self.size is not None:
            painter.drawPixmap(QRect(0, 0, *self.size), self.pixmap)
        else:
            painter.drawPixmap(self.pixmap)

    def sizeHint(self):
        if self.size is not None:
            return QSize(*self.size)
        else:
            return self.pixmap.size()

    def updateValue(self, file: str):
        self.pixmap = QPixmap(file)
        self.update()
