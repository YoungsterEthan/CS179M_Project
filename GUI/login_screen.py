import sys
from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QLabel, QWidget, QLineEdit
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
        title.setFont(QFont("Arial", 24, QFont.Bold))  
        title.setAlignment(Qt.AlignCenter)  
        title.setStyleSheet("color: #333;")  

        # Username field
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont("Arial", 10))
        self.username_label.setStyleSheet("color: black;")
        self.username_field = QLineEdit()
        self.username_field.setStyleSheet("color: black;")
        self.username_field.setFixedSize(200, 30)  
        self.username_field.setFont(QFont("Arial", 10))

        # Password field
        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Arial", 10))
        self.password_label.setStyleSheet("color: black;")
        self.password_field = QLineEdit()
        self.password_field.setFixedSize(200, 30) 
        self.password_field.setStyleSheet("color: black;")
        self.password_field.setFont(QFont("Arial", 10))
        self.password_field.setEchoMode(QLineEdit.Password)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 10))
        self.login_button.setFixedSize(100, 30)  
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

        # Error message 
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
        layout.addWidget(self.error_label)  


        self.setLayout(layout)

    def validate_login(self):
        """Validate the entered credentials."""
        username = self.username_field.text()
        password = self.password_field.text()

        if username == "user" and password == "password":
            self.error_label.hide()  
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


        self.error_label.setStyleSheet("color: darkred;")


        QTimer.singleShot(500, lambda: self.error_label.setStyleSheet(original_color))
