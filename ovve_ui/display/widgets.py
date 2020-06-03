"""
Widgets used to initialize the the OVVE UI
"""
from random import randint
from typing import TypeVar
from os import path
import numpy as np
import pyqtgraph as pg

from PyQt5.QtWidgets import (QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
                             QLabel)
from PyQt5.QtCore import Qt

from display.ui_settings import (SimpleButtonSettings, FancyButtonSettings,
                                 DisplayRectSettings, PageSettings,
                                 TextSetting)
from display.selectors import AlarmLimitSelector

# Used for documentation purposes only
MainWindow = TypeVar('MainWindow')


def initializeHomeScreenWidget(
        window: MainWindow) -> (QVBoxLayout, QStackedWidget):
    """ Creates Home Screen for Widgets """
    layout = QVBoxLayout()
    h_box_1 = QHBoxLayout()
    h_box_2 = QHBoxLayout()
    h_box_3 = QHBoxLayout()

    h_box_1left = QHBoxLayout()
    h_box_1mid= QHBoxLayout()
    h_box_1right = QHBoxLayout()

    h_box_1right.setAlignment(Qt.AlignRight)

    h_box_2.setAlignment(Qt.AlignCenter)

    v_box_3left = QVBoxLayout()
    v_box_3mid = QVBoxLayout()
    v_box_3right = QVBoxLayout()

    main_logo_path = path.abspath(path.join(path.dirname(__file__), "images/lm_logo_light.png"))
    main_logo = window.makePicButton(
        main_logo_path,
        size = (215, 50),
    )

    window.main_patient_label = QLabel(f"Current Patient: Patient {window.patient_id_display}")
    window.main_patient_label.setFont(window.ui_settings.page_settings.topBarFont)
    window.main_patient_label.setStyleSheet("QLabel {color: #000000 ;}")


    window.main_datetime_label = QLabel(window.datetime.toString()[:-8])
    window.main_datetime_label.setFont(window.ui_settings.page_settings.topBarFont)
    window.main_datetime_label.setStyleSheet("QLabel {color: #000000 ;}")


    window.main_battery_level_label = QLabel(f"{window.params.battery_level}%")
    window.main_battery_level_label.setFont(window.ui_settings.page_settings.topBarFont)
    window.main_battery_level_label.setFixedWidth(50)
    window.main_battery_level_label.setStyleSheet("QLabel {color: #000000 ;}")

    main_battery_icon_path = path.abspath(path.join(path.dirname(__file__),
                                            f"images/batteries/light_theme/{window.battery_img}"))
    window.main_battery_icon = window.makePicButton(
        main_battery_icon_path,
        size = (30, 15),
    )

    window.mode_button_main = window.makeSimpleDisplayButton(
        window.get_mode_display(window.settings.mode), size = (126,64))
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

    window.start_stop_button_main = window.makeSimpleDisplayButton("START", size = (126,64))
    window.start_stop_button_main.clicked.connect(window.changeStartStop)

    settings_icon_path = path.abspath(path.join(path.dirname(__file__), "images/gear.png"))
    window.settings_button_main = window.makePicButton(
        settings_icon_path, size=(60, 60))
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
                                          labelColor="#A9A9A9",
                                          unitColor="#A9A9A9"),
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
    h_box_1mid.addWidget(window.main_patient_label)
    h_box_1mid.addWidget(window.main_datetime_label)

    h_box_1mid.setSpacing(18)

    h_box_1right.addWidget(window.main_battery_level_label)
    h_box_1right.addWidget(window.main_battery_icon)

    h_box_1right.setSpacing(0)



    for button in [window.mode_button_main,
                   window.resp_rate_button_main,
                   window.tv_button_main,
                   window.ie_button_main,
                   window.start_stop_button_main,
                   window.settings_button_main,
                   ]:
        h_box_2.addWidget(button)

    for left_display in [window.resp_rate_display_main,
                    window.tv_insp_display_main,
                    window.tv_exp_display_main,
                    ]:
        v_box_3left.addWidget(left_display)

    stack = QStackedWidget()
    v_box_3mid.addWidget(stack)

    for right_display in [window.peep_display_main,
                    window.ppeak_display_main,
                    window.pplat_display_main,
                    ]:
        v_box_3right.addWidget(right_display)

    for h_layout1 in [h_box_1left,
                      h_box_1mid,
                     h_box_1right,
                     ]:
        h_box_1.addLayout(h_layout1)

    for v_layout3 in [v_box_3left,
                     v_box_3mid,
                     v_box_3right,
                     ]:
        h_box_3.addLayout(v_layout3)

    h_box_3.setSpacing(18)

    for h_layout in [h_box_1,
                     h_box_2,
                     h_box_3]:
        layout.addLayout(h_layout)

    return layout, stack


#TODO: Add Units
def initializeGraphWidget(window: MainWindow) -> None:
    v_box = QVBoxLayout()
    axisStyle = {'color': 'black', 'font-size': '20pt'}
    window.new_graph_pen = pg.mkPen(width=2, color="b")
    window.cache_graph_pen = pg.mkPen(width=2, color="k")

    # TODO: Adjust graph width for resp rate
    window.graph_width = 60
    window.graph_ptr = 0
    label_style = {'color': 'k', 'font-size': '16pt'}

    window.pressure_data = np.empty([window.graph_width, ])
    window.pressure_graph = pg.PlotWidget()
    # TODO: Find good values for ranges of pressure, 40 cmH2O is the max before overpressure value pops
    window.pressure_graph.setYRange(-45, 45, padding=0)

    window.pressure_graph_line = window.pressure_graph.plot(
        window.pressure_data, pen=window.new_graph_pen)
    window.pressure_graph_cache_line = window.pressure_graph.plot(
        window.pressure_data, pen=window.cache_graph_pen)
    window.pressure_graph_cache_line.hide()
    window.pressure_graph_line.hide()

    window.pressure_graph_left_axis = window.pressure_graph.getAxis("left")
    window.pressure_graph_left_axis.setLabel("Press. (cmH2O)", **label_style)

    window.flow_data = np.empty([window.graph_width,])
    window.flow_graph = pg.PlotWidget()
    window.flow_graph.setYRange(-15, 75, padding=0) #Flow should be presented in L/min.
    window.flow_graph_line = window.flow_graph.plot(window.flow_data,
                                                    pen=window.new_graph_pen)
    window.flow_graph_cache_line = window.flow_graph.plot(
        window.flow_data, pen=window.cache_graph_pen)
    window.flow_graph_cache_line.hide()
    window.flow_graph_line.hide()

    window.flow_graph_left_axis = window.flow_graph.getAxis("left")
    window.flow_graph_left_axis.setLabel("Flow (L/min.)", **label_style)

    window.volume_data = np.empty([window.graph_width,])
    window.volume_graph = pg.PlotWidget()
    # TODO: Find good values for ranges of volume, just picked a pretty big number for now
    window.volume_graph.setYRange(-200, 1200, padding=0)
    window.volume_graph_line = window.volume_graph.plot(
        window.volume_data, pen=window.new_graph_pen)
    window.volume_graph_cache_line = window.volume_graph.plot(
        window.volume_data, pen=window.cache_graph_pen)
    window.volume_graph_cache_line.hide()
    window.volume_graph_line.hide()

    window.volume_graph_left_axis = window.volume_graph.getAxis("left")
    window.volume_graph_left_axis.setLabel("Volume (mL)", **label_style)

    for graph in [window.pressure_graph, window.flow_graph, window.volume_graph]:
        graph.setXRange(0, window.graph_width, padding=0)
        graph.setBackground("w")
        graph.setMouseEnabled(False, False)
        graph.getPlotItem().hideAxis('bottom')
        v_box.addWidget(graph)

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


    mode_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor= page_settings.cancelColor,
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

    resp_rate_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor= page_settings.cancelColor,
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor="#FFFFFF"))

    resp_rate_apply = window.makeSimpleDisplayButton(
        "APPLY",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor=page_settings.commitColor,
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor="#FFFFFF"))

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


    tv_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor= page_settings.cancelColor,
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor="#FFFFFF"))


    tv_apply = window.makeSimpleDisplayButton(
        "APPLY",
        size = (150,90),
        button_settings=SimpleButtonSettings(
            fillColor= page_settings.commitColor,
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor="#FFFFFF",
            ))

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


    ie_ratio_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor= page_settings.cancelColor,
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor="#FFFFFF"))

    ie_ratio_apply = window.makeSimpleDisplayButton(
        "APPLY",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor=page_settings.commitColor,
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor="#FFFFFF"))

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
    window.alarm_display_label.setStyleSheet("QLabel {color: #000000 ;}")
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
    settings_page_label.setStyleSheet("QLabel {color: #000000 ;}")

    settings_page_label.setAlignment(Qt.AlignCenter)

    window.settings_patient_label = QLabel(
        f"Current Patient: Patient {window.patient_id_display}")
    window.settings_patient_label.setAlignment(Qt.AlignCenter)
    window.settings_patient_label.setFont(TextSetting("Arial", 20, True).font)
    window.settings_patient_label.setStyleSheet("QLabel {color: #000000 ;}")


    settings_change_patient_button = window.makeSimpleDisplayButton(
        "Change Patient",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(150, 65))
    settings_change_patient_button.clicked.connect(lambda: window.display(8))

    settings_change_datetime_button = window.makeSimpleDisplayButton(
        "Change Date/Time",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(150, 65))
    settings_change_datetime_button.clicked.connect(lambda: window.display(9))

    settings_change_alarm_limits_button = window.makeSimpleDisplayButton(
        "Change Alarm Limits",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(150, 65))
    settings_change_alarm_limits_button.clicked.connect(lambda: window.display(10))

    settings_back_button = window.makeSimpleDisplayButton(
        "Back to Main",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(200, 65))
    settings_back_button.clicked.connect(lambda: window.display(0))

    h_box_7top.addWidget(settings_page_label)
    h_box_7mid1_v1.addWidget(window.settings_patient_label)
    h_box_7mid1_v2.addWidget(settings_change_patient_button)
    h_box_7mid1_v2.addWidget(settings_change_datetime_button)
    h_box_7mid1_v2.addWidget(settings_change_alarm_limits_button)
    h_box_7bottom.addWidget(settings_back_button)
    h_box_7mid1.addLayout(h_box_7mid1_v1)
    h_box_7mid1.addLayout(h_box_7mid1_v2)

    for h_box in [h_box_7top, h_box_7mid1,h_box_7mid2, h_box_7bottom]:
        v_box_7.addLayout(h_box)

    window.page["7"].setLayout(v_box_7)


def initializeConfirmStopWidget(window: MainWindow) -> None:
    v_box_8 = QVBoxLayout()
    h_box_8top = QHBoxLayout()
    h_box_8bottom = QHBoxLayout()

    h_box_8top.setAlignment(Qt.AlignCenter)
    h_box_8bottom.setAlignment(Qt.AlignCenter)

    confirm_stop_value_label = QLabel(
        "Caution: this will stop ventilation immediately. "
        "Proceed?")
    confirm_stop_value_label.setFont(
        window.ui_settings.page_settings.mainLabelFont)
    confirm_stop_value_label.setWordWrap(True)
    confirm_stop_value_label.setAlignment(Qt.AlignCenter)
    confirm_stop_value_label.setFixedHeight(150)
    confirm_stop_value_label.setFixedWidth(400)
    confirm_stop_value_label.setStyleSheet("QLabel {color: #000000 ;}")

    confirm_stop_cancel_button = window.makeSimpleDisplayButton(
        "CANCEL",
        size = (150,90),
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            valueColor="#FFFFFF",
            fillColor=window.ui_settings.page_settings.cancelColor,
            borderColor=window.ui_settings.page_settings.cancelColor))
    confirm_stop_cancel_button.clicked.connect(lambda: window.display(0))
    confirm_stop_cancel_button.setFont(
        window.ui_settings.simple_button_settings.valueFont)

    confirm_stop_confirm_button = window.makeSimpleDisplayButton(
        "CONFIRM",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.commitSetting,
            valueColor="#FFFFFF",
            fillColor=window.ui_settings.page_settings.commitColor,
            borderColor=window.ui_settings.page_settings.commitColor))
    confirm_stop_confirm_button.clicked.connect(window.stopVentilation)
    confirm_stop_confirm_button.setFont(
        window.ui_settings.simple_button_settings.valueFont)

    h_box_8bottom.setSpacing(75)

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
    change_patient_main_label.setStyleSheet("QLabel {color: #000000 ;}")


    window.patient_page_label = QLabel(
        f"Current Patient: Patient {window.patient_id_display}")
    window.patient_page_label.setAlignment(Qt.AlignCenter)
    window.patient_page_label.setFont(TextSetting("Arial", 20, True).font)
    window.patient_page_label.setStyleSheet("QLabel {color: #000000 ;}")

    window.generate_new_patient_id_page_button = window.makeSimpleDisplayButton(
        "Generate New Patient ID",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(250, 65))
    window.generate_new_patient_id_page_button.clicked.connect(
        window.generateNewPatientID)
    generate_new_patient_id_size_policy = window.generate_new_patient_id_page_button.sizePolicy(
    )
    generate_new_patient_id_size_policy.setRetainSizeWhenHidden(True)
    window.generate_new_patient_id_page_button.setSizePolicy(
        generate_new_patient_id_size_policy)

    change_patient_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor= window.ui_settings.page_settings.cancelColor,
            borderColor=window.ui_settings.page_settings.cancelColor,
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            valueColor="#FFFFFF"))

    change_patient_cancel.clicked.connect(window.cancelNewPatientID)

    change_patient_apply = window.makeSimpleDisplayButton(
        "APPLY",
        size=(150, 90),
        button_settings=SimpleButtonSettings(
            fillColor= window.ui_settings.page_settings.commitColor,
            borderColor=window.ui_settings.page_settings.commitColor,
            valueSetting=window.ui_settings.page_settings.commitSetting,
            valueColor="#FFFFFF"))
    change_patient_apply.clicked.connect(window.commitNewPatientID)

    change_patient_back = window.makeSimpleDisplayButton(
        "Back to Settings",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
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
    h_box_10mid = QVBoxLayout()
    h_box_10bottom = QVBoxLayout()

    h_box_10top.setAlignment(Qt.AlignCenter)
    h_box_10mid.setAlignment(Qt.AlignCenter)
    h_box_10bottom.setAlignment(Qt.AlignCenter)

    change_datetime_main_label = QLabel("Set Date/Time")
    change_datetime_main_label.setFont(page_settings.mainLabelFont)
    change_datetime_main_label.setWordWrap(True)
    change_datetime_main_label.setAlignment(Qt.AlignCenter)
    change_datetime_main_label.setFixedWidth(400)
    change_datetime_main_label.setStyleSheet("QLabel {color: #000000 ;}")

    change_datetime_stack_widget = QStackedWidget()

    date_widget = QWidget()
    date_widget.setFixedHeight(250)
    date_widget.setContentsMargins(0,0,0,0)

    date_v_box = QVBoxLayout()
    date_h_box_1 = QHBoxLayout()
    date_v_box_11 = QVBoxLayout()
    date_v_box_12 = QVBoxLayout()
    date_v_box_13 = QVBoxLayout()
    date_h_box_2 = QHBoxLayout()
    date_v_box_21 = QVBoxLayout()
    date_v_box_22 = QVBoxLayout()

    date_month_increment = window.makeSimpleDisplayButton(
        "+",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))
    date_month_increment.setFixedWidth(50)
    date_month_increment.clicked.connect(window.incrementMonth)

    date_month_decrement = window.makeSimpleDisplayButton(
        "-",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))
    date_month_decrement.setFixedWidth(50)
    date_month_decrement.clicked.connect(window.decrementMonth)

    date_day_increment = window.makeSimpleDisplayButton(
        "+",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))
    date_day_increment.setFixedWidth(50)
    date_day_increment.clicked.connect(window.incrementDay)

    date_day_decrement = window.makeSimpleDisplayButton(
        "-",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))
    date_day_decrement.setFixedWidth(50)
    date_day_decrement.clicked.connect(window.decrementDay)

    date_year_increment = window.makeSimpleDisplayButton(
        "+",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))
    date_year_increment.clicked.connect(window.incrementYear)

    date_year_decrement = window.makeSimpleDisplayButton(
        "-",
        size=(50, 50),
        button_settings=SimpleButtonSettings(
            fillColor="#FFFFFF",
            borderColor=page_settings.changeButtonBorderColor,
            valueSetting=page_settings.changeButtonTextSetting,
            valueColor=page_settings.changeButtonValueColor))
    date_year_decrement.clicked.connect(window.decrementYear)

    window.date_month_label = QLabel(str(window.datetime.date().month()))
    window.date_day_label = QLabel(str(window.datetime.date().day()))
    window.date_year_label = QLabel(str(window.datetime.date().year()))
    window.date_year_label.setFixedWidth(200)


    date_cancel = window.makeSimpleDisplayButton(
        "CANCEL",
        size=(150, 60),
        button_settings=SimpleButtonSettings(
            fillColor=page_settings.cancelColor,
            borderColor=page_settings.cancelColor,
            valueSetting=page_settings.cancelSetting,
            valueColor="#FFFFFF"))
    date_cancel.clicked.connect(window.cancelDate)

    date_apply = window.makeSimpleDisplayButton(
        "APPLY",
        size=(150, 60),
        button_settings=SimpleButtonSettings(
            fillColor=page_settings.commitColor,
            borderColor=page_settings.commitColor,
            valueSetting=page_settings.commitSetting,
            valueColor="#FFFFFF"))
    date_apply.clicked.connect(window.commitDate)

    for date_label in [window.date_month_label,
                           window.date_day_label,
                           window.date_year_label]:
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

    for wrapper in [date_month_increment_wrapper, date_month_decrement_wrapper,
                    date_day_increment_wrapper, date_day_decrement_wrapper,
                    date_year_increment_wrapper, date_year_decrement_wrapper]:
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

    date_v_box_21.addWidget(date_cancel)
    date_v_box_21.setAlignment(Qt.AlignCenter)
    date_v_box_22.addWidget(date_apply)
    date_v_box_22.setAlignment(Qt.AlignCenter)

    date_h_box_2.addLayout(date_v_box_21)
    date_h_box_2.addLayout(date_v_box_22)

    date_v_box.addLayout(date_h_box_1)
    date_v_box.addLayout(date_h_box_2)

    date_widget.setLayout(date_v_box)

    #TODO: Add time setting

    for widget in [date_widget]:
        change_datetime_stack_widget.addWidget(widget)

    datetime_back = window.makeSimpleDisplayButton(
        "Back to Settings",
        button_settings=SimpleButtonSettings(
            valueSetting=page_settings.cancelSetting,
            fillColor=page_settings.alarmSilenceButtonColor
        ),
        size=(200, 50))
    datetime_back.clicked.connect(lambda: window.display(6))

    h_box_10mid.addWidget(change_datetime_stack_widget)
    h_box_10bottom.addWidget(datetime_back)

    v_box_10.addLayout(h_box_10top)
    v_box_10.addLayout(h_box_10mid)
    v_box_10.addLayout(h_box_10bottom)

    window.page["10"].setLayout(v_box_10)

def initializeAlarmLimitWidget(window: MainWindow) -> None:
    v_box_11 = QVBoxLayout() #main layout
    h_box_11_back = QHBoxLayout() #back button

    window.high_pressure_limit_selector = AlarmLimitSelector(window=window,
                                                            main_label_text="Upper Pressure Alarm",
                                                            value=window.settings.high_pressure_limit,
                                                             increment=window.settings.pressure_alarm_limit_increment
                                                             )

    window.low_pressure_limit_selector = AlarmLimitSelector(window=window,
                                                           main_label_text="Lower Pressure Alarm",
                                                           value=window.settings.low_pressure_limit,
                                                           increment = window.settings.pressure_alarm_limit_increment
                                                           )


    window.high_volume_limit_selector = AlarmLimitSelector(window=window,
                                                          main_label_text="Upper Volume Alarm",
                                                          value=window.settings.high_volume_limit,
                                                            settable = False
                                                            )

    window.low_volume_limit_selector = AlarmLimitSelector(window=window,
                                                      main_label_text="Lower Volume Alarm",
                                                      value=window.settings.low_volume_limit,
                                                      settable = False
                                                      )


    window.high_rr_limit_selector = AlarmLimitSelector(window=window,
                                                      main_label_text="Upper Resp. Rate Alarm",
                                                      value=window.settings.high_resp_rate_limit,
                                                      increment = window.settings.resp_rate_alarm_limit_increment,
                                                      )

    window.low_rr_limit_selector = AlarmLimitSelector(window = window,
                                                      main_label_text = "Lower Resp. Rate Alarm",
                                                      value = window.settings.low_resp_rate_limit,
                                                      increment = window.settings.resp_rate_alarm_limit_increment,
                                                      )


    alarm_limits_back = window.makeSimpleDisplayButton(
        "Back to Settings",
        button_settings=SimpleButtonSettings(
            valueSetting=window.ui_settings.page_settings.cancelSetting,
            fillColor=window.ui_settings.page_settings.alarmSilenceButtonColor
        ),
        size=(200, 65))
    alarm_limits_back.clicked.connect(lambda: window.display(6))
    h_box_11_back.addWidget(alarm_limits_back)
    h_box_11_back.setAlignment(Qt.AlignCenter)


    for alarm_selector in [window.high_pressure_limit_selector,
                           window.low_pressure_limit_selector,
                           window.high_volume_limit_selector,
                           window.low_volume_limit_selector,
                           window.high_rr_limit_selector,
                           window.low_rr_limit_selector,
                           ]:

        v_box_11.addWidget(alarm_selector)

    v_box_11.addLayout(h_box_11_back)
    v_box_11.setSpacing(10)
    v_box_11.setContentsMargins(0,0,0,0)

    window.page["11"].setLayout(v_box_11)
