
from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QLabel, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt

class ManifestViewerScreen(QWidget):
    def __init__(self, manifest_data, switch_to_previous_screen):
        """
        Initialize the Manifest Viewer Screen.

        :param manifest_data: A list of strings representing the manifest lines.
        :param switch_to_previous_screen: Function to return to the previous screen.
        """
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title_label = QLabel("Manifest Viewer")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Table to display the manifest
        self.table = QTableWidget()
        self.table.setColumnCount(3) 
        self.table.setHorizontalHeaderLabels(["Coordinates", "Container ID", "Content"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.setStyleSheet("font-size: 14px;")  

        # Populate the table with manifest data
        self.populate_table(manifest_data)
        layout.addWidget(self.table)

        # Back Button
        back_button = QPushButton("Back")
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid black;
                border-radius: 10px;
                color: black;
                font-size: 14px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            """
        )
        back_button.clicked.connect(switch_to_previous_screen)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def populate_table(self, manifest_data):
        """
        Populate the table with the given manifest data.

        :param manifest_data: A list of strings representing the manifest lines.
        """
        self.table.setRowCount(len(manifest_data))

        for row, line in enumerate(manifest_data):
            # Split the manifest line into its components
            try:
                coordinates, container_id, content = line.split(", ")
                # Remove unnecessary characters
                coordinates = coordinates.strip("[]")
                container_id = container_id.strip("{}")
                content = content.strip()
            except ValueError:
                continue

            # Add data to the table
            self.table.setItem(row, 0, QTableWidgetItem(coordinates))
            self.table.setItem(row, 1, QTableWidgetItem(container_id))
            self.table.setItem(row, 2, QTableWidgetItem(content))

        # Resize rows to fit contents
        self.table.resizeRowsToContents()