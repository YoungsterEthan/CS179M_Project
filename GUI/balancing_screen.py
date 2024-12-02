from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen

class GridWidget(QGridLayout):
    """Customizable grid for displaying containers."""
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols

        # Remove spacing between cells
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)  

        self.initialize_grid()

    def initialize_grid(self):
        """Create an empty grid with given dimensions."""
        cell_width = 40  # Set the fixed width of each cell
        cell_height = 40  # Set the fixed height of each cell

        for row in range(self.rows):
            for col in range(self.cols):
                cell = QLabel("")
                cell.setFixedSize(cell_width, cell_height)
                cell.setStyleSheet(
                    "border: 1px solid black; background-color: white; font-size: 12px; text-align: center;"
                )
                cell.setAlignment(Qt.AlignCenter)
                self.addWidget(cell, row, col)

    def update_cell(self, row, col, text, color="white"):
        """Update a specific cell with text and background color."""
        text_color = ""
        if color == "white":
            text_color = "black"
        else:
            text_color = "white"

        cell = self.itemAtPosition(row, col)
        if cell is not None:
            widget = cell.widget()
            if widget:
                widget.setText(text)
                widget.setStyleSheet(
                    f"border: 1px solid black; background-color: {color}; color: {text_color}; font-size: 12px; text-align: center;"
                )


class TruckWidget(QWidget):
    """Custom widget to represent the truck as a yellow circle."""
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 100)  # Set size for the truck area

    def paintEvent(self, event):
        """Paint a yellow circle representing the truck."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a yellow circle
        brush = QBrush(Qt.yellow, Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QPen(Qt.black, 2)  
        painter.setPen(pen)

        # Circle position and size (place holder for truck)
        radius = min(self.width(), self.height()) // 2
        center_x, center_y = self.width() // 2, self.height() // 2
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)


class BalancingLoadingScreen(QWidget):
    def __init__(self, title, switch_to_home, grid_left_dims, grid_right_dims, show_manifest_viewer):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        #dims
        self.left_grid_dims = grid_left_dims
        self.right_grid_dims = grid_right_dims

        # Horizontal layout for truck and grids
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)  # Space between truck and grids

        # Truck 
        truck_widget = TruckWidget()
        truck_layout = QVBoxLayout()
        truck_layout.addWidget(truck_widget)
        truck_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(truck_layout)

        # Grids layout
        grids_layout = QHBoxLayout()
        grids_layout.setSpacing(50)

        # Left grid
        left_grid_widget = QWidget()
        left_grid_layout = GridWidget(*grid_left_dims)
        left_grid_widget.setLayout(left_grid_layout)

        # Right grid
        right_grid_widget = QWidget()
        right_grid_layout = GridWidget(*grid_right_dims)
        right_grid_widget.setLayout(right_grid_layout)

        # Add grids to the layout
        grids_layout.addWidget(left_grid_widget, stretch=3)
        grids_layout.addWidget(right_grid_widget, stretch=1)

        # Add truck and grids to the main layout
        main_layout.addLayout(grids_layout)
        layout.addLayout(main_layout)

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
        manifest_button.clicked.connect(show_manifest_viewer)
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
        n_row, n_col = self.right_grid_dims
        r = n_row - row
        c = col - 1
        self.right_grid_layout.update_cell(r, c, text, color)


