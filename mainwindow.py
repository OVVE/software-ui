# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
from typing import Dict

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from widgets import AquaWidgets


class UIMainWindow():
    def __init__(self) -> None:
        self.central_widget = None
        self.grid_layout = None
        self.widgets = AquaWidgets()
        self.menubar = None
        self.statusbar = None

    def setup_ui(self, main_window) -> None:
        main_window.setObjectName("MainWindow")
        main_window.resize(1200, 855)
        spacer_item = {
            "0": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "1": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "2": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "3": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "4": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "5": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "6": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "7": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "8": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "9": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "10": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "11": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "12": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "13": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "14": QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),
            "15": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "16": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
            "17": QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),
        }

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("centralwidget")
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("gridLayout")
        self.grid_layout.addItem(spacer_item["0"], 9, 1, 1, 1)
        self.grid_layout.addItem(spacer_item["1"], 11, 1, 1, 1)

        # Set Widgets
        self._set_mode_widget()
        self._set_peep_widget()
        self._set_peak_widget()
        self._set_plateau_pressue_widget()
        self._set_tidal_volume_widget(spacer_item)
        self._set_ie_ratio_widget(spacer_item)
        self._set_fio2_widget(spacer_item)
        self._set_respitory_rate_widget(spacer_item)

        # Set Central Widget
        main_window.setCentralWidget(self.central_widget)

        # Set Menu and Status Bar
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def _set_mode_widget(self) -> None:
        """ Set Mode Label and Button """
        self.widgets.mode["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.mode["label"].setObjectName("mode_label")
        self.grid_layout.addWidget(self.widgets.mode["label"], 1, 0, 1, 1)

        self.widgets.mode["button"] = QtWidgets.QPushButton(self.central_widget)
        self.widgets.mode["button"].setCheckable(True)
        self.widgets.mode["button"].setObjectName("mode_button")
        self.grid_layout.addWidget(self.widgets.mode["button"], 1, 2, 1, 1)

    def _set_peep_widget(self) -> None:
        """ Set PEEP Label and LCD """ 
        self.widgets.peep["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.peep["label"].setObjectName("peep_label")
        self.grid_layout.addWidget(self.widgets.peep["label"], 3, 0, 1, 1)

        self.widgets.peep["lcd"] = QtWidgets.QLCDNumber(self.central_widget)
        self.widgets.peep["lcd"].setObjectName("peep_lcd")
        self.grid_layout.addWidget(self.widgets.peep["lcd"], 3, 2, 1, 1)

    def _set_peak_widget(self) -> None:
        """ Peak Press Label and LCD """
        self.widgets.peak_press["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.peak_press["label"].setObjectName("peak_press_label")
        self.grid_layout.addWidget(self.widgets.peak_press["label"], 5, 0, 1, 1)

        self.widgets.peak_press["lcd"] = QtWidgets.QLCDNumber(self.central_widget)
        self.widgets.peak_press["lcd"].setObjectName("peak_press_lcd")
        self.grid_layout.addWidget(self.widgets.peak_press["lcd"], 5, 2, 1, 1)

    def _set_plateau_pressue_widget(self) -> None:
        # Plateau Press Label and LCD
        self.widgets.plateau_press["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.plateau_press["label"].setObjectName("plateau_press_label")
        self.grid_layout.addWidget(self.widgets.plateau_press["label"], 7, 0, 1, 1)

        self.widgets.plateau_press["lcd"] = QtWidgets.QLCDNumber(self.central_widget)
        self.widgets.plateau_press["lcd"].setObjectName("plateau_press_lcd")
        self.grid_layout.addWidget(self.widgets.plateau_press["lcd"], 7, 2, 1, 1)

    def _set_tidal_volume_widget(self, spacer_item: Dict) -> None:
        """ Set Tidal Volume Label, LCD, SLIDER """
        self.widgets.tv["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.tv["label"].setObjectName("tv_label")
        self.grid_layout.addWidget(self.widgets.tv["label"], 9, 0, 1, 1)
        self.grid_layout.addItem(spacer_item["8"], 15, 4, 1, 1)

        self.widgets.tv["lcd"] = QtWidgets.QLCDNumber(self.central_widget)
        self.widgets.tv["lcd"].setObjectName("tv_lcd")
        self.grid_layout.addWidget(self.widgets.tv["lcd"], 9, 2, 1, 1)
        self.grid_layout.addItem(spacer_item["10"], 0, 2, 1, 1)
        self.grid_layout.addItem(spacer_item["11"], 12, 2, 1, 1)

        self.widgets.tv["slider"] = QtWidgets.QSlider(self.central_widget)
        self.widgets.tv["slider"].setOrientation(QtCore.Qt.Horizontal)
        self.widgets.tv["slider"].setObjectName("tv_slider")
        self.grid_layout.addWidget(self.widgets.tv["slider"], 9, 3, 1, 1)
        self.grid_layout.addItem(spacer_item["16"], 14, 2, 1, 1)
        self.grid_layout.addItem(spacer_item["17"], 16, 2, 1, 1)

    def _set_ie_ratio_widget(self, spacer_item: Dict) -> None:
        """ Set IE ratio Label, LCD, and Slider """
        self.widgets.ie["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.ie["label"].setObjectName("ie_label")
        self.grid_layout.addWidget(self.widgets.ie["label"], 11, 0, 1, 1)

        self.widgets.ie["lcd"] = QtWidgets.QLCDNumber(self.central_widget)
        self.widgets.ie["lcd"].setObjectName("ie_lcd")
        self.grid_layout.addWidget(self.widgets.ie["lcd"], 11, 2, 1, 1)
        self.grid_layout.addItem(spacer_item["12"], 10, 2, 1, 1)
        self.grid_layout.addItem(spacer_item["13"], 4, 2, 1, 1)
        self.grid_layout.addItem(spacer_item["14"], 5, 1, 1, 1)

        self.widgets.ie["slider"] = QtWidgets.QSlider(self.central_widget)
        self.widgets.ie["slider"].setOrientation(QtCore.Qt.Horizontal)
        self.widgets.ie["slider"].setObjectName("ie_slider")
        self.grid_layout.addWidget(self.widgets.ie["slider"], 11, 3, 1, 1)

    def _set_fio2_widget(self, spacer_item: Dict) -> None:
        """ FiO2 Label, LCD, and Slider """
        self.widgets.fio2["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.fio2["label"].setObjectName("fio2_label")
        self.grid_layout.addWidget(self.widgets.fio2["label"], 13, 0, 1, 1)
        self.grid_layout.addItem(spacer_item["15"], 2, 2, 1, 1)

        self.widgets.fio2["lcd"] = QtWidgets.QLCDNumber(self.central_widget)
        self.widgets.fio2["lcd"].setObjectName("fio2_lcd")
        self.grid_layout.addWidget(self.widgets.fio2["lcd"], 13, 2, 1, 1)

        self.widgets.fio2["slider"] = QtWidgets.QSlider(self.central_widget)
        self.widgets.fio2["slider"].setOrientation(QtCore.Qt.Horizontal)
        self.widgets.fio2["slider"].setObjectName("fio2_slider")
        self.grid_layout.addWidget(self.widgets.fio2["slider"], 13, 3, 1, 1)
        self.grid_layout.addItem(spacer_item["2"], 1, 1, 1, 1)
        self.grid_layout.addItem(spacer_item["3"], 8, 2, 1, 1)
        self.grid_layout.addItem(spacer_item["4"], 15, 1, 1, 1)
        self.grid_layout.addItem(spacer_item["5"], 3, 1, 1, 1)
        self.grid_layout.addItem(spacer_item["6"], 13, 1, 1, 1)
        self.grid_layout.addItem(spacer_item["7"], 7, 1, 1, 1)

    def _set_respitory_rate_widget(self, spacer_item: Dict) -> None:
        # Respitory Rate Label, LCD, and Slider
        self.widgets.resp_rate["label"] = QtWidgets.QLabel(self.central_widget)
        self.widgets.resp_rate["label"].setObjectName("resp_rate_label")
        self.grid_layout.addWidget(self.widgets.resp_rate["label"], 15, 0, 1, 1)

        self.widgets.resp_rate["lcd"] = QtWidgets.QLCDNumber(self.central_widget)
        self.widgets.resp_rate["lcd"].setObjectName("resp_rate_lcd")
        self.grid_layout.addWidget(self.widgets.resp_rate["lcd"], 15, 2, 1, 1)

        self.widgets.resp_rate["slider"] = QtWidgets.QSlider(self.central_widget)
        self.widgets.resp_rate["slider"].setOrientation(QtCore.Qt.Horizontal)
        self.widgets.resp_rate["slider"].setObjectName("resp_rate_slider")
        self.grid_layout.addWidget(self.widgets.resp_rate["slider"], 15, 3, 1, 1)
        self.grid_layout.addItem(spacer_item["9"], 6, 2, 1, 1)

    def retranslate_ui(self, main_window) -> None:
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.widgets.plateau_press["label"].setText(
            _translate("MainWindow", "Plateau Pressure"))
        self.widgets.tv["label"].setText(_translate("MainWindow", "Tidal Volume"))
        self.widgets.ie["label"].setText(_translate("MainWindow", "I/E Ratio"))
        self.widgets.resp_rate["label"].setText(_translate("MainWindow", "Resp. Rate"))
        self.widgets.fio2["label"].setText(_translate("MainWindow", "FiO2"))
        self.widgets.mode["button"].setText(_translate("MainWindow", "SIMV"))
        self.widgets.mode["label"].setText(_translate("MainWindow", "Mode"))
        self.widgets.peak_press["label"].setText(
            _translate("MainWindow", "Peak. Inspiratory Pressure"))
        self.widgets.peep["label"].setText(_translate("MainWindow", "PEEP"))
