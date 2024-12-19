import PySide6.QtWidgets as wid
import PySide6.QtCore as core

class ControleWidget(wid.QDockWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        # create
        self.contena = wid.QWidget()
        self.dial_A = wid.QDial()
        self.dial_B = wid.QDial()
        self.dial_C = wid.QDial()
        self.dial_D = wid.QDial()

        # layout
        self.layout_A = wid.QVBoxLayout()
        self.layout_A.addWidget(self.dial_A)
        self.layout_A.addWidget(self.dial_B)
        self.layout_A.addWidget(self.dial_C)
        self.layout_A.addWidget(self.dial_D)
        self.contena.setLayout(self.layout_A)
        self.setWidget(self.contena)
