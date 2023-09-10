from PyQt6.QtGui import QPainter, QPen, QFont, QMouseEvent
from PyQt6.QtWidgets import QAbstractButton, QSlider, QWidget, QVBoxLayout, QHBoxLayout, \
    QStyleOptionSlider, QStyle
from PyQt6.QtCore import Qt, QRect, QPoint
import numpy as np


class QCustomSlider(QWidget):
    def __init__(self, minimum, maximum, interval=1, orientation=Qt.Orientation.Horizontal,
                 labels=None, p0=0, parent=None, suppress_mouse_move=False):
        super().__init__(parent=parent)

        levels = range(minimum, maximum + interval, interval)

        if labels is not None:
            if not isinstance(labels, (tuple, list)):
                raise Exception("<labels> is a list or tuple.")
            if len(labels) != len(levels):
                raise Exception("Size of <labels> doesn't match levels.")
            self.levels = list(zip(levels, labels))
        else:
            self.levels = list(zip(levels, map(str, levels)))

        if orientation == Qt.Orientation.Horizontal:
            self.layout = QVBoxLayout(self)
        elif orientation == Qt.Orientation.Vertical:
            self.layout = QHBoxLayout(self)
        else:
            raise Exception("<orientation> wrong.")

        # gives some space to print labels
        self.left_margin = 10
        self.top_margin = 10
        self.right_margin = 10
        self.bottom_margin = 10

        self.suppress_mouse_move = suppress_mouse_move

        self.layout.setContentsMargins(self.left_margin, self.top_margin,
                                       self.right_margin, self.bottom_margin)

        self.sl = QSlider(orientation, self)
        self.sl.setMinimum(minimum)
        self.sl.setMaximum(maximum)
        self.sl.setValue(minimum)
        self.sl.setSliderPosition(p0)
        if orientation == Qt.Orientation.Horizontal:
            self.sl.setTickPosition(QSlider.TickPosition.TicksBelow)
            self.sl.setMinimumWidth(300)  # just to make it easier to read
        else:
            self.sl.setTickPosition(QSlider.TickPosition.TicksLeft)
            self.sl.setMinimumHeight(300)  # just to make it easier to read
        self.sl.setTickInterval(interval)
        self.sl.setSingleStep(1)
        self.sl.setPageStep(1)

        self.layout.addWidget(self.sl)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Suppress the mouseMoveEvent to disable dragging."""
        if self.suppress_mouse_move:
            return
        super().mouseMoveEvent(event)  # Call the base class implementation for normal behavior

    def paintEvent(self, e):
        super().paintEvent(e)

        style = self.sl.style()
        painter = QPainter(self)
        st_slider = QStyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation = self.sl.orientation()

        length = style.pixelMetric(QStyle.PixelMetric.PM_SliderLength, st_slider, self.sl)
        available = style.pixelMetric(QStyle.PixelMetric.PM_SliderSpaceAvailable, st_slider, self.sl)

        for v, v_str in self.levels:

            # get the size of the label
            rect = painter.drawText(QRect(), Qt.TextFlag.TextDontPrint, v_str)

            if self.sl.orientation() == Qt.Orientation.Horizontal:
                # I assume the offset is half the length of slider, therefore
                # + length//2
                x_loc = QStyle.sliderPositionFromValue(self.sl.minimum(),
                                                       self.sl.maximum(), v, available) + length // 2

                # left bound of the text = center - half of text width + L_margin
                left = x_loc - rect.width() // 2 + self.left_margin
                bottom = self.rect().bottom()

                # enlarge margins if clipping
                if v == self.sl.minimum():
                    if left <= 0:
                        self.left_margin = rect.width() // 2 - x_loc
                    if self.bottom_margin <= rect.height():
                        self.bottom_margin = rect.height()

                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

                if v == self.sl.maximum() and rect.width() // 2 >= self.right_margin:
                    self.right_margin = rect.width() // 2
                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

            else:
                y_loc = QStyle.sliderPositionFromValue(self.sl.minimum(),
                                                       self.sl.maximum(), v, available, upsideDown=True)

                bottom = y_loc + length // 2 + rect.height() // 2 + self.top_margin - 3
                # there is a 3 px offset that I can't attribute to any metric

                left = self.left_margin - rect.width()
                if left <= 0:
                    self.left_margin = rect.width() + 2
                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

            pos = QPoint(left, bottom)
            painter.drawText(pos, v_str)

        return
