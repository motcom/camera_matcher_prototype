import PySide6.QtWidgets as wid

class ControleWidget(wid.QDockWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        # create
        self.contena = wid.QWidget()
        self.checkBox_featurePoint = wid.QCheckBox("Feature Point")

        self.spacer = wid.QSpacerItem(20, 400, wid.QSizePolicy.Expanding, wid.QSizePolicy.Expanding)

        # layout
        self.layoutMaster = wid.QVBoxLayout()
        self.layoutMaster.addWidget(self.checkBox_featurePoint)
        self.layoutMaster.addItem(self.spacer)
        self.contena.setLayout(self.layoutMaster)

        self.setWidget(self.contena)
