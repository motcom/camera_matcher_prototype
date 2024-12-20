import sys
import PySide6.QtWidgets as wid
import root_widget

def main():
    app = wid.QApplication(sys.argv)
    w = root_widget.RootWidget() 
    w.show()
    app.exec()

if __name__ == "__main__":
    main()

