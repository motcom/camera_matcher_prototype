
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPainter, QPen, QMouseEvent
from PySide6.QtCore import QRect, QPoint, Qt
import cv2
import sys

class RectangleDrawer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("トラッキング領域を選択")
        self.setGeometry(100, 100, 640, 480)
        self.start_point = None
        self.end_point = None
        self.rect = None  # QRectを保持

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = event.pos()
            self.rect = QRect(self.start_point, self.end_point)
            print(f"selected region: {self.rect}")  # QRectの座標を確認
            self.start_point = None
            self.end_point = None
            self.rect = None
            self.update()


    def paintEvent(self, event):
        if self.start_point and self.end_point:
            painter = QPainter(self)
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start_point, self.end_point)
            painter.drawRect(rect)


if __name__ == "__main__":
    app = QApplication([])

    # PySideウィンドウを開き、矩形領域を選択
    drawer = RectangleDrawer()
    drawer.show()
    app.exec()

    # QRectからOpenCVのbbox形式 (x, y, w, h) を取得
    # if drawer.rect:
    #     rect = drawer.rect
    #     x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
    #     bbox = (x, y, w, h)
    #     print("tracking region(bbox):", bbox)
