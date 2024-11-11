import unittest
from PyQt5.QtWidgets import QApplication
from GUI.main_window import MainWindow


app = QApplication.instance()

#Testing class for Main Window Functionality
class TestMainWindow(unittest.TestCase):
    def setUp(self):
        """Set up the tests for Main Window"""
        self.window = MainWindow()


    def close(self):
        """Close the window after running all tests"""
        self.window.close()
        self.window = None



if __name__ == "__main__":
    unittest.main()
