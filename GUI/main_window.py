import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QRect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
