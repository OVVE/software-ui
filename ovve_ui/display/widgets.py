"""
Widgets used to initialze the the OVVE UI
"""
from random import randint
from typing import TypeVar

import numpy as np
import pyqtgraph as pg

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel
from PyQt5.QtCore import Qt

from display.ui_settings import SimpleButtonSettings, FancyButtonSettings, DisplayRectSettings, PageSettings

# Used for documentation purposes only
MainWindow = TypeVar('MainWindow')


def initializeHomeScreenWidget(
        window: MainWindow) -> (QVBoxLayout, QStackedWidget):
    """ Creates Home Screen for Widgets """
    layout = QVBoxLayout()
    h_box_11 = QHBoxLayout()
    h_box_12 = QHBoxLayout()
    h_box_11.setAlignment(Qt.AlignCenter)

    v_box_11left = QVBoxLayout()
    v_box_11mid = QVBoxLayout()
    v_box_11right = QVBoxLayout()

    window.mode_button_main = window.makeSimpleDisplayButton(
        window.get_mode_display(window.settings.mode), )
    window.mode_button_main.clicked.connect(lambda: window.display(1))

    window.resp_rate_button_main = window.makeFancyDisplayButton(
        "Set Resp. Rate",
        window.settings.resp_rate,
        "bpm",
    )

    window.resp_rate_button_main.clicked.connect(lambda: window.display(2))

    window.tv_button_main = window.makeFancyDisplayButton(
        "Set Tidal Volume",
        window.settings.tv,
        "mL",
    )
    window.tv_button_main.clicked.connect(lambda: window.display(3))

    window.ie_button_main = window.makeFancyDisplayButton(
        "Set I/E Ratio",
        window.get_ie_ratio_display(window.settings.ie_ratio),
        "",
    )
    window.ie_button_main.clicked.connect(lambda: window.display(4))

    window.alarm_button_main = window.makeSimpleDisplayButton(
        "ALARM",
        button_settings=SimpleButtonSettings(borderColor="#FF0000",
                                             fillColor='#FFFFFF',
                                             valueColor='#FF0000'),
    )
    window.alarm_button_main.clicked.connect(lambda: window.display(5))

    window.start_button_main = window.makeSimpleDisplayButton("START", )
    window.start_button_main.clicked.connect(window.changeStartStop)

    window.resp_rate_display_main = window.makeDisplayRect(
        "Resp. Rate",
        window.params.resp_rate_meas,
        "bpm",
    )

    window.tv_insp_display_main = window.makeDisplayRect(
        "TV Insp",
        window.params.tv_insp,
        "mL",
    )
    window.tv_exp_display_main = window.makeDisplayRect(
        "TV Exp",
        window.params.tv_exp,
        "mL",
    )

    window.peep_display_main = window.makeDisplayRect(
        "PEEP",
        window.params.peep,
        "cmH2O",
    )

    window.ppeak_display_main = window.makeDisplayRect(
        "Ppeak",
        window.params.ppeak,
        "cmH2O",
    )
    window.pplat_display_main = window.makeDisplayRect(
        "Pplat",
        window.params.pplat,
        "cmH2O",
    )

    h_box_11.addWidget(window.mode_button_main)
    h_box_11.addWidget(window.resp_rate_button_main)
    h_box_11.addWidget(window.tv_button_main)
    h_box_11.addWidget(window.ie_button_main)
    h_box_11.addWidget(window.alarm_button_main)
    h_box_11.addWidget(window.start_button_main)

    v_box_11left.addWidget(window.resp_rate_display_main)
    v_box_11left.addWidget(window.tv_insp_display_main)
    v_box_11left.addWidget(window.tv_exp_display_main)

    stack = QStackedWidget()

    v_box_11mid.addWidget(stack)

    v_box_11right.addWidget(window.peep_display_main)
    v_box_11right.addWidget(window.ppeak_display_main)
    v_box_11right.addWidget(window.pplat_display_main)

    h_box_12.addLayout(v_box_11left)
    h_box_12.addLayout(v_box_11mid)
    h_box_12.addLayout(v_box_11right)

    h_box_11.setSpacing(18)

    layout.addLayout(h_box_11)
    layout.addLayout(h_box_12)
    return (layout, stack)


# TODO: current graph system doesn't associate y values with x values.
#TODO: Add Units
def initializeGraphWidget(window: MainWindow) -> None:
    v_box = QVBoxLayout()
    axisStyle = {'color': 'black', 'font-size': '20pt'}
    graph_pen = pg.mkPen(width=5, color="b")

    graph_width = 400

    window.flow_data = np.linspace(0, 0, graph_width)
    window.flow_graph_ptr = -graph_width
    window.flow_graph = pg.PlotWidget()
    window.flow_graph.setFixedWidth(graph_width)
    window.flow_graph_line = window.flow_graph.plot(window.flow_data,
                                                    pen=graph_pen)
    window.flow_graph.setBackground("w")
    window.flow_graph.setMouseEnabled(False, False)
    flow_graph_left_axis = window.flow_graph.getAxis("left")
    flow_graph_left_axis.setLabel("Flow", **axisStyle)

    window.pressure_data = np.linspace(0, 0, graph_width)
    window.pressure_graph_ptr = -graph_width
    window.pressure_graph = pg.PlotWidget()
    window.pressure_graph.setFixedWidth(graph_width)
    window.pressure_graph_line = window.pressure_graph.plot(
        window.pressure_data, pen=graph_pen)
    window.pressure_graph.setBackground("w")
    window.pressure_graph.setMouseEnabled(False, False)
    pressure_graph_left_axis = window.pressure_graph.getAxis("left")
    pressure_graph_left_axis.setLabel("Pressure", **axisStyle)

    window.volume_data = np.linspace(0, 0, graph_width)
    window.volume_graph_ptr = -graph_width
    window.volume_graph = pg.PlotWidget()
    window.volume_graph.setFixedWidth(graph_width)
    window.volume_graph_line = window.volume_graph.plot(window.volume_data,
                                                        pen=graph_pen)
    window.volume_graph.setBackground("w")
    window.volume_graph.setMouseEnabled(False, False)
    volume_graph_left_axis = window.volume_graph.getAxis("left")
    volume_graph_left_axis.setLabel("Volume", **axisStyle)

    v_box.addWidget(window.flow_graph)
    v_box.addWidget(window.pressure_graph)
    v_box.addWidget(window.volume_graph)

    window.page["1"].setLayout(v_box)


def initializeModeWidget(window: MainWindow) -> None:
    """ Creates Mode Widget """
    page_settings = window.ui_settings.page_settings
    v_box = QVBoxLayout()
    h_box_1 = QHBoxLayout()
    h_box_2 = QHBoxLayout()
    h_box_3 = QHBoxLayout()
    h_box_4 = QHBoxLayout()

    h_box_1.setAlignment(Qt.AlignCenter)
    h_box_2.setAlignment(Qt.AlignCenter)
    h_box_2.setSpacing(window.ui_settings.page_settings.changeButtonSpacing)
    h_box_3.setAlignment(Qt.AlignCenter)
    h_box_4.setAlignment(Qt.AlignCenter)
    h_box_4.setSpacing(
        window.ui_settings.page_settings.commitCancelButtonSpacing)

    mode_title_label = QLabel("Set Ventilation Mode")
    mode_title_label.setFont(page_settings.mainLabelFont)
    mode_title_label.setAlignment(Qt.AlignCenter)

    window.mode_page_value_label = QLabel(
        window.get_mode_display(window.local_settings.mode))
    window.mode_page_value_label.setFont(page_settings.textValueFont)
    window.mode_page_value_label.setAlignment(Qt.AlignCenter)
    window.mode_page_value_label.setStyleSheet("QLabel {color: " +
                                               page_settings.valueColor + ";}")
    window.mode_page_value_label.setFixedWidth(page_settings.valueLabelWidth)

    mode_unit_label = QLabel("")
    mode_unit_label.setFont(page_settings.unitFont)
    mode_unit_label.setAlignment(Qt.AlignCenter)

    mode_decrement_button = window.makeSimpleDisplayButton(
        "\u2190",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    mode_increment_button = window.makeSimpleDisplayButton(
        "\u2192",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    mode_apply = window.makeSimpleDisplayButton(
        "APPLY",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor=page_settings.commitColor))
    mode_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor=page_settings.cancelColor))
    mode_decrement_button.clicked.connect(window.decrementMode)
    mode_increment_button.clicked.connect(window.incrementMode)
    mode_apply.clicked.connect(window.commitMode)
    mode_cancel.clicked.connect(window.cancelChange)

    h_box_1.addWidget(mode_title_label)
    h_box_2.addWidget(mode_decrement_button)
    h_box_2.addWidget(window.mode_page_value_label)
    h_box_2.addWidget(mode_increment_button)
    h_box_3.addWidget(mode_unit_label)
    h_box_4.addWidget(mode_apply)
    h_box_4.addWidget(mode_cancel)

    v_box.addLayout(h_box_1)
    v_box.addLayout(h_box_2)
    v_box.addLayout(h_box_3)
    v_box.addLayout(h_box_4)

    window.page["2"].setLayout(v_box)


def initializeRespiratoryRateWidget(window) -> None:
    """ Creates Respiratory Rate Widget """
    page_settings = window.ui_settings.page_settings
    v_box = QVBoxLayout()
    h_box_1 = QHBoxLayout()
    h_box_2 = QHBoxLayout()
    h_box_3 = QHBoxLayout()
    h_box_4 = QHBoxLayout()
    h_box_1.setAlignment(Qt.AlignCenter)
    h_box_2.setAlignment(Qt.AlignCenter)
    h_box_2.setSpacing(window.ui_settings.page_settings.changeButtonSpacing)
    h_box_3.setAlignment(Qt.AlignCenter)
    h_box_4.setAlignment(Qt.AlignCenter)
    h_box_4.setSpacing(
        window.ui_settings.page_settings.commitCancelButtonSpacing)

    resp_rate_title_label = QLabel("Set Respiratory Rate")
    resp_rate_title_label.setFont(page_settings.mainLabelFont)
    resp_rate_title_label.setAlignment(Qt.AlignCenter)

    window.resp_rate_page_value_label = QLabel(
        str(window.local_settings.resp_rate))
    window.resp_rate_page_value_label.setFont(page_settings.valueFont)
    window.resp_rate_page_value_label.setAlignment(Qt.AlignCenter)
    window.resp_rate_page_value_label.setStyleSheet("QLabel {color: " +
                                                    page_settings.valueColor +
                                                    ";}")

    resp_rate_unit_label = QLabel("bpm")
    resp_rate_unit_label.setFont(page_settings.unitFont)
    resp_rate_unit_label.setStyleSheet("QLabel {color: " +
                                       page_settings.unitColor + ";}")
    resp_rate_unit_label.setAlignment(Qt.AlignCenter)

    resp_rate_decrement_button = window.makeSimpleDisplayButton(
        "-",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    resp_rate_increment_button = window.makeSimpleDisplayButton(
        "+",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    resp_rate_apply = window.makeSimpleDisplayButton(
        "APPLY",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor=page_settings.commitColor))
    resp_rate_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor=page_settings.cancelColor))

    resp_rate_decrement_button.clicked.connect(window.decrementRespRate)
    resp_rate_increment_button.clicked.connect(window.incrementRespRate)
    resp_rate_apply.clicked.connect(window.commitRespRate)
    resp_rate_cancel.clicked.connect(window.cancelChange)

    h_box_1.addWidget(resp_rate_title_label)
    h_box_2.addWidget(resp_rate_decrement_button)
    h_box_2.addWidget(window.resp_rate_page_value_label)
    window.resp_rate_page_value_label.setFixedWidth(
        page_settings.valueLabelWidth)
    h_box_2.addWidget(resp_rate_increment_button)
    h_box_3.addWidget(resp_rate_unit_label)
    h_box_4.addWidget(resp_rate_apply)
    h_box_4.addWidget(resp_rate_cancel)

    v_box.addLayout(h_box_1)
    v_box.addLayout(h_box_2)
    v_box.addLayout(h_box_3)
    v_box.addLayout(h_box_4)

    window.page["3"].setLayout(v_box)


def initializeTidalVolumeWidget(window: MainWindow):
    """ Creates Tidal Volume Widget """
    page_settings = window.ui_settings.page_settings
    v_box = QVBoxLayout()
    h_box_1 = QHBoxLayout()
    h_box_2 = QHBoxLayout()
    h_box_3 = QHBoxLayout()
    h_box_4 = QHBoxLayout()
    h_box_1.setAlignment(Qt.AlignCenter)
    h_box_2.setAlignment(Qt.AlignCenter)
    h_box_2.setSpacing(window.ui_settings.page_settings.changeButtonSpacing)
    h_box_3.setAlignment(Qt.AlignCenter)
    h_box_4.setAlignment(Qt.AlignCenter)
    h_box_4.setSpacing(
        window.ui_settings.page_settings.commitCancelButtonSpacing)

    tv_title_label = QLabel("Set Tidal Volume")
    tv_title_label.setFont(page_settings.mainLabelFont)
    tv_title_label.setAlignment(Qt.AlignCenter)

    window.tv_page_value_label = QLabel(str(window.local_settings.resp_rate))
    window.tv_page_value_label.setFont(page_settings.valueFont)
    window.tv_page_value_label.setStyleSheet("QLabel {color: " +
                                             page_settings.valueColor + ";}")
    window.tv_page_value_label.setAlignment(Qt.AlignCenter)
    window.tv_page_value_label.setFixedWidth(page_settings.valueLabelWidth)

    tv_unit_label = QLabel("mL")
    tv_unit_label.setFont(page_settings.unitFont)
    tv_unit_label.setStyleSheet("QLabel {color: " + page_settings.unitColor +
                                ";}")
    tv_unit_label.setAlignment(Qt.AlignCenter)

    tv_decrement_button = window.makeSimpleDisplayButton(
        "-",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    tv_increment_button = window.makeSimpleDisplayButton(
        "+",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    tv_apply = window.makeSimpleDisplayButton(
        "APPLY",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor=page_settings.commitColor))
    tv_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor=page_settings.cancelColor))

    tv_decrement_button.clicked.connect(window.decrementTidalVol)
    tv_increment_button.clicked.connect(window.incrementTidalVol)
    tv_apply.clicked.connect(window.commitTidalVol)
    tv_cancel.clicked.connect(window.cancelChange)

    h_box_1.addWidget(tv_title_label)
    h_box_2.addWidget(tv_decrement_button)
    h_box_2.addWidget(window.tv_page_value_label)
    h_box_2.addWidget(tv_increment_button)

    h_box_3.addWidget(tv_unit_label)
    h_box_4.addWidget(tv_apply)
    h_box_4.addWidget(tv_cancel)

    v_box.addLayout(h_box_1)
    v_box.addLayout(h_box_2)
    v_box.addLayout(h_box_3)
    v_box.addLayout(h_box_4)

    window.page["4"].setLayout(v_box)


def initializeIERatioWidget(window: MainWindow):
    """ Creates i/e Ratio Widget """
    page_settings = window.ui_settings.page_settings
    v_box = QVBoxLayout()
    h_box_1 = QHBoxLayout()
    h_box_2 = QHBoxLayout()
    h_box_3 = QHBoxLayout()
    h_box_4 = QHBoxLayout()

    h_box_1.setAlignment(Qt.AlignCenter)
    h_box_2.setAlignment(Qt.AlignCenter)
    h_box_2.setSpacing(window.ui_settings.page_settings.changeButtonSpacing)
    h_box_3.setAlignment(Qt.AlignCenter)
    h_box_4.setAlignment(Qt.AlignCenter)
    h_box_4.setSpacing(
        window.ui_settings.page_settings.commitCancelButtonSpacing)

    ie_ratio_title_label = QLabel("Set I/E Ratio")
    ie_ratio_title_label.setFont(page_settings.mainLabelFont)
    ie_ratio_title_label.setAlignment(Qt.AlignCenter)

    window.ie_ratio_page_value_label = QLabel(
        window.get_ie_ratio_display(window.local_settings.ie_ratio))
    window.ie_ratio_page_value_label.setFont(page_settings.textValueFont)
    window.ie_ratio_page_value_label.setAlignment(Qt.AlignCenter)
    window.ie_ratio_page_value_label.setStyleSheet("QLabel {color: " +
                                                   page_settings.valueColor +
                                                   ";}")
    window.ie_ratio_page_value_label.setFixedWidth(
        page_settings.valueLabelWidth)

    ie_unit_label = QLabel("")
    ie_unit_label.setFont(page_settings.unitFont)
    ie_unit_label.setAlignment(Qt.AlignCenter)

    ie_ratio_decrement_button = window.makeSimpleDisplayButton(
        "\u2190",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    ie_ratio_increment_button = window.makeSimpleDisplayButton(
        "\u2192",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    ie_ratio_apply = window.makeSimpleDisplayButton(
        "APPLY",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor=page_settings.commitColor))
    ie_ratio_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor=page_settings.cancelColor))
    ie_ratio_decrement_button.clicked.connect(window.decrementIERatio)
    ie_ratio_increment_button.clicked.connect(window.incrementIERatio)
    ie_ratio_apply.clicked.connect(window.commitIERatio)
    ie_ratio_cancel.clicked.connect(window.cancelChange)

    h_box_1.addWidget(ie_ratio_title_label)
    h_box_2.addWidget(ie_ratio_decrement_button)
    h_box_2.addWidget(window.ie_ratio_page_value_label)
    h_box_2.addWidget(ie_ratio_increment_button)
    h_box_3.addWidget(ie_unit_label)
    h_box_4.addWidget(ie_ratio_apply)
    h_box_4.addWidget(ie_ratio_cancel)

    v_box.addLayout(h_box_1)
    v_box.addLayout(h_box_2)
    v_box.addLayout(h_box_3)
    v_box.addLayout(h_box_4)

    window.page["5"].setLayout(v_box)


def initializeAlarmWidget(window: MainWindow):  #Alarm
    v_box_6 = QVBoxLayout()
    h_box_6top = QHBoxLayout()
    #h_box_6middle = QHBoxLayout()
    h_box_6bottom = QHBoxLayout()

    alarm_ack = window.makeSimpleDisplayButton("Acknowledge")
    alarm_cancel = window.makeSimpleDisplayButton("Cancel")

    # Acknowledge alarm stops the alarms
    alarm_ack.clicked.connect(lambda: window.commitAlarm())
    alarm_cancel.clicked.connect(window.cancelChange)

    window.alarm_page_rect = window.makeDisplayRect(
        "Alarm", window.settings.get_alarm_display(), "", size=(400, 200))

    h_box_6top.addWidget(window.alarm_page_rect)
    #h_box_6middle.addWidget(alarm_toggle)
    h_box_6bottom.addWidget(alarm_ack)
    h_box_6bottom.addWidget(alarm_cancel)

    v_box_6.addLayout(h_box_6top)
    #v_box_6.addLayout(h_box_6middle)
    v_box_6.addLayout(h_box_6bottom)

    window.page["6"].setLayout(v_box_6)
