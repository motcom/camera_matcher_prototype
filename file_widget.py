import PySide6.QtWidgets as wid
import os

class FileWidget(wid.QDockWidget):
    def get_files_abs_path(self) -> list[str]:
        self.files_abs_path = []
        file_names = os.listdir(self.load_path)
        for file_name in file_names:
            self.files_abs_path.append(os.path.join(self.load_path, file_name))
        return self.files_abs_path

    def set_load_path(self, path):
        self.load_path = path
        self.line_load_path.setText(self.load_path)

    def on_load_btn(self):
        tmp_load_path = wid.QFileDialog.getExistingDirectory(self, "Select Directory", ".")
        self.set_load_path(tmp_load_path)

    def set_save_path(self, path):
        self.save_path = path
        self.line_save_path.setText(self.save_path)

    def on_save_btn(self):
        tmp_save_path = wid.QFileDialog.getExistingDirectory(self, "Select Directory", ".")
        self.set_save_path(tmp_save_path)

    def init_data_structure(self):
        self.load_path = ""
        self.save_path = ""
        self.files_abs_path = []

    def __init__(self,parent=None):
        super().__init__(parent)
        # create
        self.contena_wid = wid.QWidget()

        self.label_load_path = wid.QLabel("load path")
        self.line_load_path  = wid.QLineEdit()
        self.btn_load_path   = wid.QPushButton("load")

        self.label_save_path = wid.QLabel("save path")
        self.line_save_path  = wid.QLineEdit()
        self.btn_save_path   = wid.QPushButton("save")

        # event
        self.btn_load_path.clicked.connect(self.on_load_btn)
        self.btn_save_path.clicked.connect(self.on_save_btn)

        # layout
        self.layout_A = wid.QHBoxLayout()
        self.layout_A.addWidget(self.label_load_path)
        self.layout_A.addWidget(self.line_load_path)
        self.layout_A.addWidget(self.btn_load_path)

        self.layout_B = wid.QHBoxLayout()
            
        self.layout_B.addWidget(self.label_save_path)
        self.layout_B.addWidget(self.line_save_path)
        self.layout_B.addWidget(self.btn_save_path)

        self.layout_C = wid.QVBoxLayout()
        self.layout_C.addLayout(self.layout_A)
        self.layout_C.addLayout(self.layout_B)
        self.contena_wid.setLayout(self.layout_C)
        self.setWidget(self.contena_wid)

        # data strcutre init
        self.init_data_structure()

