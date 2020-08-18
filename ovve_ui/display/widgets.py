"""
Widgets used to initialize the the OVVE UI
"""
from random import randint
from typing import TypeVar
from os import path
import numpy as np
import pyqtgraph as pg

from PyQt5.QtWidgets import (QWidget, QTabWidget, QHBoxLayout, QVBoxLayout,
                             QStackedWidget, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5 import QtGui

from display.ui_settings import (SimpleButtonSettings, FancyButtonSettings,
                                 DisplayRectSettings, PageSettings,
                                 TextSetting)
from display.selectors import AlarmLimitSelector, AlarmLimitSelectorPair

from utils.alarm_limits import AlarmLimits
from utils.alarm_limit_type import AlarmLimitType, AlarmLimitPair

# Used for documentation purposes only
MainWindow = TypeVar('MainWindow')


def initializeHomeScreenWidget(
        window: MainWindow) -> None:
    """ Creates Home Screen for Widgets """
    layout = QVBoxLayout()
    h_box_1 = QHBoxLayout()
    h_box_2 = QHBoxLayout()
    h_box_3 = QHBoxLayout()

    h_box_1left = QHBoxLayout()
    h_box_1right = QHBoxLayout()

    h_box_1right.setAlignment(Qt.AlignRight)

    h_box_2.setAlignment(Qt.AlignCenter)

    v_box_3left = QVBoxLayout()
    v_box_3mid = QVBoxLayout()
    v_box_3right = QVBoxLayout()

    main_logo_path = path.abspath(
        path.join(path.dirname(__file__), "images/lm_logo_dark.png"))
    main_logo = window.makePicButton(
        main_logo_path,
        size=(185, 30),
        custom_path = True
    )
    main_logo.clicked.connect(lambda: window.display(0))

    window.main_patient_label = QLabel(
        f"Current Patient: Patient {window.patient_id_display}")
    window.main_patient_label.setFont(
        window.ui_settings.page_settings.topBarFont)
    window.main_patient_label.setStyleSheet("QLabel {color: #fc992e ;}")

    window.main_datetime_label = QLabel(window.datetime.toString()[:-8])
    window.main_datetime_label.setFont(
        window.ui_settings.page_settings.topBarFont)
    window.main_datetime_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    window.main_battery_level_label = QLabel(f"{window.params.battery_level}%")
    window.main_battery_level_label.setFont(
        window.ui_settings.page_settings.topBarFont)
    window.main_battery_level_label.setFixedWidth(50)
    window.main_battery_level_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    main_battery_icon_path = path.abspath(
        path.join(path.dirname(__file__),
                  f"images/batteries/{window.battery_img}"))
    window.main_battery_icon = window.makePicButton(
        main_battery_icon_path,
        size=(30, 15),
        custom_path = True
    )

    h_box_1.setContentsMargins(0,0,0,0)

    window.mode_button_main = window.makeSimpleDisplayButton(
        window.get_mode_display(window.settings.mode), size = (126,64))
    # window.mode_button_main.clicked.connect(lambda: window.display(1))

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

    window.start_stop_button_main = window.makeSimpleDisplayButton("START",
                                                                   size=(126,
                                                                         64),
                                                                   button_settings = SimpleButtonSettings(fillColor = "#412828", borderColor = "#fd0101", valueColor = "#fd0101"))
    window.start_stop_button_main.clicked.connect(window.changeStartStop)

    settings_icon_path = path.abspath(
        path.join(path.dirname(__file__), "images/gear.png"))
    window.settings_button_main = window.makePicButton(settings_icon_path,
                                                       size=(50, 50),
                                                       custom_path = True)
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
        rect_settings=DisplayRectSettings(fillColor="#2c2c2c",
                                          labelColor="#4c4e4f",
                                          unitColor="#4c4e4f",
                                          borderColor = "#4c4e4f",
                                          valueColor = "#4c4e4f"),
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

    h_box_1left.addWidget(main_logo)

    h_box_1right1 = QHBoxLayout()
    h_box_1right2 = QHBoxLayout()

    h_box_1right1.addWidget(window.main_patient_label)
    h_box_1right1.addWidget(window.main_datetime_label)

    h_box_1right2.addWidget(window.main_battery_level_label)
    h_box_1right2.addWidget(window.main_battery_icon)

    h_box_1right.setSpacing(25)

    h_box_1right1.setSpacing(15)
    h_box_1right2.setSpacing(0)
    h_box_1right.addLayout(h_box_1right1)
    h_box_1right.addLayout(h_box_1right2)

    for button in [
            window.mode_button_main,
            window.resp_rate_button_main,
            window.tv_button_main,
            window.ie_button_main,
            window.start_stop_button_main,
            window.settings_button_main,
    ]:
        h_box_2.addWidget(button)
    h_box_2.setSpacing(18)

    for left_display in [
            window.resp_rate_display_main,
            window.tv_insp_display_main,
            window.tv_exp_display_main,
    ]:
        v_box_3left.addWidget(left_display)

    stack = QStackedWidget()
    v_box_3mid.addWidget(stack)

    for right_display in [
            window.peep_display_main,
            window.ppeak_display_main,
            window.pplat_display_main,
    ]:
        v_box_3right.addWidget(right_display)

    for h_layout1 in [
            h_box_1left,
            h_box_1right,
    ]:
        h_box_1.addLayout(h_layout1)

    for v_layout3 in [
            v_box_3left,
            v_box_3mid,
            v_box_3right,
    ]:
        h_box_3.addLayout(v_layout3)

    h_box_3.setSpacing(18)

    for h_layout in [h_box_1, h_box_2, h_box_3]:
        layout.addLayout(h_layout)

    wrapper = QWidget()
    wrapper.setLayout(layout)

    window.home_screen_widget = wrapper

    window.stack = stack


def initializeGraphWidget(window: MainWindow) -> None:
    v_box = QVBoxLayout()
    axisStyle = {'color': 'black', 'font-size': '20pt'}
    window.new_graph_pen = pg.mkPen(width=2, color="#e9840e")
    window.cache_graph_pen = pg.mkPen(width=2, color="#6a6a6a")

    # TODO: Adjust graph width for resp rate
    window.graph_width = 60
    window.graph_ptr = 0
    label_style = {'color': '#20c7ff', 'font-size': '9pt'}

    window.pressure_data = np.empty([
        window.graph_width,
    ])
    window.pressure_graph = pg.PlotWidget()
    window.pressure_graph.setYRange(-45, 70, padding=0)

    window.pressure_graph_line = window.pressure_graph.plot(
        window.pressure_data, pen=window.new_graph_pen)
    window.pressure_graph_cache_line = window.pressure_graph.plot(
        window.pressure_data, pen=window.cache_graph_pen)
    window.pressure_graph_cache_line.hide()
    window.pressure_graph_line.hide()

    window.pressure_graph_left_axis = window.pressure_graph.getAxis("left")
    window.pressure_graph_left_axis.setLabel("Press. (cmH2O)", **label_style)

    window.flow_data = np.empty([
        window.graph_width,
    ])
    window.flow_graph = pg.PlotWidget()
    window.flow_graph.setYRange(-10, 90,
                                padding=0)  #Flow should be presented in L/min.
    window.flow_graph_line = window.flow_graph.plot(window.flow_data,
                                                    pen=window.new_graph_pen)
    window.flow_graph_cache_line = window.flow_graph.plot(
        window.flow_data, pen=window.cache_graph_pen)
    window.flow_graph_cache_line.hide()
    window.flow_graph_line.hide()

    window.flow_graph_left_axis = window.flow_graph.getAxis("left")
    window.flow_graph_left_axis.setLabel("Flow (L/min.)", **label_style)

    window.volume_data = np.empty([
        window.graph_width,
    ])
    window.volume_graph = pg.PlotWidget()
    window.volume_graph.setYRange(-100, 900, padding=0)
    window.volume_graph_line = window.volume_graph.plot(
        window.volume_data, pen=window.new_graph_pen)
    window.volume_graph_cache_line = window.volume_graph.plot(
        window.volume_data, pen=window.cache_graph_pen)
    window.volume_graph_cache_line.hide()
    window.volume_graph_line.hide()

    window.volume_graph_left_axis = window.volume_graph.getAxis("left")
    window.volume_graph_left_axis.setLabel("Volume (mL)", **label_style)

    for graph in [
            window.pressure_graph, window.flow_graph, window.volume_graph
    ]:
        graph.setStyleSheet("border: 0;")
        graph.setXRange(0, window.graph_width, padding=0)
        graph.setBackground("#232323")
        graph.setMouseEnabled(False, False)
        graph.getPlotItem().hideAxis('bottom')
        v_box.addWidget(graph)

    window.page["1"].setStyleSheet("background-color: #232323; border: 1 solid #20c7ff")
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
    mode_title_label.setStyleSheet("QLabel {color: #74fff4 ;}")

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

    mode_decrement_button = window.makePicButton("left")
    mode_increment_button = window.makePicButton("right")


    mode_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor=page_settings.cancelColor,
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor="#FFFFFF"))

    mode_apply = window.makeSimpleDisplayButton(
        "APPLY",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor=page_settings.commitColor,
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor="#FFFFFF"))

    mode_decrement_button.clicked.connect(window.decrementMode)
    mode_increment_button.clicked.connect(window.incrementMode)
    mode_cancel.clicked.connect(window.cancelChange)
    mode_apply.clicked.connect(window.commitMode)

    h_box_1.addWidget(mode_title_label)
    h_box_2.addWidget(mode_decrement_button)
    h_box_2.addWidget(window.mode_page_value_label)
    h_box_2.addWidget(mode_increment_button)
    h_box_3.addWidget(mode_unit_label)
    h_box_4.addWidget(mode_cancel)
    h_box_4.addWidget(mode_apply)

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
    resp_rate_title_label.setStyleSheet("QLabel {color: #74fff4 ;}")

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

    window.resp_rate_decrement_button = window.makePicButton("left")

    resp_rate_decrement_size_policy = window.resp_rate_decrement_button.sizePolicy()
    resp_rate_decrement_size_policy.setRetainSizeWhenHidden(True)
    window.resp_rate_decrement_button.setSizePolicy(resp_rate_decrement_size_policy)

    window.resp_rate_increment_button = window.makePicButton("right")

    resp_rate_increment_size_policy = window.resp_rate_increment_button.sizePolicy(
    )
    resp_rate_increment_size_policy.setRetainSizeWhenHidden(True)
    window.resp_rate_increment_button.setSizePolicy(
        resp_rate_increment_size_policy)


    if window.local_settings.resp_rate - window.ranges._ranges["resp_rate_increment"] \
            < window.ranges._ranges["min_resp_rate"]:
        window.resp_rate_decrement_button.hide()

    if window.local_settings.resp_rate + window.ranges._ranges["resp_rate_increment"] \
            > window.ranges._ranges["max_resp_rate"]:
        window.resp_rate_increment_button.hide()

    resp_rate_cancel = window.makePicButton("cancel")

    resp_rate_apply = window.makePicButton("apply")

    window.resp_rate_decrement_button.clicked.connect(window.decrementRespRate)
    window.resp_rate_increment_button.clicked.connect(window.incrementRespRate)

    resp_rate_cancel.clicked.connect(window.cancelChange)
    resp_rate_apply.clicked.connect(window.commitRespRate)

    h_box_1.addWidget(resp_rate_title_label)
    h_box_2.addWidget(window.resp_rate_decrement_button)
    h_box_2.addWidget(window.resp_rate_page_value_label)
    window.resp_rate_page_value_label.setFixedWidth(
        page_settings.valueLabelWidth)
    h_box_2.addWidget(window.resp_rate_increment_button)
    h_box_3.addWidget(resp_rate_unit_label)
    h_box_4.addWidget(resp_rate_cancel)
    h_box_4.addWidget(resp_rate_apply)

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
    tv_title_label.setStyleSheet("QLabel {color: #74fff4 ;}")

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

    window.tv_decrement_button = window.makePicButton("left")

    tv_decrement_size_policy = window.tv_decrement_button.sizePolicy()
    tv_decrement_size_policy.setRetainSizeWhenHidden(True)
    window.tv_decrement_button.setSizePolicy(tv_decrement_size_policy)

    if window.local_settings.tv - window.ranges._ranges["tv_increment"] \
            < window.ranges._ranges["min_tv"]:
        window.tv_decrement_button.hide()

    window.tv_increment_button = window.makePicButton("right")

    tv_increment_size_policy = window.tv_increment_button.sizePolicy()
    tv_increment_size_policy.setRetainSizeWhenHidden(True)
    window.tv_increment_button.setSizePolicy(tv_increment_size_policy)

    if window.local_settings.tv + window.ranges._ranges["tv_increment"] \
            > window.ranges._ranges["max_tv"]:
        window.tv_increment_button.hide()

    tv_cancel = window.makePicButton("cancel")
    tv_apply = window.makePicButton("apply")

    window.tv_decrement_button.clicked.connect(window.decrementTidalVol)
    window.tv_increment_button.clicked.connect(window.incrementTidalVol)
    tv_apply.clicked.connect(window.commitTidalVol)
    tv_cancel.clicked.connect(window.cancelChange)

    h_box_1.addWidget(tv_title_label)
    h_box_2.addWidget(window.tv_decrement_button)
    h_box_2.addWidget(window.tv_page_value_label)
    h_box_2.addWidget(window.tv_increment_button)

    h_box_3.addWidget(tv_unit_label)
    h_box_4.addWidget(tv_cancel)
    h_box_4.addWidget(tv_apply)

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
    ie_ratio_title_label.setStyleSheet("QLabel {color: #74fff4 ;}")

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

    ie_ratio_decrement_button = window.makePicButton("left")

    ie_ratio_increment_button = window.makePicButton("right")


    ie_ratio_cancel = window.makePicButton("cancel")
    ie_ratio_apply = window.makePicButton("apply")

    ie_ratio_decrement_button.clicked.connect(window.decrementIERatio)
    ie_ratio_increment_button.clicked.connect(window.incrementIERatio)
    ie_ratio_cancel.clicked.connect(window.cancelChange)
    ie_ratio_apply.clicked.connect(window.commitIERatio)

    h_box_1.addWidget(ie_ratio_title_label)
    h_box_2.addWidget(ie_ratio_decrement_button)
    h_box_2.addWidget(window.ie_ratio_page_value_label)
    h_box_2.addWidget(ie_ratio_increment_button)
    h_box_3.addWidget(ie_unit_label)
    h_box_4.addWidget(ie_ratio_cancel)
    h_box_4.addWidget(ie_ratio_apply)

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
    window.alarm_display_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
    window.alarm_display_label.setFixedWidth(400)

    alarm_silence_button = window.makeSimpleDisplayButton(
        f"Silence for {window.settings.silence_time} min.",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(200, 65))
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
    h_box_7mid1 = QHBoxLayout()
    h_box_7mid1_v1 = QVBoxLayout()
    h_box_7mid1_v2 = QVBoxLayout()
    h_box_7mid2 = QHBoxLayout()
    h_box_7bottom = QHBoxLayout()

    h_box_7top.setAlignment(Qt.AlignCenter)
    h_box_7mid1.setAlignment(Qt.AlignCenter)
    h_box_7bottom.setAlignment(Qt.AlignCenter)

    settings_page_label = QLabel("Settings")
    settings_page_label.setFont(window.ui_settings.page_settings.mainLabelFont)
    settings_page_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    settings_page_label.setAlignment(Qt.AlignCenter)

    window.settings_patient_label = QLabel(
        f"Current Patient: Patient {window.patient_id_display}")
    window.settings_patient_label.setAlignment(Qt.AlignCenter)
    window.settings_patient_label.setFont(TextSetting("Arial", 20, True).font)
    window.settings_patient_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
    window.settings_patient_label.setWordWrap(True)

    settings_change_patient_button = window.makeSimpleDisplayButton(
        "Change Patient",
        size=(200, 60))
    settings_change_patient_button.clicked.connect(lambda: window.display(8))

    settings_change_datetime_button = window.makeSimpleDisplayButton(
        "Change Date/Time",
        size=(200, 60))
    settings_change_datetime_button.clicked.connect(lambda: window.display(9))

    settings_change_alarm_limits_button = window.makeSimpleDisplayButton(
        "Change Alarm Limits",
        size=(200, 60))
    settings_change_alarm_limits_button.clicked.connect(
        lambda: window.display(10))

    settings_back_button = window.makeSimpleDisplayButton(
        "Back to Main",
        size=(200, 60))
    settings_back_button.clicked.connect(lambda: window.display(0))

    h_box_7top.addWidget(settings_page_label)
    h_box_7mid1_v1.addWidget(window.settings_patient_label)
    h_box_7mid1_v2.addWidget(settings_change_patient_button)
    h_box_7mid1_v2.addWidget(settings_change_datetime_button)
    h_box_7mid1_v2.addWidget(settings_change_alarm_limits_button)
    h_box_7bottom.addWidget(settings_back_button)
    h_box_7mid1.addLayout(h_box_7mid1_v1)
    h_box_7mid1.addLayout(h_box_7mid1_v2)

    for h_box in [h_box_7top, h_box_7mid1, h_box_7mid2, h_box_7bottom]:
        v_box_7.addLayout(h_box)

    window.page["7"].setLayout(v_box_7)


def initializeConfirmStopWidget(window: MainWindow) -> None:
    v_box_8 = QVBoxLayout()
    h_box_8top = QHBoxLayout()
    h_box_8bottom = QHBoxLayout()

    h_box_8top.setAlignment(Qt.AlignCenter)
    h_box_8bottom.setAlignment(Qt.AlignCenter)

    confirm_stop_value_label = QLabel()

    confirm_stop_value_label.setFont(
        TextSetting("Arial", 30, True).font)
    confirm_stop_value_label.setWordWrap(True)
    confirm_stop_value_label.setAlignment(Qt.AlignCenter)
    confirm_stop_value_label.setFixedHeight(250)
    confirm_stop_value_label.setFixedWidth(400)
    confirm_stop_value_label.setText("<font color='red'> CAUTION! </font> <br> <font color='white'> This will immediately stop ventilation.")

    confirm_stop_cancel_button = window.makePicButton(
        "cancel",
        size=(60, 60),
    )
    confirm_stop_cancel_button.clicked.connect(lambda: window.display(0))

    confirm_stop_confirm_button = window.makePicButton(
        "confirm",
        size=(60, 60),
    )
    confirm_stop_confirm_button.clicked.connect(window.stopVentilation)
    confirm_stop_confirm_button.setFont(
        window.ui_settings.simple_button_settings.valueFont)

    h_box_8bottom.setSpacing(100)

    h_box_8top.addWidget(confirm_stop_value_label)
    h_box_8bottom.addWidget(confirm_stop_cancel_button)
    h_box_8bottom.addWidget(confirm_stop_confirm_button)
    v_box_8.addLayout(h_box_8top)
    v_box_8.addLayout(h_box_8bottom)

    window.page["8"].setLayout(v_box_8)


def initializeChangePatientWidget(window: MainWindow) -> None:
    v_box_9 = QVBoxLayout()
    h_box_9top = QHBoxLayout()
    h_box_9mid1 = QHBoxLayout()
    h_box_9mid2 = QHBoxLayout()
    h_box_9mid3 = QHBoxLayout()
    h_box_9bottom = QHBoxLayout()

    h_box_9top.setAlignment(Qt.AlignCenter)
    h_box_9mid1.setAlignment(Qt.AlignCenter)
    h_box_9mid2.setAlignment(Qt.AlignCenter)
    h_box_9mid3.setAlignment(Qt.AlignCenter)
    h_box_9bottom.setAlignment(Qt.AlignCenter)

    change_patient_main_label = QLabel("Change Patient")
    change_patient_main_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    change_patient_main_label.setWordWrap(True)
    change_patient_main_label.setAlignment(Qt.AlignCenter)
    change_patient_main_label.setFixedWidth(400)
    change_patient_main_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    window.patient_page_label = QLabel(
        f"Current Patient: Patient {window.patient_id_display}")
    window.patient_page_label.setAlignment(Qt.AlignCenter)
    window.patient_page_label.setFont(TextSetting("Arial", 20, True).font)
    window.patient_page_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    window.generate_new_patient_id_page_button = window.makeSimpleDisplayButton(
        "Generate New Patient ID",
        size=(250, 65))
    window.generate_new_patient_id_page_button.clicked.connect(
        window.generateNewPatientID)
    generate_new_patient_id_size_policy = window.generate_new_patient_id_page_button.sizePolicy(
    )
    generate_new_patient_id_size_policy.setRetainSizeWhenHidden(True)
    window.generate_new_patient_id_page_button.setSizePolicy(
        generate_new_patient_id_size_policy)

    change_patient_cancel = window.makePicButton("cancel")
    change_patient_cancel.clicked.connect(window.cancelNewPatientID)

    change_patient_apply = window.makePicButton("apply")
    change_patient_apply.clicked.connect(window.commitNewPatientID)

    change_patient_back = window.makeSimpleDisplayButton(
        "Back to Settings",
        size=(200, 65))
    change_patient_back.clicked.connect(lambda: window.display(6))

    h_box_9mid3.setSpacing(75)

    h_box_9top.addWidget(change_patient_main_label)
    h_box_9mid1.addWidget(window.patient_page_label)
    h_box_9mid2.addWidget(window.generate_new_patient_id_page_button)
    h_box_9mid3.addWidget(change_patient_cancel)
    h_box_9mid3.addWidget(change_patient_apply)
    h_box_9bottom.addWidget(change_patient_back)
    v_box_9.addLayout(h_box_9top)
    v_box_9.addLayout(h_box_9mid1)
    v_box_9.addLayout(h_box_9mid2)
    v_box_9.addLayout(h_box_9mid3)
    v_box_9.addLayout(h_box_9bottom)

    window.page["9"].setLayout(v_box_9)


def initializeChangeDatetimeWidget(window: MainWindow) -> None:
    page_settings = window.ui_settings.page_settings
    window.new_date = window.datetime.date()
    window.new_time = window.datetime.time()

    v_box_10 = QVBoxLayout()
    h_box_10top = QVBoxLayout()
    h_box_10bottom = QVBoxLayout()

    h_box_10top.setAlignment(Qt.AlignCenter)
    h_box_10bottom.setAlignment(Qt.AlignCenter)

    change_datetime_main_label = QLabel("Set Date/Time")
    change_datetime_main_label.setFont(page_settings.mainLabelFont)
    change_datetime_main_label.setAlignment(Qt.AlignCenter)
    change_datetime_main_label.setFixedWidth(400)
    change_datetime_main_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
    h_box_10top.addWidget(change_datetime_main_label)

    change_datetime_tab_widget = QTabWidget()

    date_widget = QWidget()
    date_widget.setFixedHeight(280)
    date_widget.setContentsMargins(0, 0, 0, 0)

    date_v_box = QVBoxLayout()
    date_h_box_1 = QHBoxLayout()
    date_v_box_11 = QVBoxLayout()
    date_v_box_12 = QVBoxLayout()
    date_v_box_13 = QVBoxLayout()
    date_h_box_2 = QHBoxLayout()
    date_h_box_21 = QHBoxLayout()
    date_h_box_22 = QHBoxLayout()

    date_month_increment = window.makePicButton("up")
    date_month_increment.setFixedWidth(50)
    date_month_increment.setFixedHeight(50)

    date_month_increment.clicked.connect(window.incrementMonth)

    date_month_decrement = window.makePicButton("down")
    date_month_decrement.setFixedWidth(50)
    date_month_decrement.setFixedHeight(50)
    date_month_decrement.clicked.connect(window.decrementMonth)

    date_day_increment = window.makePicButton("up")
    date_day_increment.setFixedWidth(50)
    date_day_increment.setFixedHeight(50)
    date_day_increment.clicked.connect(window.incrementDay)

    date_day_decrement = window.makePicButton("down")
    date_day_decrement.setFixedWidth(50)
    date_day_decrement.setFixedHeight(50)
    date_day_decrement.clicked.connect(window.decrementDay)

    date_year_increment = window.makePicButton("up")
    date_year_increment.setFixedHeight(50)
    date_year_increment.clicked.connect(window.incrementYear)

    date_year_decrement = window.makePicButton("down")
    date_year_decrement.setFixedHeight(50)

    date_year_decrement.clicked.connect(window.decrementYear)

    window.date_month_label = QLabel(str(window.datetime.date().month()))
    window.date_day_label = QLabel(str(window.datetime.date().day()))
    window.date_year_label = QLabel(str(window.datetime.date().year()))
    window.date_year_label.setFixedWidth(200)
    for label in [ window.date_month_label, window.date_day_label,  window.date_year_label]:
        label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    date_cancel = window.makePicButton("cancel")
    date_cancel.clicked.connect(window.cancelDate)

    date_apply = window.makePicButton("apply")
    date_apply.clicked.connect(window.commitDate)

    for date_label in [
            window.date_month_label, window.date_day_label,
            window.date_year_label
    ]:
        date_label.setFont(page_settings.setDatetimeFont)
        date_label.setAlignment(Qt.AlignCenter)

    date_month_increment_wrapper = QHBoxLayout()
    date_month_increment_wrapper.addWidget(date_month_increment)

    date_month_decrement_wrapper = QHBoxLayout()
    date_month_decrement_wrapper.addWidget(date_month_decrement)

    date_day_increment_wrapper = QHBoxLayout()
    date_day_increment_wrapper.addWidget(date_day_increment)

    date_day_decrement_wrapper = QHBoxLayout()
    date_day_decrement_wrapper.addWidget(date_day_decrement)

    date_year_increment_wrapper = QHBoxLayout()
    date_year_increment_wrapper.addWidget(date_year_increment)

    date_year_decrement_wrapper = QHBoxLayout()
    date_year_decrement_wrapper.addWidget(date_year_decrement)

    for wrapper in [
            date_month_increment_wrapper, date_month_decrement_wrapper,
            date_day_increment_wrapper, date_day_decrement_wrapper,
            date_year_increment_wrapper, date_year_decrement_wrapper
    ]:
        wrapper.setAlignment(Qt.AlignCenter)

    date_v_box_11.addLayout(date_month_increment_wrapper)
    date_v_box_11.addWidget(window.date_month_label)
    date_v_box_11.addLayout(date_month_decrement_wrapper)

    date_v_box_12.addLayout(date_day_increment_wrapper)
    date_v_box_12.addWidget(window.date_day_label)
    date_v_box_12.addLayout(date_day_decrement_wrapper)

    date_v_box_13.addLayout(date_year_increment_wrapper)
    date_v_box_13.addWidget(window.date_year_label)
    date_v_box_13.addLayout(date_year_decrement_wrapper)

    for v_box in [date_v_box_11, date_v_box_12, date_v_box_13]:
        v_box.setAlignment(Qt.AlignCenter)
        date_h_box_1.addLayout(v_box)

    date_h_box_21.addWidget(date_cancel)
    date_h_box_21.setAlignment(Qt.AlignCenter)
    date_h_box_22.addWidget(date_apply)
    date_h_box_22.setAlignment(Qt.AlignCenter)

    date_h_box_2.addLayout(date_h_box_21)
    date_h_box_2.addLayout(date_h_box_22)

    date_v_box.addLayout(date_h_box_1)
    date_v_box.addLayout(date_h_box_2)

    date_widget.setLayout(date_v_box)

    time_widget = QWidget()
    time_widget.setFixedHeight(280)
    time_widget.setContentsMargins(0, 0, 0, 0)

    time_v_box = QVBoxLayout()
    time_h_box_1 = QHBoxLayout()
    time_v_box_11 = QVBoxLayout()
    time_v_box_12 = QVBoxLayout()
    time_v_box_13 = QVBoxLayout()
    time_h_box_2 = QHBoxLayout()
    time_v_box_21 = QVBoxLayout()
    time_v_box_22 = QVBoxLayout()

    time_hour_increment = window.makePicButton("up")
    time_hour_increment.setFixedWidth(50)
    time_hour_increment.clicked.connect(lambda: window.incrementTime(3600))

    time_hour_decrement = window.makePicButton("down")
    time_hour_decrement.setFixedWidth(50)
    time_hour_decrement.clicked.connect(lambda: window.incrementTime(-3600))

    time_min_increment = window.makePicButton("up")
    time_min_increment.setFixedWidth(50)
    time_min_increment.clicked.connect(lambda: window.incrementTime(60))

    time_min_decrement = window.makePicButton("down")
    time_min_decrement.setFixedWidth(50)
    time_min_decrement.clicked.connect(lambda: window.incrementTime(-60))

    time_sec_increment = window.makePicButton("up")
    time_sec_increment.clicked.connect(lambda: window.incrementTime(1))

    time_sec_decrement = window.makePicButton("down")
    time_sec_decrement.clicked.connect(lambda: window.incrementTime(-1))

    window.time_hour_label = QLabel(str(window.datetime.time().hour()))
    window.time_min_label = QLabel(str(window.datetime.time().minute()))
    window.time_sec_label = QLabel(str(window.datetime.time().second()))
    window.date_year_label.setFixedWidth(200)

    for label in [ window.time_hour_label, window.time_min_label,  window.time_sec_label]:
        label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    time_cancel = window.makePicButton("cancel")
    time_cancel.clicked.connect(window.cancelTime)

    time_apply = window.makePicButton("apply")
    time_apply.clicked.connect(window.commitTime)

    for time_label in [window.time_hour_label,
                       window.time_min_label,
                       window.time_sec_label]:
        time_label.setFont(page_settings.setDatetimeFont)
        time_label.setAlignment(Qt.AlignCenter)

    time_hour_increment_wrapper = QHBoxLayout()
    time_hour_increment_wrapper.addWidget(time_hour_increment)

    time_hour_decrement_wrapper = QHBoxLayout()
    time_hour_decrement_wrapper.addWidget(time_hour_decrement)

    time_min_increment_wrapper = QHBoxLayout()
    time_min_increment_wrapper.addWidget(time_min_increment)

    time_min_decrement_wrapper = QHBoxLayout()
    time_min_decrement_wrapper.addWidget(time_min_decrement)

    time_sec_increment_wrapper = QHBoxLayout()
    time_sec_increment_wrapper.addWidget(time_sec_increment)

    time_sec_decrement_wrapper = QHBoxLayout()
    time_sec_decrement_wrapper.addWidget(time_sec_decrement)

    for wrapper in [time_hour_increment_wrapper, time_hour_decrement_wrapper,
                    time_min_increment_wrapper, time_min_decrement_wrapper,
                    time_sec_increment_wrapper, time_sec_decrement_wrapper]:
        wrapper.setAlignment(Qt.AlignCenter)

    time_v_box_11.addLayout(time_hour_increment_wrapper)
    time_v_box_11.addWidget(window.time_hour_label)
    time_v_box_11.addLayout(time_hour_decrement_wrapper)

    time_v_box_12.addLayout(time_min_increment_wrapper)
    time_v_box_12.addWidget(window.time_min_label)
    time_v_box_12.addLayout(time_min_decrement_wrapper)

    time_v_box_13.addLayout(time_sec_increment_wrapper)
    time_v_box_13.addWidget(window.time_sec_label)
    time_v_box_13.addLayout(time_sec_decrement_wrapper)

    for v_box in [time_v_box_11, time_v_box_12, time_v_box_13]:
        v_box.setAlignment(Qt.AlignCenter)
        time_h_box_1.addLayout(v_box)

    time_v_box_21.addWidget(time_cancel)
    time_v_box_21.setAlignment(Qt.AlignCenter)
    time_v_box_22.addWidget(time_apply)
    time_v_box_22.setAlignment(Qt.AlignCenter)

    time_h_box_2.addLayout(time_v_box_21)
    time_h_box_2.addLayout(time_v_box_22)

    time_v_box.addLayout(time_h_box_1)
    time_v_box.addLayout(time_h_box_2)

    time_widget.setLayout(time_v_box)

    date_widget.setAutoFillBackground(True)
    time_widget.setAutoFillBackground(True)

    change_datetime_tab_widget.addTab(date_widget, "Date")
    change_datetime_tab_widget.addTab(time_widget, "Time")

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Background, QColor("#2C2C2C"))
    change_datetime_tab_widget.setPalette(palette)

    h_box_10top.addWidget(change_datetime_tab_widget)

    v_box_10.addLayout(h_box_10top)
    v_box_10.setContentsMargins(10,10,10,10)

    window.page["10"].setLayout(v_box_10)


def initializeAlarmLimitWidget(window: MainWindow) -> None:

    v_box_11 = QVBoxLayout()  #main layout
    h_box_11_top = QHBoxLayout()

    alarm_limits_tabbed = QTabWidget()
    makeandAddAllAlarmSelectors(window, alarm_limits_tabbed)

    h_box_11_top.addWidget(alarm_limits_tabbed)
    v_box_11.addLayout(h_box_11_top)
    v_box_11.setContentsMargins(0, 0, 0, 0)

    window.page["11"].setLayout(v_box_11)


def makeandAddAllAlarmSelectors(window, tab_widget):
    window.alarmLimitSelectors = {}
    window.alarmLimitSelectorPairs = {}
    for limit_type in AlarmLimitType:
        selector = AlarmLimitSelector(window, limit_type)
        window.alarmLimitSelectors[limit_type] = selector

    for limit_type in AlarmLimitType:
        window.alarmLimitSelectors[limit_type].setPairSelector()

    count = 0
    for pair_type in AlarmLimitPair:
        pair = AlarmLimitSelectorPair(window, pair_type)
        window.alarmLimitSelectorPairs[pair_type] = pair
        tab_widget.addTab(pair, pair.tab_str)
        tab_widget.tabBar().setTabTextColor(count, QColor(255,255,255))
        count+=1

    tab_widget.setStyleSheet('''
        QTabBar::tab {
        background-color: #2C2C2C; 
        border: 1px solid rgb(255,255,255); 
        margin-left: 10px;
        margin-right: 10px;
        height: 40px;
        width: 80px;
        }

        QTabWidget {
        background-color: #2C2C2C;
        }
    
    ''')


def initializeWarningScreen(window: MainWindow) -> None:
    v_box_12 = QVBoxLayout()
    h_box_12_1 = QHBoxLayout()
    h_box_12_2 = QHBoxLayout()
    h_box_12_2.setAlignment(Qt.AlignCenter)

    window.warning_label = QLabel("")
    window.warning_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    window.warning_label.setWordWrap(True)
    window.warning_label.setAlignment(Qt.AlignCenter)
    window.warning_label.setFixedHeight(150)
    window.warning_label.setFixedWidth(400)
    window.warning_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    window.warning_ack_button =  window.makeSimpleDisplayButton("OK", size = (200,80))
    window.warning_ack_button.clicked.connect(lambda: window.display(0))

    h_box_12_1.addWidget(window.warning_label)
    h_box_12_2.addWidget(window.warning_ack_button)
    v_box_12.addLayout(h_box_12_1)
    v_box_12.addLayout(h_box_12_2)
    window.page["12"].setLayout(v_box_12)



def initializeStopVentilationAndPowerDownScreen(window: MainWindow) -> None:
    v_box_13 = QVBoxLayout()
    h_box_13top = QHBoxLayout()
    h_box_13bottom = QHBoxLayout()

    h_box_13top.setAlignment(Qt.AlignCenter)
    h_box_13bottom.setAlignment(Qt.AlignCenter)

    confirm_stop_and_power_down_value_label = QLabel(
        "Stop ventilation and power down the device?")
    confirm_stop_and_power_down_value_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    confirm_stop_and_power_down_value_label.setWordWrap(True)
    confirm_stop_and_power_down_value_label.setAlignment(Qt.AlignCenter)
    confirm_stop_and_power_down_value_label.setFixedHeight(150)
    confirm_stop_and_power_down_value_label.setFixedWidth(400)
    confirm_stop_and_power_down_value_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    confirm_stop_and_power_down_cancel_button = window.makePicButton(
        "cancel",
        size=(60, 60),
    )
    confirm_stop_and_power_down_cancel_button.clicked.connect(lambda: window.display(0))

    confirm_stop_and_power_down_confirm_button = window.makePicButton(
        "confirm",
        size=(60, 60),
    )
    confirm_stop_and_power_down_confirm_button.clicked.connect(window.powerDown)

    confirm_stop_and_power_down_confirm_button.setFont(
        window.ui_settings.simple_button_settings.valueFont)

    h_box_13bottom.setSpacing(100)

    h_box_13top.addWidget(confirm_stop_and_power_down_value_label)
    h_box_13bottom.addWidget(confirm_stop_and_power_down_cancel_button)
    h_box_13bottom.addWidget(confirm_stop_and_power_down_confirm_button)
    v_box_13.addLayout(h_box_13top)
    v_box_13.addLayout(h_box_13bottom)

    window.page["13"].setLayout(v_box_13)

def initializePowerDownScreen(window: MainWindow) -> None:
    v_box_14 = QVBoxLayout()
    h_box_14top = QHBoxLayout()
    h_box_14bottom = QHBoxLayout()

    h_box_14top.setAlignment(Qt.AlignCenter)
    h_box_14bottom.setAlignment(Qt.AlignCenter)

    confirm_power_down_value_label = QLabel(
        "Power down the device?")
    confirm_power_down_value_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    confirm_power_down_value_label.setWordWrap(True)
    confirm_power_down_value_label.setAlignment(Qt.AlignCenter)
    confirm_power_down_value_label.setFixedHeight(150)
    confirm_power_down_value_label.setFixedWidth(400)
    confirm_power_down_value_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    confirm_power_down_cancel_button = window.makePicButton(
        "cancel",
        size=(60, 60),
    )
    confirm_power_down_cancel_button.clicked.connect(lambda: window.display(0))

    confirm_power_down_confirm_button = window.makePicButton(
        "confirm",
        size=(60, 60),
    )
    confirm_power_down_confirm_button.clicked.connect(window.powerDown)

    confirm_power_down_confirm_button.setFont(
        window.ui_settings.simple_button_settings.valueFont)

    h_box_14bottom.setSpacing(100)

    h_box_14top.addWidget(confirm_power_down_value_label)
    h_box_14bottom.addWidget(confirm_power_down_cancel_button)
    h_box_14bottom.addWidget(confirm_power_down_confirm_button)
    v_box_14.addLayout(h_box_14top)
    v_box_14.addLayout(h_box_14bottom)

    window.page["14"].setLayout(v_box_14)

def initializeLostCommsScreen(window: MainWindow) -> None:
    v_box_15 = QVBoxLayout()
    h_box_15top = QHBoxLayout()
    h_box_15bottom = QHBoxLayout()

    h_box_15top.setAlignment(Qt.AlignCenter)
    h_box_15bottom.setAlignment(Qt.AlignCenter)

    comms_lost_value_label = QLabel(
        "Communications with controller lost!  Click OK to power down.")
    comms_lost_value_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    comms_lost_value_label.setWordWrap(True)
    comms_lost_value_label.setAlignment(Qt.AlignCenter)
    comms_lost_value_label.setFixedHeight(150)
    comms_lost_value_label.setFixedWidth(400)
    comms_lost_value_label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    comms_lost_cancel_button = window.makePicButton(
        "cancel",
        size=(60, 60),
    )
    comms_lost_cancel_button.clicked.connect(lambda: window.display(0))

    comms_lost_confirm_button = window.makePicButton(
        "confirm",
        size=(60, 60),
    )
    comms_lost_confirm_button.clicked.connect(window.powerDown)

    comms_lost_confirm_button.setFont(
        window.ui_settings.simple_button_settings.valueFont)

    h_box_15bottom.setSpacing(100)

    h_box_15top.addWidget(comms_lost_value_label)
    h_box_15bottom.addWidget(comms_lost_cancel_button)
    h_box_15bottom.addWidget(comms_lost_confirm_button)
    v_box_15.addLayout(h_box_15top)
    v_box_15.addLayout(h_box_15bottom)

    window.page["15"].setLayout(v_box_15)

def initializeCalibWidget(window: MainWindow) -> None:
    v_box_16 = QVBoxLayout()
    h_box_16_1 = QHBoxLayout()
    calib_label = QLabel("Calibration in progress. Please wait")
    calib_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
    calib_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    window.disableStartButton()
    window.disableMainButtons()

    h_box_16_1.addWidget(calib_label)
    v_box_16.addLayout(h_box_16_1)

    window.page["16"].setLayout(v_box_16)

def initializeReadyWidget(window: MainWindow) -> None:
    def beginVentilation():
        window.display(0)
        window.ready_to_ventilate_signal.emit()
        window.enableStartButton()
        window.enableMainButtons()

    v_box_17 = QVBoxLayout()
    h_box_17_1 = QHBoxLayout()
    h_box_17_2 = QHBoxLayout()

    ready_label = QLabel("Calibration completed. Please check initial settings, connect to patient, and start ventilation.")
    ready_label.setStyleSheet("QLabel {color: #FFFFFF ;}")
    ready_label.setFixedWidth(400)
    ready_label.setWordWrap(True)
    ready_label.setAlignment(Qt.AlignCenter)
    ready_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)

    ready_confirm = window.makePicButton("confirm")
    ready_confirm.clicked.connect(beginVentilation)

    h_box_17_1.addWidget(ready_label)
    h_box_17_2.addWidget(ready_confirm)

    for h_box in [h_box_17_1, h_box_17_2]:
        h_box.setAlignment(Qt.AlignCenter)
        v_box_17.addLayout(h_box)

    window.page["17"].setLayout(v_box_17)

def initializeSetupWidget(window: MainWindow) -> None:
    window.setup_stack = QStackedWidget()
    for step in range(1 , 5):
        window.setup_stack.addWidget(
            initializeSetupStepWidget(window, step, window.setup_stack)
        )


def initializeSetupStepWidget(window, step, stack):
    setup_messages = {"1": "Please confirm that the device is disconnected from the patient.",
                        "2": "Please ensure the pressure sensor is disconnected "
                             "from the breathing circuit",
                        "3": "Please ensure the airflow sensor is connected "
                             "to the breathing circuit",
                        "4": "Press Calibrate to begin calibration"
                        }

    setup_layout = QVBoxLayout()
    setup_sub_layouts = {str(j): QHBoxLayout() for j in range(1, 5)}

    logo_path = path.abspath(
        path.join(path.dirname(__file__), "images/lm_logo_dark.png"))
    setup_logo = window.makePicButton(
        logo_path,
        size=(370, 60),
        custom_path=True
    )

    setup_instruction = QLabel(setup_messages[str(step)])
    label_list = [setup_instruction]

    if step == 1:
        setup_header = QLabel("Welcome to the LifeMech Adaptive Ventilation System")
        label_list.append(setup_header)

    for label in label_list:
        label.setFont(window.ui_settings.page_settings.mainLabelFont)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(150)
        label.setFixedWidth(400)
        label.setStyleSheet("QLabel {color: #FFFFFF ;}")

    if step == 4:
        setup_confirm = window.makeSimpleDisplayButton("Calibrate", size=(200, 80))
        setup_confirm.clicked.connect(lambda: window.ready_to_calibrate_signal.emit())
    else:
        setup_confirm = window.makeSimpleDisplayButton("Confirm", size=(200, 80))
        setup_confirm.clicked.connect(lambda: stack.setCurrentIndex(step))

    setup_sub_layouts["1"].addWidget(setup_logo)
    if step == 1:
        setup_sub_layouts["2"].addWidget(setup_header)
    setup_sub_layouts["3"].addWidget(setup_instruction)
    setup_sub_layouts["4"].addWidget(setup_confirm)

    for j in range(1, 5):
        if j != 2 or step == 1:
            layout = setup_sub_layouts[str(j)]
            layout.setAlignment(Qt.AlignCenter)
            setup_layout.addLayout(layout)

    wrapper = QWidget()
    wrapper.setLayout(setup_layout)

    return wrapper









  


