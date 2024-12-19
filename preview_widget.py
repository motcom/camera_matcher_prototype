import PySide6.QtWidgets as wid
import PySide6.QtCore as core
import PySide6.QtGui as gui

class PreviewWidget(wid.QGraphicsView):
    def __init__(self,parent=None):
        super().__init__(parent)
        # create
        scene = wid.QGraphicsScene()
        self.image = wid.QGraphicsPixmapItem()
        self.image.setPixmap(gui.QPixmap("image.jpg"))
        scene.addItem(self.image)

        #layout
        self.setScene(scene)
