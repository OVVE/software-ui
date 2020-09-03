 
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


from typing import Any, Optional, Tuple, Union, TypeVar

from PyQt5.Qt import QSize, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QAbstractButton, QVBoxLayout, QHBoxLayout, QLabel

from display.ui_settings import (SimpleButtonSettings, FancyButtonSettings,
                                 DisplayRectSettings, PageSettings,
                                 TextSetting)
from utils.alarm_limits import AlarmLimits
from utils.alarm_limit_type import AlarmLimitType, AlarmLimitPair

MainWindow = TypeVar('MainWindow')


class AlarmLimitSelectorPair(QWidget):
    def __init__(self,
                 window: MainWindow,
                 alarmLimitPair: AlarmLimitPair,
                 parent=None):
        QWidget.__init__(self, parent=parent)
        self.page_settings = window.ui_settings.page_settings
        self.window = window
        self.properties = window.alarm_limit_pairs[alarmLimitPair]
        self.low_selector = window.alarmLimitSelectors[self.properties["low"]]
        self.high_selector = window.alarmLimitSelectors[
            self.properties["high"]]

        self.outer_layout = QHBoxLayout()
        self.inner_layouts = {}
        for loc in ["left", "mid", "right"]:
            self.inner_layouts[loc] = QVBoxLayout()

        self.tab_str = self.properties["short_name"]
        self.main_label = QLabel(self.properties["full_name"])
        self.styleMainLabel()

        self.inner_layouts["left"].addWidget(self.low_selector)
        self.inner_layouts["mid"].addWidget(self.main_label)
        self.inner_layouts["right"].addWidget(self.high_selector)

        for key in self.inner_layouts:
            self.inner_layouts[key].setAlignment(Qt.AlignCenter)
            self.outer_layout.addLayout(self.inner_layouts[key])

        self.setLayout(self.outer_layout)

    def styleMainLabel(self):
        self.main_label.setFont(self.page_settings.alarmLimitMainLabelFont)
        self.main_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_label.setWordWrap(True)
        self.main_label.setFixedHeight(150)


class AlarmLimitSelector(QWidget):
    def __init__(self,
                 window: MainWindow,
                 alarmLimitType: AlarmLimitType,
                 parent=None):
        QWidget.__init__(self, parent=parent)
        self.page_settings = window.ui_settings.page_settings
        button_settings = SimpleButtonSettings(
            fillColor=self.page_settings.changeButtonFillColor,
            borderColor=self.page_settings.changeButtonBorderColor,
            valueSetting=self.page_settings.changeButtonTextSetting,
            valueColor=self.page_settings.changeButtonValueColor)

        self.window = window
        self.alarmLimitType = alarmLimitType
        self.properties = window.alarm_limits[self.alarmLimitType]
        self.pair_selector = None
        self.warn_on_limit_value = True

        self.layout = QVBoxLayout()

        self.main_label = QLabel(self.properties["name"])
        self.styleMainLabel()

        self.dec_button = self.window.makePicButton("down")

        self.value_label = QLabel(
            str(
                round(self.window.settings.alarm_limit_values[
                    self.alarmLimitType])))
        self.styleValueLabel()

        self.inc_button = self.window.makePicButton("up")
        for widget in [
                self.inc_button, self.value_label, self.dec_button,
                self.main_label
        ]:
            wrapper = QHBoxLayout()
            wrapper.setAlignment(Qt.AlignCenter)
            wrapper.addWidget(widget)
            self.layout.addLayout(wrapper)

        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)
        self.connectOrHideButtons()

    def styleMainLabel(self):
        self.main_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
        self.main_label.setFont(self.page_settings.alarmLimitLabelFont)
        self.main_label.setAlignment(Qt.AlignLeft)
        self.main_label.setFixedWidth(300)

    def styleValueLabel(self):
        self.value_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
        self.value_label.setFont(self.page_settings.alarmLimitValueFont)
        self.value_label.setAlignment(Qt.AlignCenter)
        # self.value_label.setFixedWidth(100)

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
        if self.properties["settable"]:
            self.window.settings.alarm_limit_values[
                self.alarmLimitType] += self.properties["increment"]
            if self.properties["warning_limit"] is not None:
                if self.window.settings.alarm_limit_values[
                        self.
                        alarmLimitType] > self.properties["warning_limit"]:
                    if self.warn_on_limit_value:
                        self.window.warn(self.properties["warning_msg"], 10)
                        self.warn_on_limit_value = False
            self.updateValue()
            self.checkIfHideShowButtons()

    def decrementValue(self):
        # TODO: check warning limit
        if self.properties["settable"]:
            self.window.settings.alarm_limit_values[
                self.alarmLimitType] -= self.properties["increment"]
            if self.properties["warning_limit"] is not None:
                if self.window.settings.alarm_limit_values[
                        self.alarmLimitType] > self.properties["warning_limit"]:
                    if self.warn_on_limit_value:
                        self.window.warn(self.properties["warning_msg"], 10)
                        self.warn_on_limit_value = False
                else:
                   self.warn_on_limit_value = True
            self.updateValue()
            self.checkIfHideShowButtons()

    def checkIfHideShowButtons(self, rec_call=False):

        if self.properties["low"]:
            if self.properties["hard_limit"] is not None:

                if self.window.settings.alarm_limit_values[self.alarmLimitType] \
                        - self.properties["increment"] < self.properties["hard_limit"]:
                    self.dec_button.hide()

                else:
                    if self.properties["settable"]:
                        self.dec_button.show()

            if self.window.settings.alarm_limit_values[self.alarmLimitType] \
                    + self.properties["increment"] >= \
                    self.window.settings.alarm_limit_values[self.properties["pair"]]:

                self.inc_button.hide()

            else:
                if self.properties["settable"]:
                    self.inc_button.show()

        elif not self.properties["low"]:
            if self.properties["hard_limit"] is not None:

                if self.window.settings.alarm_limit_values[self.alarmLimitType] \
                        + self.properties["increment"] > self.properties["hard_limit"]:
                    self.inc_button.hide()

                else:
                    if self.properties["settable"]:
                        self.inc_button.show()

            if self.window.settings.alarm_limit_values[self.alarmLimitType] \
                    - self.properties["increment"] <= \
                    self.window.settings.alarm_limit_values[self.properties["pair"]]:

                self.dec_button.hide()

            else:
                if self.properties["settable"]:
                    self.dec_button.show()

        if self.pair_selector is not None and not rec_call:
            self.pair_selector.checkIfHideShowButtons(True)

    def setPairSelector(self):
        self.pair_selector = self.window.alarmLimitSelectors[
            self.properties["pair"]]

    def updateValue(self):
        self.value_label.setText(
            str(
                round(self.window.settings.alarm_limit_values[
                    self.alarmLimitType])))
        self.value_label.update()
        self.window.passChanges()
