"""
Widgets used to initialze the the OVVE UI
"""
from random import randint
from typing import TypeVar

import numpy as np
import pyqtgraph as pg

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from display.ui_settings import SimpleButtonSettings, FancyButtonSettings, DisplayRectSettings


# Used for documentation purposes only
MainWindow = TypeVar('MainWindow')


def initializeHomeScreenWidget(window: MainWindow) -> None:
    """ Creates Home Screen for Widgets """
    v_box_1_main = QVBoxLayout()

    h_box_11 = QHBoxLayout()
    h_box_12 = QHBoxLayout()

    v_box_11left = QVBoxLayout()
    v_box_11mid = QVBoxLayout()
    v_box_11right = QVBoxLayout()

    window.mode_button_main = window.makeSimpleDisplayButton(
        window.get_mode_display(window.settings.mode),
        size=(115, 65),
    )
    window.mode_button_main.clicked.connect(lambda: window.display(1))

    window.resp_rate_button_main = window.makeFancyDisplayButton(
        "Set Resp. Rate",
        window.settings.resp_rate,
        "b/min",
        size=(115, 65),
    )

    window.resp_rate_button_main.clicked.connect(lambda: window.display(2))

    window.tv_button_main = window.makeFancyDisplayButton(
        "Set Tidal Volume",
        window.settings.tv,
        "l/min",
        size=(115, 65),
    )
    window.tv_button_main.clicked.connect(lambda: window.display(3))

    window.ie_button_main = window.makeFancyDisplayButton(
        "Set I/E Ratio",
        window.get_ie_display(window.settings.ie_ratio),
        "l/min",
        size=(115, 65),
    )
    window.ie_button_main.clicked.connect(lambda: window.display(4))

    window.alarm_button_main = window.makeSimpleDisplayButton(
        "ALARM",
        size=(115, 65),
        button_settings=SimpleButtonSettings(borderColor="#FF0000",
                                             fillColor='#FFFFFF',
                                             valueColor='#FF0000'),
    )
    window.alarm_button_main.clicked.connect(lambda: window.display(5))

    window.start_button_main = window.makeSimpleDisplayButton(
        "START",
        size=(115, 65),
    )
    # TODO: Connect

    window.resp_rate_display_main = window.makeDisplayRect(
        "Resp. Rate",
        window.params.resp_rate_meas,
        "bpm",
        size=(175, 115),
    )

    window.tv_insp_display_main = window.makeDisplayRect(
        "TV Insp",
        window.params.tv_insp,
        "mL",
        size=(175, 115),
    )
    window.tv_exp_display_main = window.makeDisplayRect(
        "TV Exp",
        window.params.tv_exp,
        "mL",
        size=(175, 115),
    )

    window.peep_display_main = window.makeDisplayRect(
        "PEEP",
        window.params.peep,
        "cmH2O",
        size=(175, 115),
    )

    window.ppeak_display_main = window.makeDisplayRect(
        "Ppeak",
        window.params.ppeak,
        "cmH2O",
        size=(175, 115),
    )
    window.pplat_display_main = window.makeDisplayRect(
        "Pplat",
        window.params.pplat,
        "cmH2O",
        size=(175, 115),
    )

    axisStyle = {'color': 'black', 'font-size': '20pt'}
    graph_pen = pg.mkPen(width=5, color="b")

    graph_width = 400
    window.tv_insp_data = np.linspace(0, 0, graph_width)
    window.flow_graph_ptr = -graph_width

    # TODO: current graph system doesn't associate y values with x values.
    #       Need to fix?
    window.flow_graph = pg.PlotWidget()
    window.flow_graph.setFixedWidth(graph_width)
    window.flow_graph_line = window.flow_graph.plot(
        window.tv_insp_data,
        pen=graph_pen)  # shows Serial (tv_insp) data for now
    window.flow_graph.setBackground("w")
    window.flow_graph.setMouseEnabled(False, False)
    flow_graph_left_axis = window.flow_graph.getAxis("left")
    flow_graph_left_axis.setLabel("Flow", **axisStyle)  # TODO: Add units

    indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data = [randint(-10, 10) for _ in range(10)]

    window.pressure_graph = pg.PlotWidget()
    window.pressure_graph.setFixedWidth(graph_width)
    window.pressure_graph_line = window.pressure_graph.plot(indices,
                                                        data,
                                                        pen=graph_pen)
    window.pressure_graph.setBackground("w")
    window.pressure_graph.setMouseEnabled(False, False)
    pressure_graph_left_axis = window.pressure_graph.getAxis("left")
    pressure_graph_left_axis.setLabel("Pressure",
                                      **axisStyle)  # TODO: Add units

    window.volume_graph = pg.PlotWidget()
    window.volume_graph.setFixedWidth(graph_width)
    window.pressure_graph_line = window.volume_graph.plot(indices,
                                                      data,
                                                      pen=graph_pen)
    window.volume_graph.setBackground("w")
    window.volume_graph.setMouseEnabled(False, False)
    window.pressure_graph_left_axis = window.volume_graph.getAxis("left")
    window.pressure_graph_left_axis.setLabel("Volume",
                                           **axisStyle)  # TODO: Add units

    h_box_11.addWidget(window.mode_button_main)
    h_box_11.addWidget(window.resp_rate_button_main)
    h_box_11.addWidget(window.tv_button_main)
    h_box_11.addWidget(window.ie_button_main)
    h_box_11.addWidget(window.alarm_button_main)
    h_box_11.addWidget(window.start_button_main)

    v_box_11left.addWidget(window.resp_rate_display_main)
    v_box_11left.addWidget(window.tv_insp_display_main)
    v_box_11left.addWidget(window.tv_exp_display_main)

    v_box_11mid.addWidget(window.flow_graph)
    v_box_11mid.addWidget(window.pressure_graph)
    v_box_11mid.addWidget(window.volume_graph)

    v_box_11right.addWidget(window.peep_display_main)
    v_box_11right.addWidget(window.ppeak_display_main)
    v_box_11right.addWidget(window.pplat_display_main)

    h_box_12.addLayout(v_box_11left)
    h_box_12.addLayout(v_box_11mid)
    h_box_12.addLayout(v_box_11right)

    v_box_1_main.addLayout(h_box_11)
    v_box_1_main.addLayout(h_box_12)
    window.page["1"].setLayout(v_box_1_main)

def initializeModeWidget(window: MainWindow) -> None:
    """ Creates Mode Widget """
    v_box = QVBoxLayout()
    h_box_top = QHBoxLayout()
    h_box_mid= QHBoxLayout()
    h_box_bot = QHBoxLayout()

    mode_change = window.makeSimpleDisplayButton("CHANGE MODE")
    mode_apply = window.makeSimpleDisplayButton("APPLY")
    mode_cancel = window.makeSimpleDisplayButton("CANCEL")

    mode_change.clicked.connect(
        lambda: window.changeMode(not window.local_settings.mode))
    mode_apply.clicked.connect(lambda: window.commitMode())
    mode_cancel.clicked.connect(window.cancelChange)

    window.mode_page_rect = window.makeDisplayRect(
        "Mode", window.get_mode_display(window.settings.mode), "", size=(500, 200))

    h_box_top.addWidget(window.mode_page_rect)
    h_box_mid.addWidget(mode_change)
    h_box_bot.addWidget(mode_apply)
    h_box_bot.addWidget(mode_cancel)

    v_box.addLayout(h_box_top)
    v_box.addLayout(h_box_mid)
    v_box.addLayout(h_box_bot)

    window.page["2"].setLayout(v_box)


def initializeRespiratoryRateWidget(window) -> None:
    """ Creates Respiratory Rate Widget """
    v_box = QVBoxLayout()
    h_box_top = QHBoxLayout()
    h_box_mid = QHBoxLayout()
    h_box_bot = QHBoxLayout()

    window.resp_rate_page_rect = window.makeDisplayRect(
        "Resp. Rate",
        window.local_settings.resp_rate,
        "b/min",
        size=(500, 200))

    resp_rate_increment_button = window.makeSimpleDisplayButton(
        "+ " + str(window.resp_rate_increment))
    resp_rate_decrement_button = window.makeSimpleDisplayButton(
        "- " + str(window.resp_rate_increment))
    resp_rate_apply = window.makeSimpleDisplayButton("APPLY")
    resp_rate_cancel = window.makeSimpleDisplayButton("CANCEL")

    resp_rate_increment_button.clicked.connect(window.incrementRespRate)
    resp_rate_decrement_button.clicked.connect(window.decrementRespRate)
    resp_rate_apply.clicked.connect(window.commitRespRate)
    resp_rate_cancel.clicked.connect(window.cancelChange)

    h_box_top.addWidget(window.resp_rate_page_rect)
    h_box_mid.addWidget(resp_rate_increment_button)
    h_box_mid.addWidget(resp_rate_decrement_button)
    h_box_bot.addWidget(resp_rate_apply)
    h_box_bot.addWidget(resp_rate_cancel)

    v_box.addLayout(h_box_top)
    v_box.addLayout(h_box_mid)
    v_box.addLayout(h_box_bot)

    window.page["3"].setLayout(v_box)

def initializeTidalVolumeWidget(window: MainWindow):
    """ Creates Tidal Volume Widget """
    v_box = QVBoxLayout()
    h_box_top = QHBoxLayout()
    h_box_mid = QHBoxLayout()
    h_box_bot = QHBoxLayout()

    window.tv_page_rect = window.makeDisplayRect(
        "Tidal Volume",
        window.settings.tv,
        "l/min",
        size=(500, 200))

    tv_increment_button = window.makeSimpleDisplayButton(
        "+ " + str(window.tv_increment))
    tv_decrement_button = window.makeSimpleDisplayButton(
        "- " + str(window.tv_increment))
    tv_apply = window.makeSimpleDisplayButton("APPLY")
    tv_cancel = window.makeSimpleDisplayButton("CANCEL")

    tv_increment_button.clicked.connect(window.incrementTidalVol)
    tv_decrement_button.clicked.connect(window.decrementTidalVol)
    tv_apply.clicked.connect(window.commitTidalVol)
    tv_cancel.clicked.connect(window.cancelChange)

    h_box_top.addWidget(window.tv_page_rect)
    h_box_mid.addWidget(tv_increment_button)
    h_box_mid.addWidget(tv_decrement_button)
    h_box_bot.addWidget(tv_apply)
    h_box_bot.addWidget(tv_cancel)

    v_box.addLayout(h_box_top)
    v_box.addLayout(h_box_mid)
    v_box.addLayout(h_box_bot)

    window.page["4"].setLayout(v_box)


def initializeIERatioWidget(window: MainWindow):
    """ Creates i/e Ratio Widget """
    v_box = QVBoxLayout()
    h_box_top = QHBoxLayout()
    h_box_mid = QHBoxLayout()
    h_box_bot = QHBoxLayout()

    window.ie_page_rect = window.makeDisplayRect(
        "I/E Ratio", window.get_ie_display(window.settings.ie_ratio), "", size=(500, 200))

    ie_change_size = (150, 50)

    ie_change_0 = window.makeSimpleDisplayButton(
        window.get_ie_display(0), size=ie_change_size)
    ie_change_1 = window.makeSimpleDisplayButton(
        window.get_ie_display(1), size=ie_change_size)
    ie_change_2 = window.makeSimpleDisplayButton(
        window.get_ie_display(2), size=ie_change_size)
    ie_change_3 = window.makeSimpleDisplayButton(
        window.get_ie_display(3), size=ie_change_size)

    ie_apply = window.makeSimpleDisplayButton("APPLY")
    ie_cancel = window.makeSimpleDisplayButton("CANCEL")

    ie_change_0.clicked.connect(lambda: window.changeIERatio(0))
    ie_change_1.clicked.connect(lambda: window.changeIERatio(1))
    ie_change_2.clicked.connect(lambda: window.changeIERatio(2))
    ie_change_3.clicked.connect(lambda: window.changeIERatio(3))

    ie_apply.clicked.connect(window.commitIERatio)
    ie_cancel.clicked.connect(window.cancelChange)

    h_box_top.addWidget(window.ie_page_rect)
    h_box_mid.addWidget(ie_change_0)
    h_box_mid.addWidget(ie_change_1)
    h_box_mid.addWidget(ie_change_2)
    h_box_mid.addWidget(ie_change_3)

    h_box_bot.addWidget(ie_apply)
    h_box_bot.addWidget(ie_cancel)

    v_box.addLayout(h_box_top)
    v_box.addLayout(h_box_mid)
    v_box.addLayout(h_box_bot)

    window.page["5"].setLayout(v_box)

def initializeAlarmWidget(window: MainWindow): #Alarm
    v_box_6 = QVBoxLayout()
    h_box_6top = QHBoxLayout()
    #h_box_6middle = QHBoxLayout()
    h_box_6bottom = QHBoxLayout()

    alarm_ack = window.makeSimpleDisplayButton("Acknowledge")
    alarm_cancel= window.makeSimpleDisplayButton("Cancel")

    # Acknowledge alarm stops the alarms
    alarm_ack.clicked.connect(lambda: window.commitAlarm())
    alarm_cancel.clicked.connect(window.cancelChange)

    window.alarm_page_rect = window.makeDisplayRect("Alarm",
                                                    window.settings.get_alarm_display(),
                                                    "", size = (500,200))

    h_box_6top.addWidget(window.alarm_page_rect)
    #h_box_6middle.addWidget(alarm_toggle)
    h_box_6bottom.addWidget(alarm_ack)
    h_box_6bottom.addWidget(alarm_cancel)

    v_box_6.addLayout(h_box_6top)
    #v_box_6.addLayout(h_box_6middle)
    v_box_6.addLayout(h_box_6bottom)

    window.page["6"].setLayout(v_box_6)
