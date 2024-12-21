import PySide6.QtWidgets as wid
import slide_widget as sw

app = wid.QApplication([])
slide_widget = sw.SlideWidget()
slide_widget.show()
app.exec_()

    

