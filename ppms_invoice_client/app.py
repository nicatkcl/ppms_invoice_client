from PyQt5.QtWidgets import QApplication

from .ui.main import Window


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit( app.exec_() )