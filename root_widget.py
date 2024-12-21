import PySide6.QtWidgets as wid
import PySide6.QtCore as core
import preview_widget as pw
import control_widget as cw
import file_widget as fw
import slide_widget as sw
import cv2


class RootWidget(wid.QMainWindow):
    def slot_load_image_list(self,files_abs_path:list):
        print("ok_slot")
        print(files_abs_path)
        FILE_EXTENTION = [".jpg",".png"]

        self.img_lst.clear()
        for filePath in files_abs_path:
            if FILE_EXTENTION[0] in filePath or FILE_EXTENTION[1] in filePath:  
                self.img_lst.append(cv2.imread(filePath))

    def data_init(self):
        self.img_lst = []

    def __init__(self):
        super().__init__()

        # propety
        self.setWindowTitle("Movie Player")

        # crate
        self.preview_window = pw.PreviewWidget()
        self.controle_window = cw.ControleWidget()
        self.file_windows = fw.FileWidget()

        # event
        self.file_windows.emmit_signal_getfiles_abs_path.connect(self.slot_load_image_list) 

        # layout
        self.setCentralWidget(self.preview_window)
        self.addDockWidget(core.Qt.DockWidgetArea.RightDockWidgetArea, self.controle_window)
        self.addDockWidget(core.Qt.DockWidgetArea.BottomDockWidgetArea, sw.SlideWidget())
        self.addDockWidget(core.Qt.DockWidgetArea.BottomDockWidgetArea, self.file_windows)

        # data init
        self.data_init()







