import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QLabel, QWidget, QLineEdit
)


class LoginScreen(QWidget):
    def __init__(self, switch_to_task_selection):
        super().__init__()
        self.switch_to_task_selection = switch_to_task_selection
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_field = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.validate_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_field)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def validate_login(self):
        username = self.username_field.text()
        password = self.password_field.text()
        # Simplified validation for demonstration purposes
        if username == "user" and password == "password":
            self.switch_to_task_selection()
        else:
            error_label = QLabel("Invalid credentials. Please try again.")
            self.layout().addWidget(error_label)


class TaskSelectionScreen(QWidget):
    def __init__(self, switch_to_balancing, switch_to_loading):
        super().__init__()
        layout = QVBoxLayout()

        self.balancing_button = QPushButton("Balancing Task")
        self.balancing_button.clicked.connect(switch_to_balancing)

        self.loading_button = QPushButton("Loading/Unloading Task")
        self.loading_button.clicked.connect(switch_to_loading)

        layout.addWidget(self.balancing_button)
        layout.addWidget(self.loading_button)

        self.setLayout(layout)


class BalancingScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Balancing Screen"))
        # Additional components like grid of cargo containers can go here
        self.setLayout(layout)


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Loading/Unloading Screen"))
        # Additional components like grid of cargo containers can go here
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crane Optimization App")
        self.setGeometry(100, 100, 800, 600)

        # Central widget to manage screens
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize screens
        self.login_screen = LoginScreen(self.show_task_selection_screen)
        self.task_selection_screen = TaskSelectionScreen(
            self.show_balancing_screen, self.show_loading_screen
        )
        self.balancing_screen = BalancingScreen()
        self.loading_screen = LoadingScreen()

        # Add screens to stacked widget
        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.task_selection_screen)
        self.central_widget.addWidget(self.balancing_screen)
        self.central_widget.addWidget(self.loading_screen)

        # Show the login screen initially
        self.central_widget.setCurrentWidget(self.login_screen)

    def show_task_selection_screen(self):
        """Switch to the Task Selection screen."""
        self.central_widget.setCurrentWidget(self.task_selection_screen)

    def show_balancing_screen(self):
        """Switch to the Balancing screen."""
        self.central_widget.setCurrentWidget(self.balancing_screen)

    def show_loading_screen(self):
        """Switch to the Loading/Unloading screen."""
        self.central_widget.setCurrentWidget(self.loading_screen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
