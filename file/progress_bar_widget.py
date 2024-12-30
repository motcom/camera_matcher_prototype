import PySide6.QtWidgets as wid
import PySide6.QtCore as core

class ProgressBarWidget(wid.QWidget):
    signal_end = core.Signal()
    def __init__(self, min_val = 0,max_val=100,parent=None):
        super(ProgressBarWidget, self).__init__(parent)

        # propety
        self.min_val = min_val
        self.max_val = max_val

        # create progress bar
        self.progress_bar = wid.QProgressBar()
        self.progress_bar.setRange(self.min_val, self.max_val)
        self.progress_bar.setValue(0)

        # layout
        self.layoutA = wid.QVBoxLayout()
        self.layoutA.addWidget(self.progress_bar)
        self.setLayout(self.layoutA)


    def slot_set_value(self,value:int):
        self.progress_bar.setValue(value)
        if self.max_val <= value:
            self.signal_end.emit()
