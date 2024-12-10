import sys
sys.path.insert(0, '/Users/youngsterethan/Desktop/CS179M_Project/CS179M_Project-1/Load_Balance')
sys.path.insert(0, '/Users/youngsterethan/Desktop/CS179M_Project/CS179M_Project-1/')
from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ContainerData import ContainerData
from Manifest import Manifest
from Loader import Loader
from Balancer import Balancer
import os
from load_unload_selction_screen import *

class TaskSelectionScreen(QWidget):
    def __init__(self, main_window, switch_to_balancing, switch_to_loading):
        super().__init__()
        self.main_window = main_window  
        self.switch_to_balancing = switch_to_balancing
        self.switch_to_loading = switch_to_loading

        # Set white background
        self.setStyleSheet("background-color: white;")

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # Balancing Task Button
        self.balancing_button = QPushButton("Balancing Task")
        self.balancing_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.balancing_button.setFixedSize(300, 100)
        self.balancing_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4682B4;  /* Steel Blue */
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1E90FF;  /* Dodger Blue */
            }
            """
        )
        self.balancing_button.clicked.connect(lambda: self.upload_file("Balancing Task"))

        # Loading Task Button
        self.loading_button = QPushButton("Loading/Unloading Task")
        self.loading_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.loading_button.setFixedSize(300, 100)
        self.loading_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4682B4;  /* Steel Blue */
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1E90FF;  /* Dodger Blue */
            }
            """
        )
        self.loading_button.clicked.connect(lambda: self.upload_file("Loading/Unloading Task"))


        # Add buttons to the layout
        button_layout.addWidget(self.balancing_button)
        button_layout.addWidget(self.loading_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def upload_file(self, task_name):
        """Prompt the user to upload a file for the selected task."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, f"Open {task_name} File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.process_file(file_path, task_name)

    def process_file(self, file_path, task_name):
        """Validate and process the selected file, then switch to the appropriate screen."""
        try:
            # Validate file type or content
            with open(file_path, "r") as file:
                data = file.readlines()

            # Remove the .txt extension from path
            file = os.path.splitext(file_path)[0]

            manifest = Manifest('', file)
            manifest.read_manifest()

            def handle_selection(offload, load):
                # print("in selection")
                loader = Loader(manifest)
                moves = loader.load_unload(load, offload)
                self.main_window.set_moves(moves)


            self.main_window.set_manifest_data(data)

            if task_name == "Loading/Unloading Task":
                selection_screen = LoadUnloadSelectionScreen(manifest, handle_selection)
                selection_screen.exec_()
            else:
                balancer = Balancer(manifest)
                moves = balancer.balance()
                self.main_window.set_moves(moves)
            

            # Transition to the appropriate screen
            if task_name == "Balancing Task":
                self.switch_to_balancing()
            elif task_name == "Loading/Unloading Task":
                self.switch_to_loading()

        except Exception as e:
            # Show error message
            self.show_message("Error", f"Failed to process file: {e}", error=True)

    def show_message(self, title, message, error=False):
        """Show a custom message box with black text."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        # Set the message box icon
        if error:
            msg_box.setIcon(QMessageBox.Critical)
        else:
            msg_box.setIcon(QMessageBox.Information)


        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
                color: black;  /* Black text color */
            }
            QMessageBox QLabel {
                color: black;  /* Ensures text in QLabel remains black */
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                border: 1px solid black;
                color: black;
            }
            """
        )
        msg_box.exec_()


