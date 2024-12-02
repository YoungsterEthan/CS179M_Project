import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget
)
from balancing_screen import *
from login_screen import * 
from manifest_view_screen import *
from task_selection_screen import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arkloaders App")
        self.setGeometry(100, 100, 800, 600)

        # Central widget to manage screens
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.manifest_data = []

        # Initialize screens
        self.login_screen = LoginScreen(self.show_task_selection_screen)
        self.task_selection_screen = TaskSelectionScreen(
            self,
            self.show_balancing_screen,
            self.show_loading_screen
        )
        self.manifest_viewer_screen = ManifestViewerScreen(self.manifest_data, self.show_task_selection_screen)

        # Balancing and Loading screens with a link to view the manifest
        self.balancing_screen = BalancingLoadingScreen(
            title="Balancing Screen",
            switch_to_home=self.show_task_selection_screen,
            grid_left_dims=(8, 24), 
            grid_right_dims=(10, 12), 
            show_manifest_viewer=self.show_manifest_viewer_screen 
        )
        self.loading_screen = BalancingLoadingScreen(
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

    def show_task_selection_screen(self):
        """Switch to the Task Selection screen."""
        self.central_widget.setCurrentWidget(self.task_selection_screen)

    def show_balancing_screen(self):
        """Switch to the Balancing screen."""
        self.populate_ship(self.balancing_screen)  
        self.central_widget.setCurrentWidget(self.balancing_screen)

    def show_loading_screen(self):
        """Switch to the Loading screen."""
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
        self.manifest_viewer_screen = ManifestViewerScreen(self.manifest_data, self.show_balancing_screen)
        self.central_widget.addWidget(self.manifest_viewer_screen)

    def populate_ship(self, screen):
        """
        Populate the right grid with manifest data:
        - NAN cells are colored black.
        - Non-UNUSED tasks display the container's content.
        """
        grid_rows, grid_cols = 10, 12  # Grid dimensions

        # screen.update_right_grid(, 1, "", "black")


        for line in self.manifest_data:
            try:
                # Parse the manifest line
                coordinates, container_id, content = line.split(", ")
                row, col = map(int, coordinates.strip("[]").split(","))
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
                        screen.update_right_grid(row, col, content, "white")

    

            except ValueError as e:
                print(f"Error processing line: {line}, Error: {e}")
                continue





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
