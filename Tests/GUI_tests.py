import unittest
from PyQt5.QtWidgets import QApplication
from ..GUI.main_window import MainWindow  

app = QApplication([])

class TestMainWindow(unittest.TestCase):
    def startWindow(self):
        self.window = MainWindow()
    def closeWindow(self):
        self.window.close()

if __name__ == "__main__":
    unittest.main()