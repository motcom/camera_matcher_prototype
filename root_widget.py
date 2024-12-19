import PySide6.QtWidgets as wid
import PySide6.QtCore as core
import PySide6.QtGui as gui
import preview_widget as pw
import control_widget as cw
import file_widget as fw
import cv2


class RootWidget(wid.QMainWindow):
    def update_images(self):
        self.img_lst.clear()
        img_filePath_lst = self.file_windows.get_files_abs_path()
        for img_filePath in img_filePath_lst:
            self.img_lst.append(cv2.imread(img_filePath))

    def data_init(self):
        self.img_lst = []

    def __init__(self):
        super().__init__()

        # propety
        self.setWindowTitle("Root Directory")

        # crate
        self.preview_window = pw.PreviewWidget()
        self.controle_window = cw.ControleWidget()
        self.file_windows = fw.FileWidget()

        # layout
        self.setCentralWidget(self.preview_window)
        self.addDockWidget(core.Qt.DockWidgetArea.RightDockWidgetArea, self.controle_window)
        self.addDockWidget(core.Qt.DockWidgetArea.BottomDockWidgetArea, self.file_windows)

        # data init
        self.data_init







