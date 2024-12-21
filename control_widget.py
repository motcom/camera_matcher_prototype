import PySide6.QtWidgets as wid

class ControleWidget(wid.QDockWidget):
    def get_values(self):
        return (self.valA,self.valB,self.valC,self.valD)

    def on_dial_val_change(self):
        NORMALIZE_VAL = 100
        self.valA = self.dial_A.value() / NORMALIZE_VAL
        self.valB = self.dial_B.value() / NORMALIZE_VAL
        self.valC = self.dial_C.value() / NORMALIZE_VAL
        self.valD = self.dial_D.value() / NORMALIZE_VAL

    def __init__(self,parent=None):
        super().__init__(parent)

        # create
        self.contena = wid.QWidget()
        self.dial_A = wid.QDial()
        self.dial_B = wid.QDial()
        self.dial_C = wid.QDial()
        self.dial_D = wid.QDial()

        # propety
        self.dial_A.setRange(0,100)
        self.dial_B.setRange(0,100)
        self.dial_C.setRange(0,100)
        self.dial_D.setRange(0,100)

        # event 
        self.dial_A.valueChanged.connect(self.on_dial_val_change)
        self.dial_B.valueChanged.connect(self.on_dial_val_change)
        self.dial_C.valueChanged.connect(self.on_dial_val_change)
        self.dial_D.valueChanged.connect(self.on_dial_val_change)

        # layout
        self.layout_A = wid.QVBoxLayout()
        self.layout_A.addWidget(self.dial_A)
        self.layout_A.addWidget(self.dial_B)
        self.layout_A.addWidget(self.dial_C)
        self.layout_A.addWidget(self.dial_D)
        self.contena.setLayout(self.layout_A)
        self.setWidget(self.contena)
