import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('title')

        self.resize(320, 240)
        self.show()

    def keyPressEvent(self, e):
        def isPrintable(key):
            printable = [
                Qt.Key_Enter
            ]

            if key in printable:
                return True
            else:
                return False

        control = False

        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            print('enter')
        
        if not control and isPrintable(e.key()):
            print(e.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())