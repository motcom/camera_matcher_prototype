import PySide6.QtWidgets as wid
import PySide6.QtGui as gui
import PySide6.QtCore as core
from typing import Optional
import numpy as np


class PreviewWidget(wid.QWidget):
    signal_tarcker_update = core.Signal(core.QRectF)


    def __init__(self,parent=None):
        super().__init__(parent)
        self.img = gui.QPixmap()
        self.start_point = None
        self.end_point = None
        self.rect:Optional[core.QRect] = None  # QRectを保持


    def paintEvent(self, event: gui.QPaintEvent) -> None:
        painter = gui.QPainter(self)
        painter.drawPixmap(0,0,self.img)

    # Rectangleの描画
        if self.start_point and self.end_point:
            pen = gui.QPen(core.Qt.red, 2, core.Qt.SolidLine)
            painter.setPen(pen)
            rect = core.QRectF(self.start_point, self.end_point)
            painter.drawRect(rect)


    def slot_update_image(self,img:gui.QPixmap):
        self.img = img
        self.update()
        

    # マウスイベント ----------------------------------------------
    def mousePressEvent(self, event): # start point の設定
        if event.button() == core.Qt.LeftButton:
            self.start_point = event.position()

    def mouseMoveEvent(self, event): # drag中の処理
        if self.start_point:
            self.end_point = event.position()
            self.update()

    def mouseReleaseEvent(self, event): # release時の処理
        if event.button() == core.Qt.LeftButton:
            self.end_point = event.position()

            # QrectFの設定
            tmp_rect = core.QRectF(self.start_point, self.end_point)

            self.start_point = None
            self.end_point = None

            self.signal_tarcker_update.emit(tmp_rect)


