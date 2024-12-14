import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget
)
from GUI.balancing_screen import *
from GUI.login_screen import * 
from GUI.manifest_view_screen import *
from GUI.task_selection_screen import *

import os
from RecoveryLogger import RecoveryLogger
from Logger import Logger
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arkloaders App")
        self.setGeometry(100, 100, 800, 1000)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #87CEEB;")  # Ocean blue background

        # Central widget to manage screens
        self.central_widget = QStackedWidget()
        self.central_widget.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.setCentralWidget(self.central_widget)

        self.manifest_data = []
        self.current_move_index = 0  # Track the current move
        self.moves = []  # Store moves

        self.opened = False

        # Initialize the RecoveryLogger
        self.recovery_logger = RecoveryLogger(recovery_path="")  
        self.current_task = 0

        #initialize Logger
        self.logger = Logger()

        # Initialize screens
        
        self.login_screen = LoginScreen(self.show_task_selection_screen, self)
        self.task_selection_screen = TaskSelectionScreen(
            self,
            self.show_balancing_screen,
            self.show_loading_screen
        )
        self.manifest_viewer_screen = ManifestViewerScreen(self.manifest_data, self.show_task_selection_screen)

        # Balancing and Loading screens with a link to view the manifest
        self.balancing_screen = BalancingLoadingScreen(self,
            title="Balancing Screen",
            switch_to_home=self.show_task_selection_screen,
            grid_left_dims=(8, 24), 
            grid_right_dims=(10, 12), 
            show_manifest_viewer=self.show_manifest_viewer_screen 
        )
        self.loading_screen = BalancingLoadingScreen(self,
            title="Loading/Unloading Screen",
            switch_to_home=self.show_task_selection_screen,
            grid_left_dims=(8, 24),
            grid_right_dims=(10, 12), 
            show_manifest_viewer=self.show_manifest_viewer_screen  
        )

        # Add screens to stacked widget
        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.task_selection_screen)
        self.central_widget.addWidget(self.balancing_screen)
        self.central_widget.addWidget(self.loading_screen)
        self.central_widget.addWidget(self.manifest_viewer_screen)

        # Show the login screen initially
        self.central_widget.setCurrentWidget(self.login_screen)

        if self.recovery_logger.fexists():
            with open('last_opened.txt', "r") as file:
                data = file.readlines()
                self.set_manifest_data(data)

            self.show_message(
                    "Recovery",
                    "A previous session was found. Moves have been recovered.",
                    error=False,
                )
            self.recover_moves()

            if(self.recovery_logger.last_task == "Balancing\n"):
                print("WE BALAnCING")
                self.show_balancing_screen()
                for i in range(self.current_move_index):
                    self.balancing_screen.next_move()
            if(self.recovery_logger.last_task == "Loading/Unloading Task\n"):
                print("WE loadin")
                self.show_loading_screen()
                for i in range(self.current_move_index):
                    self.loading_screen.next_move()

    def show_login_screen(self):
        self.login_screen.switch_screen = self.current_task
        self.central_widget.setCurrentWidget(self.login_screen)


    def show_task_selection_screen(self):
        """Switch to the Task Selection screen."""
        self.central_widget.setCurrentWidget(self.task_selection_screen)

    def show_balancing_screen(self):
        """Switch to the Balancing screen."""
        print('self.current_move_index:', self.current_move_index)
        self.current_task = self.show_balancing_screen

        if self.opened == False:
            self.opened = True
            self.populate_ship(self.balancing_screen)  
        self.central_widget.setCurrentWidget(self.balancing_screen)

    def show_loading_screen(self):
        self.current_task = self.show_loading_screen
        """Switch to the Loading screen."""
        if self.opened == False:
            self.opened = True
            self.populate_ship(self.loading_screen)  
        self.central_widget.setCurrentWidget(self.loading_screen)

    def show_manifest_viewer_screen(self):
        """Switch to the Manifest Viewer screen."""
        self.update_manifest_viewer_screen()
        self.central_widget.setCurrentWidget(self.manifest_viewer_screen)

    def set_manifest_data(self, data):
        """Set the manifest data to be displayed."""
        self.manifest_data = data

    def update_manifest_viewer_screen(self):
        """Update the Manifest Viewer Screen with the latest manifest data."""
        self.central_widget.removeWidget(self.manifest_viewer_screen)
        self.manifest_viewer_screen = ManifestViewerScreen(self.manifest_data, self.current_task)
        self.central_widget.addWidget(self.manifest_viewer_screen)

    def populate_ship(self, screen):
        """
        Populate the right grid with manifest data:
        - NAN cells are colored black.
        - Non-UNUSED tasks display the container's content.
        """
        grid_rows, grid_cols = 10, 12  # Grid dimensions

        for line in self.manifest_data:
            try:
                # Parse the manifest line
                coordinates, weight, content = line.split(", ")
                row, col = map(int, coordinates.strip("[]").split(","))
                metadata = {"Name": content, "Weight": weight}
                # print(f"Original coordinates: row={row}, col={col}")

                # Subtract 1 for zero-based indexing
                grid_row = grid_rows - row  # Flip row (top-down to bottom-up)
                grid_col = col - 1          # Convert 1-based to 0-based index
                # print(f"Mapped to grid: grid_row={grid_row}, grid_col={grid_col}")

                # Validate grid indices to avoid out-of-bounds errors
                if 0 <= grid_row < grid_rows and 0 <= grid_col < grid_cols:
                    if content.strip() == "NAN":
                        # print(f'(row,ccol): ({row}, {col})')
                        screen.update_right_grid(row, col, "", "black")
                    elif content.strip() == "UNUSED":
                        screen.update_right_grid(row, col, "", "white")
                    else:
                        screen.update_right_grid(row, col, content, "white", metadata)
                        
    

            except ValueError as e:
                print(f"Error processing line: {line}, Error: {e}")
                continue


    def set_moves(self, moves, task):
        """Set the moves to be displayed on the balancing screen."""
        self.moves = moves

        print("TASKSASR:", task)

        if(task == "Balancing\n"):
            print('test1')
            self.balancing_screen.set_moves(moves)
        else:
            print('test2')
            self.loading_screen.set_moves(moves)

        # Create a recovery file using RecoveryLogger
        if not self.recovery_logger.fexists():
            self.recovery_logger.last_task = task
            self.recovery_logger.create(moves)

    def save_move_progress(self):
        """Save the current move progress to the recovery file."""
        self.recovery_logger.save_next_move()

    def recover_moves(self):
        """Recover moves from the recovery file."""
        moves, last_completed = self.recovery_logger.recover()
        print("moves: ", moves)
        print("last completed:", last_completed)
        print(f'LAST TASK: {self.recovery_logger.last_task}')
        if moves:
            print("runi")
            self.set_moves(moves, self.recovery_logger.last_task)
            self.current_move_index = last_completed  # Restore last completed move index
            # print("index:", self.current_move_index)
            # self.balancing_screen.current_move_index = last_completed  # Sync with BalancingLoadingScreen

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



    def delete_last(self):
        """Delete a file if it exists."""
        file_path ='last_opened.txt'
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"File '{file_path}' has been deleted.")
            except Exception as e:
                print(f"Error deleting file '{file_path}': {e}")
        else:
            print(f"File '{file_path}' does not exist.")

