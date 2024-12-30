import PySide6.QtCore as core
import cv2

class FileListLoader(core.QThread):
    signal_send_files = core.Signal(list)
    signal_send_progress = core.Signal(int) 

    def __init__(self,files_abs_path):
        super().__init__()
        self.files_abs_path = files_abs_path

    def run(self):
        FILE_EXTENTION = [".jpg",".png"]
        img_lst = []
        index = 0
        for filePath in self.files_abs_path:
            if FILE_EXTENTION[0] in filePath or FILE_EXTENTION[1] in filePath:  
                img_lst.append(cv2.imread(filePath))
                self.signal_send_progress.emit(index)
                index += 1

        self.signal_send_files.emit(img_lst)
