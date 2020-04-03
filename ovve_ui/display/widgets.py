"""
Widgets used to initialze the the OVVE UI
"""
from random import randint
from typing import TypeVar

import numpy as np
import pyqtgraph as pg

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout


# Used for documentation purposes only
MainWindow = TypeVar('MainWindow')


def initializeHomeScreenWidget(window: MainWindow) -> None:
    """ Creates Home Screen for Widgets """
    h_box = QHBoxLayout()
    v_box_left = QVBoxLayout()
    v_box_mid = QVBoxLayout()
    v_box_right = QVBoxLayout()

    window.mode_button_main = window.makeSimpleDisplayButton(
        window.get_mode_display(window.settings.mode))
    window.mode_button_main.clicked.connect(lambda: window.display(1))

    window.resp_rate_button_main = window.makeFancyDisplayButton(
        "Resp. Rate", window.settings.resp_rate, "b/min")
    window.resp_rate_button_main.clicked.connect(lambda: window.display(2))

    window.minute_vol_button_main = window.makeFancyDisplayButton(
        "Minute Volume", window.settings.tv, "l/min")
    window.minute_vol_button_main.clicked.connect(lambda: window.display(3))

    window.ie_button_main = window.makeFancyDisplayButton(
        "I/E Ratio", window.get_ie_display(window.settings.ie_ratio), "l/min")
    window.ie_button_main.clicked.connect(lambda: window.display(4))

    window.peep_display_main = window.makeDisplayRect(
        "PEEP", 5, "cmH2O")
    window.tv_insp_display_main = window.makeDisplayRect(
        "TV Insp", window.params.tv_insp, "mL")
    window.tv_exp_display_main = window.makeDisplayRect(
        "TV Exp", window.params.tv_exp, "mL")
    window.ppeak_display_main = window.makeDisplayRect(
        "Ppeak", window.params.ppeak, "cmH2O")
    window.pplat_display_main = window.makeDisplayRect(
        "Pplat", window.params.pplat, "cmH2O")

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
        window.tv_insp_data, pen=graph_pen)  # shows Serial (tv_insp) data for now
    window.flow_graph.setBackground("w")
    window.flow_graph.setMouseEnabled(False, False)
    flow_graph_left_axis = window.flow_graph.getAxis("left")
    flow_graph_left_axis.setLabel("Flow", **axisStyle)  # TODO: Add units

    indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data = [randint(-10, 10) for _ in range(10)]

    window.pressure_graph = pg.PlotWidget()
    window.pressure_graph.setFixedWidth(graph_width)
    window.pressure_graph_line = window.pressure_graph.plot(
        indices, data, pen=graph_pen)
    window.pressure_graph.setBackground("w")
    window.pressure_graph.setMouseEnabled(False, False)
    pressure_graph_left_axis = window.pressure_graph.getAxis("left")
    pressure_graph_left_axis.setLabel("Pressure", **axisStyle)  # TODO: Add units

    window.volume_graph = pg.PlotWidget()
    window.volume_graph.setFixedWidth(graph_width)
    window.pressure_graph_line = window.volume_graph.plot(
        indices, data, pen=graph_pen)
    window.volume_graph.setBackground("w")
    window.volume_graph.setMouseEnabled(False, False)
    window.pressure_graph_left_axis = window.volume_graph.getAxis("left")
    window.pressure_graph_left_axis.setLabel("Volume", **axisStyle)  # TODO: Add units

    v_box_left.addWidget(window.mode_button_main)
    v_box_left.addWidget(window.resp_rate_button_main)
    v_box_left.addWidget(window.minute_vol_button_main)
    v_box_left.addWidget(window.ie_button_main)
    v_box_left.addWidget(window.peep_display_main)

    v_box_mid.addWidget(window.flow_graph)
    v_box_mid.addWidget(window.pressure_graph)
    v_box_mid.addWidget(window.volume_graph)

    v_box_right.addWidget(window.tv_insp_display_main)
    v_box_right.addWidget(window.tv_exp_display_main)
    v_box_right.addWidget(window.ppeak_display_main)
    v_box_right.addWidget(window.pplat_display_main)

    h_box.addLayout(v_box_left)
    h_box.addLayout(v_box_mid)
    h_box.addLayout(v_box_right)
    
    window.page["1"].setLayout(h_box)


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


def initializeRespitoryRateWidget(window) -> None:
    """ Creates Respitory Rate Widget """
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

def initializeMinuteVolumeWidget(window: MainWindow):
    """ Creates Minute Volume Widget """
    v_box = QVBoxLayout()
    h_box_top = QHBoxLayout()
    h_box_mid = QHBoxLayout()
    h_box_bot = QHBoxLayout()

    window.minute_vol_page_rect = window.makeDisplayRect(
        "Minute Volume",
        window.local_settings.tv,
        "l/min",
        size=(500, 200))

    minute_vol_increment_button = window.makeSimpleDisplayButton(
        "+ " + str(window.minute_volume_increment))
    minute_vol_decrement_button = window.makeSimpleDisplayButton(
        "- " + str(window.minute_volume_increment))
    minute_vol_apply = window.makeSimpleDisplayButton("APPLY")
    minute_vol_cancel = window.makeSimpleDisplayButton("CANCEL")

    minute_vol_increment_button.clicked.connect(window.incrementMinuteVol)
    minute_vol_decrement_button.clicked.connect(window.decrementMinuteVol)
    minute_vol_apply.clicked.connect(window.commitMinuteVol)
    minute_vol_cancel.clicked.connect(window.cancelChange)

    h_box_top.addWidget(window.minute_vol_page_rect)
    h_box_mid.addWidget(minute_vol_increment_button)
    h_box_mid.addWidget(minute_vol_decrement_button)
    h_box_bot.addWidget(minute_vol_apply)
    h_box_bot.addWidget(minute_vol_cancel)

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
