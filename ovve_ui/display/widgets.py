"""
Widgets used to initialze the the OVVE UI
"""
from random import randint

import numpy as np
import pyqtgraph as pg

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout


def initializeHomeScreenWidget(window) -> None:
    """ Creates Home Screen for Widgets """
    h_box_1 = QHBoxLayout()

    v_box_1left = QVBoxLayout()
    v_box_1mid = QVBoxLayout()
    v_box_1right = QVBoxLayout()

    window.mode_button_main = window.makeSimpleDisplayButton(
        window.settings.get_mode_display())
    window.mode_button_main.clicked.connect(lambda: window.display(1))

    window.resp_rate_button_main = window.makeFancyDisplayButton(
        "Resp. Rate", window.settings.resp_rate, "b/min")
    window.resp_rate_button_main.clicked.connect(lambda: window.display(2))

    window.minute_vol_button_main = window.makeFancyDisplayButton(
        "Minute Volume",
        window.settings.minute_volume,
        "l/min",
    )
    window.minute_vol_button_main.clicked.connect(lambda: window.display(3))

    window.ie_button_main = window.makeFancyDisplayButton(
        "I/E Ratio",
        window.settings.get_ie_display(),
        "l/min",
    )
    window.ie_button_main.clicked.connect(lambda: window.display(4))

    window.peep_display_main = window.makeDisplayRect(
        "PEEP",
        5,
        "cmH2O",
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

    v_box_1left.addWidget(window.mode_button_main)
    v_box_1left.addWidget(window.resp_rate_button_main)
    v_box_1left.addWidget(window.minute_vol_button_main)
    v_box_1left.addWidget(window.ie_button_main)
    v_box_1left.addWidget(window.peep_display_main)

    v_box_1mid.addWidget(window.flow_graph)
    v_box_1mid.addWidget(window.pressure_graph)
    v_box_1mid.addWidget(window.volume_graph)

    v_box_1right.addWidget(window.tv_insp_display_main)
    v_box_1right.addWidget(window.tv_exp_display_main)
    v_box_1right.addWidget(window.ppeak_display_main)
    v_box_1right.addWidget(window.pplat_display_main)

    h_box_1.addLayout(v_box_1left)
    h_box_1.addLayout(v_box_1mid)
    h_box_1.addLayout(v_box_1right)
    window.page["1"].setLayout(h_box_1)

def initializeModeWidget(window) -> None:
    """ Creates Mode Widget """
    v_box_2 = QVBoxLayout()
    h_box_2top = QHBoxLayout()
    h_box_2middle = QHBoxLayout()
    h_box_2bottom = QHBoxLayout()

    mode_change = window.makeSimpleDisplayButton("CHANGE MODE")
    mode_apply = window.makeSimpleDisplayButton("APPLY")
    mode_cancel = window.makeSimpleDisplayButton("CANCEL")

    mode_change.clicked.connect(
        lambda: window.changeMode(not window.local_settings.ac_mode))
    mode_apply.clicked.connect(lambda: window.commitMode())
    mode_cancel.clicked.connect(window.cancelChange)

    window.mode_page_rect = window.makeDisplayRect(
        "Mode",
        window.local_settings.get_mode_display(),
        "",
        size=(500, 200))

    h_box_2top.addWidget(window.mode_page_rect)
    h_box_2middle.addWidget(mode_change)
    h_box_2bottom.addWidget(mode_apply)
    h_box_2bottom.addWidget(mode_cancel)

    v_box_2.addLayout(h_box_2top)
    v_box_2.addLayout(h_box_2middle)
    v_box_2.addLayout(h_box_2bottom)

    window.page["2"].setLayout(v_box_2)

def initializeRespitoryRateWidget(window) -> None:
    """ Creates Respitory Rate Widget """
    v_box_3 = QVBoxLayout()
    h_box_3top = QHBoxLayout()
    h_box_3mid = QHBoxLayout()
    h_box_3bottom = QHBoxLayout()

    window.resp_rate_page_rect = window.makeDisplayRect(
        "Resp. Rate",
        window.local_settings.resp_rate,
        "b/min",
        size=(500, 200))

    resp_rate_increment_button = window.makeSimpleDisplayButton(
        "+ " + str(window.settings.resp_rate_increment))
    resp_rate_decrement_button = window.makeSimpleDisplayButton(
        "- " + str(window.settings.resp_rate_increment))
    resp_rate_apply = window.makeSimpleDisplayButton("APPLY")
    resp_rate_cancel = window.makeSimpleDisplayButton("CANCEL")

    resp_rate_increment_button.clicked.connect(window.incrementRespRate)
    resp_rate_decrement_button.clicked.connect(window.decrementRespRate)
    resp_rate_apply.clicked.connect(window.commitRespRate)
    resp_rate_cancel.clicked.connect(window.cancelChange)

    h_box_3top.addWidget(window.resp_rate_page_rect)
    h_box_3mid.addWidget(resp_rate_increment_button)
    h_box_3mid.addWidget(resp_rate_decrement_button)
    h_box_3bottom.addWidget(resp_rate_apply)
    h_box_3bottom.addWidget(resp_rate_cancel)

    v_box_3.addLayout(h_box_3top)
    v_box_3.addLayout(h_box_3mid)
    v_box_3.addLayout(h_box_3bottom)

    window.page["3"].setLayout(v_box_3)

def initializeMinuteVolumeWidget(window):
    """ Creates Minute Volume Widget """
    v_box_4 = QVBoxLayout()
    h_box_4top = QHBoxLayout()
    h_box_4mid = QHBoxLayout()
    h_box_4bottom = QHBoxLayout()

    window.minute_vol_page_rect = window.makeDisplayRect(
        "Minute Volume",
        window.local_settings.minute_volume,
        "l/min",
        size=(500, 200))

    minute_vol_increment_button = window.makeSimpleDisplayButton(
        "+ " + str(window.settings.minute_volume_increment))
    minute_vol_decrement_button = window.makeSimpleDisplayButton(
        "- " + str(window.settings.minute_volume_increment))
    minute_vol_apply = window.makeSimpleDisplayButton("APPLY")
    minute_vol_cancel = window.makeSimpleDisplayButton("CANCEL")

    minute_vol_increment_button.clicked.connect(window.incrementMinuteVol)
    minute_vol_decrement_button.clicked.connect(window.decrementMinuteVol)
    minute_vol_apply.clicked.connect(window.commitMinuteVol)
    minute_vol_cancel.clicked.connect(window.cancelChange)

    h_box_4top.addWidget(window.minute_vol_page_rect)
    h_box_4mid.addWidget(minute_vol_increment_button)
    h_box_4mid.addWidget(minute_vol_decrement_button)
    h_box_4bottom.addWidget(minute_vol_apply)
    h_box_4bottom.addWidget(minute_vol_cancel)

    v_box_4.addLayout(h_box_4top)
    v_box_4.addLayout(h_box_4mid)
    v_box_4.addLayout(h_box_4bottom)

    window.page["4"].setLayout(v_box_4)

def initializeIERatioWidget(window):
    """ Creates i/e Ratio Widget """
    v_box_5 = QVBoxLayout()
    h_box_5top = QHBoxLayout()
    h_box_5mid = QHBoxLayout()
    h_box_5bottom = QHBoxLayout()

    window.ie_page_rect = window.makeDisplayRect(
        "I/E Ratio", window.settings.get_ie_display(), "", size=(500, 200))

    ie_change_size = (150, 50)

    ie_change_0 = window.makeSimpleDisplayButton(
        window.settings.ie_ratio_display[0], size=ie_change_size)
    ie_change_1 = window.makeSimpleDisplayButton(
        window.settings.ie_ratio_display[1], size=ie_change_size)
    ie_change_2 = window.makeSimpleDisplayButton(
        window.settings.ie_ratio_display[2], size=ie_change_size)
    ie_change_3 = window.makeSimpleDisplayButton(
        window.settings.ie_ratio_display[3], size=ie_change_size)

    ie_apply = window.makeSimpleDisplayButton("APPLY")
    ie_cancel = window.makeSimpleDisplayButton("CANCEL")

    ie_change_0.clicked.connect(lambda: window.changeIERatio(0))
    ie_change_1.clicked.connect(lambda: window.changeIERatio(1))
    ie_change_2.clicked.connect(lambda: window.changeIERatio(2))
    ie_change_3.clicked.connect(lambda: window.changeIERatio(3))

    ie_apply.clicked.connect(window.commitIERatio)
    ie_cancel.clicked.connect(window.cancelChange)

    h_box_5top.addWidget(window.ie_page_rect)
    h_box_5mid.addWidget(ie_change_0)
    h_box_5mid.addWidget(ie_change_1)
    h_box_5mid.addWidget(ie_change_2)
    h_box_5mid.addWidget(ie_change_3)

    h_box_5bottom.addWidget(ie_apply)
    h_box_5bottom.addWidget(ie_cancel)

    v_box_5.addLayout(h_box_5top)
    v_box_5.addLayout(h_box_5mid)
    v_box_5.addLayout(h_box_5bottom)

    window.page["5"].setLayout(v_box_5)
