"""

"""
from typing import Any, Optional, Tuple, Union

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PySide2.QtWidgets import QAbstractButton, QWidget, QVBoxLayout, QLabel

from display.ui_settings import DisplayRectSettings


class DisplayRect(QWidget):
    def __init__(self,
                 label: str,
                 value: Union[int, float, str],
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

        self.layout = QVBoxLayout()

        self.label_label = QLabel(self.label)
        self.value_label = QLabel(str(self.value))
        self.unit_label = QLabel(self.unit)

        self.label_label.setFont(self.rect_settings.labelFont)
        self.label_label.setAlignment(Qt.AlignCenter)
        self.label_label.setStyleSheet("QLabel {color: " +
                                       self.rect_settings.labelColor +
                                       "; margin-top: 6px;}")
        self.layout.addWidget(self.label_label)

        self.value_label.setFont(self.rect_settings.valueFont)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setMargin(-10)
        self.value_label.setStyleSheet("QLabel {color: " +
                                       self.rect_settings.valueColor + ";}")
        self.value_label.setFixedWidth(self.size[0])
        self.layout.addWidget(self.value_label)

        self.unit_label.setFont(self.rect_settings.unitFont)
        self.unit_label.setAlignment(Qt.AlignCenter)
        self.unit_label.setStyleSheet("QLabel {color: " +
                                      self.rect_settings.unitColor + ";}")
        self.layout.addWidget(self.unit_label)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.setBrush(self.rect_settings.getFillBrush())
        painter.setPen(self.rect_settings.getBorderPen())
        painter.drawRect(0, 0, *self.size)

    def sizeHint(self) -> QSize:
        return QSize(*self.size)

    def updateValue(self, value: Union[int, float, str]) -> None:
        self.value = value
        self.value_label.setText(str(value))
        self.update()
