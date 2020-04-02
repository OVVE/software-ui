from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TextSetting:
    def __init__(self, fontName, fontSize, bold):
        if bold:
            self.font = QFont(fontName, fontSize, QFont.Bold)
        else:
            self.font = QFont(fontName, fontSize)

#TODO: Abstract text placement
class FancyButtonSettings:
    def __init__(self, labelSetting = TextSetting("Times", 20, True),
                 numberSetting = TextSetting("Times", 36, True),
                 unitSetting = TextSetting("Times", 18, False),
                 fillColor = '#d2fcdc',
                 labelColor = '#3ed5f0',
                 numberColor = Qt.black,
                 unitColor = Qt.gray
                 ):

        self.labelFont = labelSetting.font
        self.numberFont = numberSetting.font
        self.unitFont = unitSetting.font
        self.fillColor = fillColor
        self.labelColor = labelColor
        self.numberColor = numberColor
        self.unitColor = unitColor

    def getFillBrush(self):
        return QBrush(QColor(self.fillColor))

    def getLabelPen(self):
        return QPen(QColor(self.labelColor))

    def getNumberPen(self):
        return QPen(QColor(self.numberColor))

    def getUnitPen(self):
        return QPen(QColor(self.unitColor))

#TODO: Abstract text placement
class SimpleButtonSettings:
    def __init__(self, valueSetting = TextSetting("Times", 20, True),
                 fillColor = '#d2fcdc',
                 valueColor = Qt.black
                 ):

        self.valueFont = valueSetting.font
        self.fillColor = fillColor
        self.valueColor = valueColor

    def getFillBrush(self):
        return QBrush(QColor(self.fillColor))

    def getValuePen(self):
        return QPen(QColor(self.valueColor))

class DisplayRectSettings:
    def __init__(self, labelSetting = TextSetting("Times", 20, True),
                 numberSetting = TextSetting("Times", 36, True),
                 unitSetting = TextSetting("Times", 18, False),
                 fillColor = '#c4dbff',
                 labelColor = '#3ed5f0',
                 numberColor = Qt.black,
                 unitColor = Qt.gray
                 ):
        self.labelFont = labelSetting.font
        self.numberFont = numberSetting.font
        self.unitFont = unitSetting.font
        self.fillColor = fillColor
        self.labelColor = labelColor
        self.numberColor = numberColor
        self.unitColor = unitColor

    def getFillBrush(self):
        return QBrush(QColor(self.fillColor))

    def getLabelPen(self):
        return QPen(QColor(self.labelColor))

    def getNumberPen(self):
        return QPen(QColor(self.numberColor))

    def getUnitPen(self):
        return QPen(QColor(self.unitColor))


class UISettings:
    def __init__(self, fancy_button_settings=FancyButtonSettings(),
                 simple_button_settings=SimpleButtonSettings(),
                 display_rect_settings=DisplayRectSettings(),
                 fancy_button_default_size=(200, 100), simple_button_default_size=(200, 50),
                 display_rect_default_size=(200, 100)):

        self.fancy_button_settings = fancy_button_settings
        self.simple_button_settings = simple_button_settings
        self.display_rect_settings = display_rect_settings
        self.fancy_button_default_size = fancy_button_default_size
        self.simple_button_default_size = simple_button_default_size
        self.display_rect_default_size = display_rect_default_size

    def set_fancy_button_settings(self, new_settings):
        self.fancy_button_settings = new_settings

    def set_simple_button_settings(self, new_settings):
        self.simple_button_settings = new_settings

    def set_display_rect_settings(self, new_settings):
        self.display_rect_settings = new_settings
