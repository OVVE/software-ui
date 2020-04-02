from typing import Tuple, Optional

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TextSetting:
    def __init__(self, fontName: str, fontSize: int, bold: bool):
        if bold:
            self.font = QFont(fontName, fontSize, QFont.Bold)

        else:
            self.font = QFont(fontName, fontSize)


#TODO: Abstract text placement
class FancyButtonSettings:
    def __init__(self,
                 labelSetting: TextSetting = TextSetting("Arial", 12, True),
                 valueSetting: TextSetting = TextSetting("Arial Black", 36, True),
                 unitSetting: TextSetting = TextSetting("Arial", 10, False),
                 fillColor: str ='#f2fff0',
                 borderColor: str = '#c5c5c5',
                 labelColor: str ='#A7A9AA',
                 valueColor: str = '#000000',
                 unitColor: str = '#808080',
                 default_size: Tuple[int, int] = (150, 80)):

        self.labelFont = labelSetting.font
        self.valueFont = valueSetting.font
        self.unitFont = unitSetting.font
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.labelColor = labelColor
        self.valueColor = valueColor
        self.unitColor = unitColor
        self.default_size = default_size

    def getFillBrush(self) -> QBrush:
        return QBrush(QColor(self.fillColor))

    def getBorderPen(self) -> QPen:
        return QPen(QColor(self.borderColor), 1, Qt.SolidLine)

    def getLabelPen(self) -> QPen:
        return QPen(QColor(self.labelColor))

    def getValuePen(self) -> QPen:
        return QPen(QColor(self.valueColor))

    def getUnitPen(self) -> QPen:
        return QPen(QColor(self.unitColor))

    def getLabelCoords(self, size=None) -> Tuple[int, int]:
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 1 / 5)

    def getValueCoords(
            self, size: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 3 / 5)

    def getUnitCoords(
            self, size: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 9 / 10)


class SimpleButtonSettings:
    def __init__(self,
                 valueSetting: TextSetting = TextSetting("Arial Black", 24, False),
                 fillColor: str = '#f2fff0',
                 borderColor: str = '#C5C5C5',
                 valueColor: str = '#000000',
                 default_size: Tuple[int, int] = (115, 65)):

        self.valueFont = valueSetting.font
        self.borderColor = borderColor
        self.fillColor = fillColor
        self.valueColor = valueColor
        self.default_size = default_size

    def getFillBrush(self) -> QBrush:
        return QBrush(QColor(self.fillColor))

    def getBorderPen(self) -> QPen:
        return QPen(QColor(self.borderColor), 1, Qt.SolidLine)

    def getValuePen(self) -> QPen:
        return QPen(QColor(self.valueColor))

    def getValueCoords(
            self, size: Optional[Tuple[int, int]] = None) ->Tuple[int, int]:
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 3 / 5)

class DisplayRectSettings:
    def __init__(self,
                 labelSetting: TextSetting = TextSetting("Arial", 24, True),
                 valueSetting: TextSetting = TextSetting("Arial Black", 52, True),
                 unitSetting: TextSetting = TextSetting("Arial", 18, False),
                 fillColor: str = '#ECFAFF',
                 borderColor: str = '#C5C5C5',
                 labelColor: str = '#29ABE2',
                 valueColor: str = '#000000',
                 unitColor: str = '#7394A0',
                 default_size: Tuple[int, int] = (150, 80)):
        self.labelFont = labelSetting.font
        self.valueFont = valueSetting.font
        self.unitFont = unitSetting.font
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.labelColor = labelColor
        self.valueColor = valueColor
        self.unitColor = unitColor
        self.default_size = default_size

    def getFillBrush(self) -> QBrush:
        return QBrush(QColor(self.fillColor))

    def getBorderPen(self) -> QPen:
        return QPen(QColor(self.borderColor), 1, Qt.SolidLine)

    def getLabelPen(self) -> QPen:
        return QPen(QColor(self.labelColor))

    def getValuePen(self) -> QPen:
        return QPen(QColor(self.valueColor))

    def getUnitPen(self) -> QPen:
        return QPen(QColor(self.unitColor))

    def getLabelCoords(
            self, size: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 1 / 5)

    def getValueCoords(
            self, size: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4), \
               int(use_size[1] * 3 / 5)

    def getUnitCoords(
            self, size: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        use_size = self.default_size if size is None else size
        return int(use_size[0] / 4),\
               int(use_size[1] * 9 / 10)


class UISettings:
    def __init__(self,
                 fancy_button_settings: FancyButtonSettings = FancyButtonSettings(),
                 simple_button_settings: SimpleButtonSettings = SimpleButtonSettings(),
                 display_rect_settings: DisplayRectSettings = DisplayRectSettings()):

        self.fancy_button_settings = fancy_button_settings
        self.simple_button_settings = simple_button_settings
        self.display_rect_settings = display_rect_settings

    def set_fancy_button_settings(
            self, new_settings: FancyButtonSettings) -> None:
        self.fancy_button_settings = new_settings

    def set_simple_button_settings(
            self, new_settings: SimpleButtonSettings) -> None:
        self.simple_button_settings = new_settings

    def set_display_rect_settings(
            self, new_settings: DisplayRectSettings) -> None:
        self.display_rect_settings = new_settings
