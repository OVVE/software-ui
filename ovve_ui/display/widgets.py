"""
Widgets used to initialize the the OVVE UI
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
        window.get_ie_ratio_display(window.settings.ie_ratio_enum),
        "",
    )
    window.ie_button_main.clicked.connect(lambda: window.display(4))

    window.start_stop_button_main = window.makeSimpleDisplayButton("START")
    window.start_stop_button_main.clicked.connect(window.changeStartStop)

    window.settings_button_main = window.makeSimpleDisplayButton("SETTINGS")
    window.settings_button_main.clicked.connect(lambda: window.display(6))


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
    # window.tv_exp_display_main = window.makeDisplayRect(
    #     "TV Exp",
    #     window.params.tv_exp,
    #     "mL",
    # )

    window.tv_exp_display_main = window.makeDisplayRect(
        "TV Exp",
        "---",
        "mL",
        rect_settings=DisplayRectSettings(fillColor="#C5C5C5",
                                          labelColor = "#A9A9A9",
                                          unitColor = "#A9A9A9"
                                          ),
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
    h_box_11.addWidget(window.start_stop_button_main)
    h_box_11.addWidget(window.settings_button_main)

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


#TODO: Add Units
def initializeGraphWidget(window: MainWindow) -> None:
    v_box = QVBoxLayout()
    axisStyle = {'color': 'black', 'font-size': '20pt'}
    window.new_graph_pen = pg.mkPen(width=2, color="b")
    window.cache_graph_pen = pg.mkPen(width=2, color="k")
    # TODO: Adjust graph width for resp rate
    window.graph_width = 60
    window.graph_ptr = 0
    label_style = {'color': 'k', 'font-size': '14pt'}


    window.flow_data = np.empty([window.graph_width,])
    window.flow_graph = pg.PlotWidget()
    # TODO: Find good values for the ranges of flow, just use MIN and MAX from sensor for now
    window.flow_graph.setXRange(0, window.graph_width, padding=0)
    window.flow_graph.setYRange(-30, 30, padding=0) #Flow should be presented in L/min.

    window.flow_graph_line = window.flow_graph.plot(window.flow_data,
                                                    pen=window.new_graph_pen)
    window.flow_graph_cache_line = window.flow_graph.plot(
        window.flow_data, pen=window.cache_graph_pen)
    window.flow_graph_cache_line.hide()

    window.flow_graph.setBackground("w")
    window.flow_graph.setMouseEnabled(False, False)
    window.flow_graph_left_axis = window.flow_graph.getAxis("left")
    window.flow_graph_left_axis.setLabel("Flow (L/min.)", **label_style)
    window.flow_graph.getPlotItem().hideAxis('bottom')

    window.pressure_data = np.empty([window.graph_width,])
    window.pressure_graph = pg.PlotWidget()
    # TODO: Find good values for ranges of pressure, 40 cmH2O is the max before overpressure value pops
    window.pressure_graph.setXRange(0, window.graph_width, padding=0)
    window.pressure_graph.setYRange(-45, 45, padding=0)

    window.pressure_graph_line = window.pressure_graph.plot(
        window.pressure_data, pen=window.new_graph_pen)
    window.pressure_graph_cache_line = window.pressure_graph.plot(
        window.pressure_data, pen=window.cache_graph_pen)
    window.pressure_graph_cache_line.hide()

    window.pressure_graph.setBackground("w")
    window.pressure_graph.setMouseEnabled(False, False)
    window.pressure_graph_left_axis = window.pressure_graph.getAxis("left")
    window.pressure_graph_left_axis.setLabel("Press. (cmH2O)", **label_style)
    window.pressure_graph.getPlotItem().hideAxis('bottom')

    window.volume_data = np.empty([window.graph_width,])
    window.volume_graph = pg.PlotWidget()
    # TODO: Find good values for ranges of volume, just picked a pretty big number for now
    window.volume_graph.setXRange(0, window.graph_width, padding=0)
    window.volume_graph.setYRange(-200, 1200, padding=0)
    window.volume_graph_line = window.volume_graph.plot(
        window.volume_data, pen=window.new_graph_pen)
    window.volume_graph_cache_line = window.volume_graph.plot(
        window.volume_data, pen=window.cache_graph_pen)
    window.volume_graph_cache_line.hide()

    window.volume_graph.setBackground("w")
    window.volume_graph.setMouseEnabled(False, False)
    window.volume_graph_left_axis = window.volume_graph.getAxis("left")
    window.volume_graph_left_axis.setLabel("Volume (mL)", **label_style)
    window.volume_graph.getPlotItem().hideAxis('bottom')

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
    mode_title_label.setStyleSheet("QLabel {color: #000000 ;}")

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
    resp_rate_title_label.setStyleSheet("QLabel {color: #000000 ;}")

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

    window.resp_rate_decrement_button = window.makeSimpleDisplayButton(
        "-",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    resp_rate_decrement_size_policy = window.resp_rate_decrement_button.sizePolicy(
    )
    resp_rate_decrement_size_policy.setRetainSizeWhenHidden(True)
    window.resp_rate_decrement_button.setSizePolicy(
        resp_rate_decrement_size_policy)

    if window.local_settings.resp_rate - window.ranges._ranges["resp_rate_increment"] \
            < window.ranges._ranges["min_resp_rate"]:
        window.resp_rate_decrement_button.hide()

    window.resp_rate_increment_button = window.makeSimpleDisplayButton(
        "+",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    resp_rate_increment_size_policy = window.resp_rate_increment_button.sizePolicy(
    )
    resp_rate_increment_size_policy.setRetainSizeWhenHidden(True)
    window.resp_rate_increment_button.setSizePolicy(
        resp_rate_increment_size_policy)

    if window.local_settings.resp_rate + window.ranges._ranges["resp_rate_increment"] \
            > window.ranges._ranges["max_resp_rate"]:
        window.resp_rate_increment_button.hide()

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

    window.resp_rate_decrement_button.clicked.connect(window.decrementRespRate)
    window.resp_rate_increment_button.clicked.connect(window.incrementRespRate)

    resp_rate_apply.clicked.connect(window.commitRespRate)
    resp_rate_cancel.clicked.connect(window.cancelChange)

    h_box_1.addWidget(resp_rate_title_label)
    h_box_2.addWidget(window.resp_rate_decrement_button)
    h_box_2.addWidget(window.resp_rate_page_value_label)
    window.resp_rate_page_value_label.setFixedWidth(
        page_settings.valueLabelWidth)
    h_box_2.addWidget(window.resp_rate_increment_button)
    h_box_3.addWidget(resp_rate_unit_label)
    h_box_4.addWidget(resp_rate_apply)
    h_box_4.addWidget(resp_rate_cancel)

    v_box.addLayout(h_box_1)
    v_box.addLayout(h_box_2)
    v_box.addLayout(h_box_3)
    v_box.addLayout(h_box_4)

    window.page["3"].setLayout(v_box)


def initializeTidalVolumeWidget(window: MainWindow) -> None:
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
    tv_title_label.setStyleSheet("QLabel {color: #000000 ;}")

    window.tv_page_value_label = QLabel(str(window.local_settings.tv))
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

    window.tv_decrement_button = window.makeSimpleDisplayButton(
        "-",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    tv_decrement_size_policy = window.tv_decrement_button.sizePolicy()
    tv_decrement_size_policy.setRetainSizeWhenHidden(True)
    window.tv_decrement_button.setSizePolicy(tv_decrement_size_policy)

    if window.local_settings.tv - window.ranges._ranges["tv_increment"] \
            < window.ranges._ranges["min_tv"]:
        window.tv_decrement_button.hide()

    window.tv_increment_button = window.makeSimpleDisplayButton(
        "+",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))

    tv_increment_size_policy = window.tv_increment_button.sizePolicy()
    tv_increment_size_policy.setRetainSizeWhenHidden(True)
    window.tv_increment_button.setSizePolicy(tv_increment_size_policy)

    if window.local_settings.tv + window.ranges._ranges["tv_increment"] \
            > window.ranges._ranges["max_tv"]:
        window.tv_increment_button.hide()

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

    window.tv_decrement_button.clicked.connect(window.decrementTidalVol)
    window.tv_increment_button.clicked.connect(window.incrementTidalVol)
    tv_apply.clicked.connect(window.commitTidalVol)
    tv_cancel.clicked.connect(window.cancelChange)

    h_box_1.addWidget(tv_title_label)
    h_box_2.addWidget(window.tv_decrement_button)
    h_box_2.addWidget(window.tv_page_value_label)
    h_box_2.addWidget(window.tv_increment_button)

    h_box_3.addWidget(tv_unit_label)
    h_box_4.addWidget(tv_apply)
    h_box_4.addWidget(tv_cancel)

    v_box.addLayout(h_box_1)
    v_box.addLayout(h_box_2)
    v_box.addLayout(h_box_3)
    v_box.addLayout(h_box_4)

    window.page["4"].setLayout(v_box)


def initializeIERatioWidget(window: MainWindow) -> None:
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
    ie_ratio_title_label.setStyleSheet("QLabel {color: #000000 ;}")

    window.ie_ratio_page_value_label = QLabel(
        window.get_ie_ratio_display(window.local_settings.ie_ratio_enum))
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


def initializeAlarmWidget(window: MainWindow) -> None:  #Alarm
    v_box_6 = QVBoxLayout()
    h_box_6top = QHBoxLayout()
    h_box_6mid = QHBoxLayout()
    h_box_6bottom = QHBoxLayout()

    h_box_6top.setAlignment(Qt.AlignCenter)
    h_box_6mid.setAlignment(Qt.AlignCenter)
    h_box_6bottom.setAlignment(Qt.AlignCenter)

    alarm_page_label = QLabel("Alarm")
    alarm_page_label.setFont(window.ui_settings.page_settings.mainLabelFont)
    alarm_page_label.setAlignment(Qt.AlignCenter)

    window.alarm_display_label = QLabel()
    window.alarm_display_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    window.alarm_display_label.setAlignment(Qt.AlignCenter)
    window.alarm_display_label.setWordWrap(True)

    alarm_silence_button = window.makeSimpleDisplayButton(
        f"Silence for {window.settings.silence_time} min.",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(130, 65))
    alarm_silence_button.clicked.connect(lambda: window.silenceAlarm())

    h_box_6top.addWidget(alarm_page_label)
    h_box_6mid.addWidget(window.alarm_display_label)
    h_box_6bottom.addWidget(alarm_silence_button)

    h_box_6bottom.setSpacing(10)

    v_box_6.addLayout(h_box_6top)
    v_box_6.addLayout(h_box_6mid)
    v_box_6.addLayout(h_box_6bottom)

    window.page["6"].setLayout(v_box_6)


def initializeSettingsWidget(window: MainWindow) -> None:
    v_box_7 = QVBoxLayout()
    h_box_7top = QHBoxLayout()
    h_box_7bottom = QHBoxLayout()

    h_box_7top.setAlignment(Qt.AlignCenter)
    h_box_7bottom.setAlignment(Qt.AlignCenter)

    settings_page_label = QLabel("Settings")
    settings_page_label.setFont(window.ui_settings.page_settings.mainLabelFont)

    settings_page_label.setAlignment(Qt.AlignCenter)

    settings_back_button = window.makeSimpleDisplayButton(
        "Back",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(200, 65))
    settings_back_button.clicked.connect(lambda: window.display(0))

    h_box_7top.addWidget(settings_page_label)
    h_box_7bottom.addWidget(settings_back_button)
    v_box_7.addLayout(h_box_7top)
    v_box_7.addLayout(h_box_7bottom)

    window.page["7"].setLayout(v_box_7)
