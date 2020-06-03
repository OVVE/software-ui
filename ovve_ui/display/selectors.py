from typing import Any, Optional, Tuple, Union, TypeVar

from PyQt5.Qt import QSize, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QAbstractButton, QVBoxLayout, QHBoxLayout, QLabel

from display.ui_settings import (SimpleButtonSettings, FancyButtonSettings,
                                 DisplayRectSettings, PageSettings,
                                 TextSetting)
from utils.alarm_limits import AlarmLimits, AlarmLimitType

MainWindow = TypeVar('MainWindow')

class AlarmLimitSelector(QWidget):
    def __init__(self,  window: MainWindow, alarmLimitType: AlarmLimitType, parent = None):
        QWidget.__init__(self, parent=parent)
        self.page_settings = window.ui_settings.page_settings
        button_settings = SimpleButtonSettings(
                fillColor= self.page_settings.changeButtonFillColor,
                borderColor=self.page_settings.changeButtonBorderColor,
                valueSetting=self.page_settings.changeButtonTextSetting,
                valueColor=self.page_settings.changeButtonValueColor)

        self.window = window
        self.properties = window.alarm_limits[alarmLimitType]

        self.outer_layout = QHBoxLayout()
        self.left_inner_layout =  QHBoxLayout()
        self.right_inner_layout =  QHBoxLayout()

        self.main_label = QLabel(self.properties["name"])
        self.styleMainLabel()

        self.dec_button = self.window.makeSimpleDisplayButton(
            "-",
            size=(50, 50),
            button_settings=button_settings)

        self.value_label = QLabel(str(self.properties["value"]))
        self.styleValueLabel()

        self.inc_button = self.window.makeSimpleDisplayButton(
            "+",
            size=(50, 50),
            button_settings=button_settings)
        self.connectOrHideButtons()

        self.left_inner_layout.addWidget(self.main_label)
        for widget in [self.dec_button, self.value_label, self.inc_button]:
            self.right_inner_layout.addWidget(widget)


        for inner_layout in [self.left_inner_layout, self.right_inner_layout]:
            inner_layout.setAlignment(Qt.AlignCenter)
            self.outer_layout.addLayout(inner_layout)

        self.setFixedHeight(65)
        self.outer_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.outer_layout)

    def styleMainLabel(self):
        self.main_label.setStyleSheet("QLabel {color: #000000 ;}")
        self.main_label.setFont(self.page_settings.alarmLimitLabelFont)
        self.main_label.setAlignment(Qt.AlignLeft)
        self.main_label.setFixedWidth(300)

    def styleValueLabel(self):
        self.value_label.setStyleSheet("QLabel {color: #000000 ;}")
        self.value_label.setFont(self.page_settings.alarmLimitValueFont)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setFixedWidth(100)

    def connectOrHideButtons(self):
        inc_dec_size_policy = self.dec_button.sizePolicy()
        inc_dec_size_policy.setRetainSizeWhenHidden(True)
        self.dec_button.setSizePolicy(inc_dec_size_policy)
        self.inc_button.setSizePolicy(inc_dec_size_policy)

        if self.properties["settable"]:
            self.dec_button.clicked.connect(self.decrementValue)
            self.inc_button.clicked.connect(self.incrementValue)

        else:
            self.inc_button.hide()
            self.dec_button.hide()

    def incrementValue(self):
        # TODO: check hard limit
        # TODO: check warning limit
        if self.properties["settable"]:
            self.properties["value"]+=self.properties["increment"]
            self.updateValue()

    def decrementValue(self):
        # TODO: check hard limit
        # TODO: check warning limit
        if self.properties["settable"]:
            self.properties["value"]-=self.properties["increment"]
            self.updateValue()


    def updateValue(self):
        self.value_label.setText(str(self.properties["value"]))
        self.value_label.update()
        self.window.passChanges()


