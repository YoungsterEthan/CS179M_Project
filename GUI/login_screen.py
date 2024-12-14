from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QLabel, QWidget, QLineEdit
)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter
from PyQt5.QtCore import Qt, QTimer

class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QLineEdit {
                color: #2F4F4F;
                background-color: #FFFFFF;
                border: 2px solid #4682B4;  /* Steel Blue */
                border-radius: 5px;
                padding: 5px;
            }
            """
        )

    def focusInEvent(self, event):
        """Change border color to Dodger Blue when focused."""
        self.setStyleSheet(
            """
            QLineEdit {
                color: #2F4F4F;
                background-color: #FFFFFF;
                border: 2px solid #1E90FF;  /* Dodger Blue */
                border-radius: 5px;
                padding: 5px;
            }
            """
        )
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Revert border color back to Steel Blue when focus is lost."""
        self.setStyleSheet(
            """
            QLineEdit {
                color: #2F4F4F;
                background-color: #FFFFFF;
                border: 2px solid #4682B4;  /* Steel Blue */
                border-radius: 5px;
                padding: 5px;
            }
            """
        )
        super().focusOutEvent(event)



class LoginScreen(QWidget):
    def __init__(self, next_screen):
        super().__init__()
        self.switch_screen = next_screen

        # Set background color
        self.setStyleSheet("background-color: #87CEEB;")  # Ocean-like light blue

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the content vertically

        # Placeholder for Ark image
        ark_image_label = QLabel()
        ark_pixmap = QPixmap("/Users/youngsterethan/Desktop/CS179M_Project/CS179M_Project-1/GUI/Ark.png")  # Replace with actual path to the PNG file
        ark_image_label.setPixmap(ark_pixmap)
        ark_image_label.setAlignment(Qt.AlignCenter)

        # Title at the top
        title = QLabel("Ark Loaders")
        title.setFont(QFont("Impact", 36, QFont.Bold))  # Strong, bold font
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                color: #2F4F4F;  /* Text color */
                padding: 10px;   /* Adds spacing for the outline */
                border: 3px solid #8B4513; /* SaddleBrown for a wooden effect */
                background-color: #F5DEB3; /* Optional: Light wood-like background */
                border-radius: 10px; /* Rounded edges for a smoother look */
            }
            """
        )


        # Username field
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont("Arial", 12))
        self.username_label.setStyleSheet("color: #2F4F4F;")  # Match title color
        self.username_field = CustomLineEdit()
        self.username_field.setFixedSize(250, 35)
        self.username_field.setFixedSize(250, 35)
        self.username_field.setFont(QFont("Arial", 10))

        # Password field
        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont("Arial", 12))
        self.password_label.setStyleSheet("color: #2F4F4F;")

        self.password_field = CustomLineEdit()
        self.password_field.setFixedSize(250, 35)

        self.password_field.setFont(QFont("Arial", 10))
        self.password_field.setEchoMode(QLineEdit.Password)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.login_button.setFixedSize(120, 40)
        self.login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4682B4;  /* Steel Blue */
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1E90FF;  /* Dodger Blue */
            }
            """
        )
        self.login_button.clicked.connect(self.validate_login)

        # Error message
        self.error_label = QLabel("")
        self.error_label.setFont(QFont("Arial", 12))
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        # Add widgets to the layout
        layout.addWidget(ark_image_label)
        layout.addWidget(title)
        layout.addSpacing(10)
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

        if username == "" and password == "":
            self.error_label.hide()
            self.switch_screen()
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
