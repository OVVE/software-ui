from typing import Any, Optional, Tuple, Union, TypeVar

from PyQt5.Qt import QSize, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QAbstractButton, QVBoxLayout, QHBoxLayout, QLabel

from display.ui_settings import (SimpleButtonSettings, FancyButtonSettings,
                                 DisplayRectSettings, PageSettings,
                                 TextSetting)
from utils.alarm_limits import AlarmLimits
from utils.alarm_limit_type import AlarmLimitType


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
        self.alarmLimitType = alarmLimitType
        self.properties = window.alarm_limits[self.alarmLimitType]

        self.outer_layout = QHBoxLayout()
        self.left_inner_layout =  QHBoxLayout()
        self.right_inner_layout =  QHBoxLayout()

        self.main_label = QLabel(self.properties["name"])
        self.styleMainLabel()

        self.dec_button = self.window.makeSimpleDisplayButton(
            "-",
            size=(50, 50),
            button_settings=button_settings)

        self.value_label = QLabel(str(round(self.window.settings.alarm_limit_values[self.alarmLimitType])))
        self.styleValueLabel()

        self.inc_button = self.window.makeSimpleDisplayButton(
            "+",
            size=(50, 50),
            button_settings=button_settings)



        self.left_inner_layout.addWidget(self.main_label)
        for widget in [self.dec_button, self.value_label, self.inc_button]:
            self.right_inner_layout.addWidget(widget)


        for inner_layout in [self.left_inner_layout, self.right_inner_layout]:
            inner_layout.setAlignment(Qt.AlignCenter)
            self.outer_layout.addLayout(inner_layout)



        self.setFixedHeight(65)
        self.outer_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.outer_layout)
        self.connectOrHideButtons()


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
        dec_size_policy = self.dec_button.sizePolicy()
        dec_size_policy.setRetainSizeWhenHidden(True)

        inc_size_policy = self.dec_button.sizePolicy()
        inc_size_policy.setRetainSizeWhenHidden(True)

        self.dec_button.setSizePolicy(dec_size_policy)
        self.inc_button.setSizePolicy(inc_size_policy)

        if self.properties["settable"]:
            self.dec_button.clicked.connect(self.decrementValue)
            self.inc_button.clicked.connect(self.incrementValue)
            self.checkIfHideShowButtons()

        else:
            self.inc_button.hide()
            self.dec_button.hide()

    def incrementValue(self):
        # TODO: check hard limit
        # TODO: check warning limit
        if self.properties["settable"]:
            self.window.settings.alarm_limit_values[self.alarmLimitType]+=self.properties["increment"]
            self.updateValue()
            self.checkIfHideShowButtons()

    def decrementValue(self):
        # TODO: check hard limit
        # TODO: check warning limit
        if self.properties["settable"]:
            self.window.settings.alarm_limit_values[self.alarmLimitType]-=self.properties["increment"]
            self.updateValue()
            self.checkIfHideShowButtons()

    def checkIfHideShowButtons(self):
        if self.properties["hard_limit"] is not None:

            if self.properties["low"]:
                if self.window.settings.alarm_limit_values[self.alarmLimitType] \
                        - self.properties["increment"] < self.properties["hard_limit"]:
                    self.dec_button.hide()

                else:
                    if self.properties["settable"]:
                        if not self.dec_button.isVisible():
                            self.dec_button.show()


            elif not self.properties["low"]:
                if self.window.settings.alarm_limit_values[self.alarmLimitType] \
                        + self.properties["increment"] > self.properties["hard_limit"]:
                    self.inc_button.hide()


                else:
                    if self.properties["settable"]:
                        if not self.inc_button.isVisible():
                            self.inc_button.show()


    def updateValue(self):
        self.value_label.setText(str(round(self.window.settings.alarm_limit_values[self.alarmLimitType])))
        self.value_label.update()
        self.window.passChanges()


