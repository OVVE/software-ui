from typing import Any, Optional, Tuple, Union, TypeVar

from PyQt5.Qt import QSize, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QAbstractButton, QVBoxLayout, QHBoxLayout, QLabel

from display.ui_settings import (SimpleButtonSettings, FancyButtonSettings,
                                 DisplayRectSettings, PageSettings,
                                 TextSetting)

MainWindow = TypeVar('MainWindow')

class AlarmLimitSelector(QWidget):
    def __init__(self,  window: MainWindow, main_label_text, value, dec_func, inc_func, parent = None):
        QWidget.__init__(self, parent=parent)
        page_settings = window.ui_settings.page_settings
        button_settings = SimpleButtonSettings(
                fillColor= page_settings.changeButtonFillColor,
                borderColor=page_settings.changeButtonBorderColor,
                valueSetting=page_settings.changeButtonTextSetting,
                valueColor=page_settings.changeButtonValueColor)

        self.main_label_text = main_label_text
        self.value = value
        self.dec_func = dec_func
        self.inc_func = inc_func
        self.outer_layout = QHBoxLayout()
        self.left_inner_layout =  QHBoxLayout()
        self.right_inner_layout =  QHBoxLayout()


        self.main_label = QLabel(self.main_label_text)

        self.main_label.setStyleSheet("QLabel {color: #000000 ;}")
        self.main_label.setFont(page_settings.alarmLimitLabelFont)
        self.main_label.setAlignment(Qt.AlignLeft)
        self.main_label.setFixedWidth(300)

        self.dec_button = window.makeSimpleDisplayButton(
            "-",
            size=(50, 50),
            button_settings=button_settings)
        self.dec_button.clicked.connect(self.dec_func)

        self.value_label = QLabel(str(self.value))

        self.value_label.setStyleSheet("QLabel {color: #000000 ;}")
        self.value_label.setFont(page_settings.alarmLimitValueFont)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setFixedWidth(100)

        self.inc_button = window.makeSimpleDisplayButton(
            "+",
            size=(50, 50),
            button_settings=button_settings)
        self.inc_button.clicked.connect(self.inc_func)


        self.left_inner_layout.addWidget(self.main_label)
        for widget in [self.dec_button, self.value_label, self.inc_button]:
            self.right_inner_layout.addWidget(widget)


        for inner_layout in [self.left_inner_layout, self.right_inner_layout]:
            inner_layout.setAlignment(Qt.AlignCenter)
            self.outer_layout.addLayout(inner_layout)

        self.setFixedHeight(65)
        self.outer_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.outer_layout)

    def updateValue(self, value: int):
        self.value = value
        self.value_label.setText(str(self.value))
        self.value_label.update()


