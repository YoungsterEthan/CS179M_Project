import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, QMessageBox, QFileDialog, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class LoginScreen(QWidget):
    def __init__(self, switch_to_task_selection):
        super().__init__()
        self.switch_to_task_selection = switch_to_task_selection

        # Set white background
        self.setStyleSheet("background-color: white;")

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the content vertically

        # Title at the top
        title = QLabel("Arkloaders")
        title.setFont(QFont("Arial", 24, QFont.Bold))  # Larger, bold font
        title.setAlignment(Qt.AlignCenter)  # Center the title
        title.setStyleSheet("color: #333;")  # Optional: Dark gray color

        # Username field
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont("Arial", 10))
        self.username_label.setStyleSheet("color: black;")
        self.username_field = QLineEdit()
        self.username_field.setStyleSheet("color: black;")
        self.username_field.setFixedSize(200, 30)  # Smaller text box
        self.username_field.setFont(QFont("Arial", 10))

        # Password field
        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Arial", 10))
        self.password_label.setStyleSheet("color: black;")
        self.password_field = QLineEdit()
        self.password_field.setFixedSize(200, 30)  # Smaller text box
        self.password_field.setStyleSheet("color: black;")
        self.password_field.setFont(QFont("Arial", 10))
        self.password_field.setEchoMode(QLineEdit.Password)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 10))
        self.login_button.setFixedSize(100, 30)  # Compact button size
        self.login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )
        self.login_button.clicked.connect(self.validate_login)

# Error message (hidden initially)
        self.error_label = QLabel("")
        self.error_label.setFont(QFont("Arial", 10))
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        # Add fields and button to the layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_field)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)  # Add the error label to the layout


        self.setLayout(layout)

    def validate_login(self):
        """Validate the entered credentials."""
        username = self.username_field.text()
        password = self.password_field.text()

        if username == "user" and password == "password":
            self.error_label.hide()  # Hide the error label on success
            self.switch_to_task_selection()
        else:
            # Update and show the error message
            self.error_label.setText("Invalid credentials. Please try again.")
            self.error_label.show()

            # Highlight the error message briefly
            self.flash_error_label()

    def flash_error_label(self):
        """Temporarily highlight the error label."""
        original_color = self.error_label.styleSheet()

        # Change the text color to a brighter red
        self.error_label.setStyleSheet("color: darkred;")

        # Restore the original style after 500ms
        QTimer.singleShot(500, lambda: self.error_label.setStyleSheet(original_color))


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt


class TaskSelectionScreen(QWidget):
    def __init__(self, switch_to_balancing, switch_to_loading):
        super().__init__()

        # Store transition methods
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
        self.balancing_button.setFixedSize(300, 100)
        self.balancing_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f0f0f0;  /* Light gray fill */
                border: 2px solid black;    /* Black border */
                border-radius: 10px;        /* Optional: Rounded corners */
                color: black;               /* Black text */
                font-size: 16px;            /* Larger font size */
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;  /* Slightly darker gray on hover */
            }
            """
        )
        self.balancing_button.clicked.connect(self.upload_balancing_file)

        # Loading Task Button
        self.loading_button = QPushButton("Loading/Unloading Task")
        self.loading_button.setFixedSize(300, 100)
        self.loading_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid black;
                border-radius: 10px;
                color: black;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            """
        )
        self.loading_button.clicked.connect(self.upload_loading_file)

        # Add buttons to the layout
        button_layout.addWidget(self.balancing_button)
        button_layout.addWidget(self.loading_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def upload_balancing_file(self):
        """Prompt the user to upload a file for the balancing task."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Balancing File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.process_file(file_path, "Balancing Task")

    def upload_loading_file(self):
        """Prompt the user to upload a file for the loading/unloading task."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Loading/Unloading File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.process_file(file_path, "Loading/Unloading Task")

    def process_file(self, file_path, task_name):
        """Validate and process the selected file, then switch to the appropriate screen."""
        try:
            # Validate file type or content
            with open(file_path, "r") as file:
                data = file.read()

            # Show success message
            self.show_message("File Uploaded", f"File uploaded for {task_name}: {file_path}")

            # Transition to the next screen based on the task
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

        # Apply stylesheet for black text
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
                background-color: #f0f0f0;  /* Light gray buttons */
                border: 1px solid black;
                color: black;
            }
            """
        )
        msg_box.exec_()

class GridWidget(QGridLayout):
    """Customizable grid for displaying containers."""
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols

        # Remove spacing between cells
        self.setSpacing(0)  # No space between the cells
        self.setContentsMargins(0, 0, 0, 0)  # Remove margins around the grid

        self.initialize_grid()

    def initialize_grid(self):
        """Create an empty grid with given dimensions."""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = QLabel("")
                cell.setStyleSheet(
                    "border: 1px solid black; background-color: white; font-size: 12px; text-align: center;"
                )
                cell.setAlignment(Qt.AlignCenter)
                self.addWidget(cell, row, col)

    def update_cell(self, row, col, text, color="white"):
        """Update a specific cell with text and background color."""
        cell = self.itemAtPosition(row, col).widget()
        if cell:
            cell.setText(text)
            cell.setStyleSheet(
                f"border: 1px solid black; background-color: {color}; font-size: 12px; text-align: center;"
            )


class BalancingScreen(QWidget):
    def __init__(self, title, switch_to_home, grid_left_dims, grid_right_dims):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Horizontal layout for grids
        grids_layout = QHBoxLayout()
        grids_layout.setSpacing(50)  # Separation between grids

        # Left grid
        left_grid_widget = QWidget()
        left_grid_layout = GridWidget(*grid_left_dims)
        left_grid_widget.setLayout(left_grid_layout)

        # Right grid
        right_grid_widget = QWidget()
        right_grid_layout = GridWidget(*grid_right_dims)
        right_grid_widget.setLayout(right_grid_layout)

        # Add grids to the layout with stretch factors
        grids_layout.addWidget(left_grid_widget, stretch=3)  # Left grid gets more space
        grids_layout.addWidget(right_grid_widget, stretch=1)  # Right grid gets less space
        layout.addLayout(grids_layout)

        # Bottom control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        # Next Move Button
        next_button = QPushButton("Next Move")
        next_button.setStyleSheet("font-size: 14px; padding: 8px;")
        controls_layout.addWidget(next_button)

        # Estimated Time Remaining
        time_label = QLabel("Estimated Time Remaining: N/A")
        time_label.setStyleSheet("font-size: 14px; color: black;")
        controls_layout.addWidget(time_label)

        # Manifest Button
        manifest_button = QPushButton("View Manifest")
        manifest_button.setStyleSheet("font-size: 14px; padding: 8px;")
        controls_layout.addWidget(manifest_button)

        # Back Button
        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet("font-size: 14px; padding: 8px;")
        back_button.clicked.connect(switch_to_home)
        controls_layout.addWidget(back_button)

        layout.addLayout(controls_layout)
        self.setLayout(layout)

        # Store the grid layouts for customization
        self.left_grid_layout = left_grid_layout
        self.right_grid_layout = right_grid_layout

    def update_left_grid(self, row, col, text, color="white"):
        """Update a cell in the left grid."""
        self.left_grid_layout.update_cell(row, col, text, color)

    def update_right_grid(self, row, col, text, color="white"):
        """Update a cell in the right grid."""
        self.right_grid_layout.update_cell(row, col, text, color)


class LoadingScreen(QWidget):
    def __init__(self, switch_to_task_selection):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Label for the Loading/Unloading Screen
        layout.addWidget(QLabel("Loading/Unloading Screen"))

        # Back Button
        back_button = QPushButton("Back to Task Selection")
        back_button.setFixedSize(200, 40)
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
        back_button.clicked.connect(switch_to_task_selection)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crane Optimization App")
        self.setGeometry(100, 100, 800, 600)

        # Central widget to manage screens
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Example manifest data
        self.manifest_data = [
            "[01,01], {00000}, NAN",
            "[01,02], {00000}, NAN",
            "[02,05], {02000}, Cat",
            "[03,05], {02007}, Dog",
            "[08,05], {03044}, Pig",
            # Add the rest of your manifest lines here
        ]

        # Initialize screens
        self.task_selection_screen = TaskSelectionScreen(self.show_balancing_screen, self.show_loading_screen)
        self.balancing_screen = BalancingScreen("Balancing Screen", self.show_task_selection_screen, (8, 24), (12, 8))
        self.loading_screen = BalancingScreen("Loading/Unloading Screen", self.show_task_selection_screen, (8, 24), (12, 8))
        self.manifest_viewer_screen = ManifestViewerScreen(self.manifest_data, self.show_balancing_screen)

        # Add screens to stacked widget
        self.central_widget.addWidget(self.task_selection_screen)
        self.central_widget.addWidget(self.balancing_screen)
        self.central_widget.addWidget(self.loading_screen)
        self.central_widget.addWidget(self.manifest_viewer_screen)

        # Show the task selection screen initially
        self.central_widget.setCurrentWidget(self.task_selection_screen)

    def show_balancing_screen(self):
        """Switch to the Balancing screen."""
        self.central_widget.setCurrentWidget(self.balancing_screen)

    def show_loading_screen(self):
        """Switch to the Loading screen."""
        self.central_widget.setCurrentWidget(self.loading_screen)

    def show_manifest_viewer_screen(self):
        """Switch to the Manifest Viewer screen."""
        self.central_widget.setCurrentWidget(self.manifest_viewer_screen)

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
        self.table.setColumnCount(3)  # Columns: Coordinates, Container ID, Content
        self.table.setHorizontalHeaderLabels(["Coordinates", "Container ID", "Content"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.setStyleSheet("font-size: 14px;")  # Font styling for the table

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
                # Skip any malformed lines
                continue

            # Add data to the table
            self.table.setItem(row, 0, QTableWidgetItem(coordinates))
            self.table.setItem(row, 1, QTableWidgetItem(container_id))
            self.table.setItem(row, 2, QTableWidgetItem(content))

        # Resize rows to fit contents
        self.table.resizeRowsToContents()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
