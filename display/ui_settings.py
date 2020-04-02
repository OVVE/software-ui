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
                 valueSetting = TextSetting("Times", 36, True),
                 unitSetting = TextSetting("Times", 18, False),
                 fillColor = '#d2fcdc',
                 labelColor = '#3ed5f0',
                 valueColor = Qt.black,
                 unitColor = Qt.gray,
                 default_size = (150,80)
                 ):

        self.labelFont = labelSetting.font
        self.valueFont = valueSetting.font
        self.unitFont = unitSetting.font
        self.fillColor = fillColor
        self.labelColor = labelColor
        self.valueColor = valueColor
        self.unitColor = unitColor
        self.default_size = default_size

    def getFillBrush(self):
        return QBrush(QColor(self.fillColor))

    def getLabelPen(self):
        return QPen(QColor(self.labelColor))

    def getValuePen(self):
        return QPen(QColor(self.valueColor))

    def getUnitPen(self):
        return QPen(QColor(self.unitColor))

    def getLabelCoords(self, size = None):
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 1 / 5)

    def getValueCoords(self, size = None):
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 3 / 5)

    def getUnitCoords(self, size = None):
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 9 / 10)

class SimpleButtonSettings:
    def __init__(self, valueSetting = TextSetting("Times", 20, True),
                 fillColor = '#d2fcdc',
                 valueColor = Qt.black,
                 default_size = (150,25)
                 ):

        self.valueFont = valueSetting.font
        self.fillColor = fillColor
        self.valueColor = valueColor
        self.default_size = default_size

    def getFillBrush(self):
        return QBrush(QColor(self.fillColor))

    def getValuePen(self):
        return QPen(QColor(self.valueColor))

    def getValueCoords(self, size=None):
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 4 / 5)

class DisplayRectSettings:
    def __init__(self, labelSetting = TextSetting("Times", 20, True),
                 valueSetting = TextSetting("Times", 36, True),
                 unitSetting = TextSetting("Times", 18, False),
                 fillColor = '#c4dbff',
                 labelColor = '#3ed5f0',
                 valueColor = Qt.black,
                 unitColor = Qt.gray,
                 default_size = (150,80)
                 ):
        self.labelFont = labelSetting.font
        self.valueFont = valueSetting.font
        self.unitFont = unitSetting.font
        self.fillColor = fillColor
        self.labelColor = labelColor
        self.valueColor = valueColor
        self.unitColor = unitColor
        self.default_size = default_size

    def getFillBrush(self):
        return QBrush(QColor(self.fillColor))

    def getLabelPen(self):
        return QPen(QColor(self.labelColor))

    def getValuePen(self):
        return QPen(QColor(self.valueColor))

    def getUnitPen(self):
        return QPen(QColor(self.unitColor))

    def getLabelCoords(self, size = None):
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 1 / 5)

    def getValueCoords(self, size = None):
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 3 / 5)

    def getUnitCoords(self, size = None):
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4),\
               int(use_size[1] * 9 / 10)

class UISettings:
    def __init__(self, fancy_button_settings=FancyButtonSettings(),
                 simple_button_settings=SimpleButtonSettings(),
                 display_rect_settings=DisplayRectSettings()):

        self.fancy_button_settings = fancy_button_settings
        self.simple_button_settings = simple_button_settings
        self.display_rect_settings = display_rect_settings

    def set_fancy_button_settings(self, new_settings):
        self.fancy_button_settings = new_settings

    def set_simple_button_settings(self, new_settings):
        self.simple_button_settings = new_settings

    def set_display_rect_settings(self, new_settings):
        self.display_rect_settings = new_settings
