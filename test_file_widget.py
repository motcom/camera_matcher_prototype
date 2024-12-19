import PySide6.QtWidgets as wid
import file_widget as fw
import sys
from pytestqt import qtbot
import pytest


@pytest.fixture(scope="session")
def app_func():
    app = wid.QApplication([])
    return app

@pytest.fixture()
def file_widget_func(app_func):
    file_widget = fw.FileWidget()
    return file_widget

def test_set_load_path(file_widget_func: fw.FileWidget):
    file_widget = file_widget_func
    file_widget.set_load_path("C:\\Users\\motti\\Documents\\NoteBurner YouTube Video Downloader\\CvicCmMovie\\images")    
    assert len(file_widget.get_files_abs_path()) == 719
    assert file_widget.get_files_abs_path()[0] == "C:\\Users\\motti\\Documents\\NoteBurner YouTube Video Downloader\\CvicCmMovie\\images\\civic_00001.png"




