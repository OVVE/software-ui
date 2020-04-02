"""

"""
from typing import Any
from typing import Optional
from typing import Tuple
from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.Qt import QWidget
from PyQt5.Qt import QSize
from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPen


class DisplayRect(QWidget):
    def __init__(self,
                 label: str,
                 value: Union[int, float],
                 unit: str,
                 parent: Optional[Any] = None,
                 size: Tuple[int, int] = (200, 100)) -> None:
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.size = size

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        label_font = QFont("Times", 20, QFont.Bold)
        number_font = QFont("Times", 36, QFont.Bold)
        unit_font = QFont("Times", 18)

        painter.setBrush(QBrush(QColor("#c4dbff")))
        painter.drawRect(0, 0, *self.size)
        painter.setPen(QPen(QColor("#3ed5f0")))
        painter.setFont(label_font)
        painter.drawText(int(self.size[0] / 2 - 50), int(self.size[1] / 5),
                         self.label)
        painter.setPen(QPen(Qt.black))
        painter.setFont(number_font)
        painter.drawText(int(self.size[0] / 2 - 50), int(3 * self.size[1] / 5),
                         str(self.value))
        painter.setFont(unit_font)
        painter.setPen(QPen(Qt.gray))
        painter.drawText(int(self.size[0] / 2 - 50),
                         int(self.size[1] * 9 / 10), str(self.unit))

    def sizeHint(self) -> QSize:
        return QSize(*self.size)

    def updateValue(self, value: Union[int, float]) -> None:
        self.value = value
        self.update()
