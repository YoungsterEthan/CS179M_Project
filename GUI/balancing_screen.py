from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor

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


class TruckWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(50, 50)  # Set the size of the truck
        self.container_name = ""  # Stores the name of the container in the truck

    def paintEvent(self, event):
        """Draw the truck as a yellow circle and display container name if present."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("yellow")))
        painter.drawEllipse(0, 0, self.width(), self.height())

        # Draw the container name in the center of the circle
        if self.container_name:
            painter.setPen(Qt.black)
            painter.drawText(self.rect(), Qt.AlignCenter, self.container_name)

    def update_container(self, container_name):
        """Update the truck to display the container name."""
        self.container_name = container_name
        self.update()  # Trigger a repaint to display the container

    def clear_container(self):
        """Clear the truck (remove the container name)."""
        self.container_name = ""
        self.update()  # Trigger a repaint to clear the container


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

        # dims
        self.left_grid_dims = grid_left_dims
        self.right_grid_dims = grid_right_dims

        self.moves = []

        # Horizontal layout for grids, crane, and truck
        main_layout = QHBoxLayout()
        main_layout.setSpacing(50)  # Space between sections

        # Left grid
        left_grid_widget = QWidget()
        left_grid_layout = GridWidget(*grid_left_dims)
        left_grid_widget.setLayout(left_grid_layout)
        main_layout.addWidget(left_grid_widget, stretch=3)

        # Crane and truck layout
        crane_truck_layout = QHBoxLayout()
        crane_truck_layout.setAlignment(Qt.AlignCenter)  # Align elements in the center

        # Truck widget
        self.truck_widget = TruckWidget()
        self.truck_widget.setFixedSize(80, 80)  # Adjusted size
        self.truck_widget.setStyleSheet("border: 2px solid black; background-color: yellow; border-radius: 40px;")
        crane_truck_layout.addWidget(self.truck_widget, alignment=Qt.AlignCenter)

        # Crane
        self.crane = QLabel()
        self.crane.setFixedSize(50, 500)  # Made taller
        self.crane.setStyleSheet("background-color: red; border-radius: 10px;")
        crane_truck_layout.addWidget(self.crane, alignment=Qt.AlignCenter)

        main_layout.addLayout(crane_truck_layout, stretch=1)

        # Right grid
        right_grid_widget = QWidget()
        right_grid_layout = GridWidget(*grid_right_dims)
        right_grid_widget.setLayout(right_grid_layout)
        main_layout.addWidget(right_grid_widget, stretch=3)

        layout.addLayout(main_layout)

        # Bottom control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        # Next Move Button
        next_button = QPushButton("Next Move")
        next_button.setStyleSheet("font-size: 14px; padding: 8px;")
        next_button.clicked.connect(self.next_move)  # Connect to the next_move method
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

    def set_moves(self, moves):
        """Set the moves for the screen."""
        self.moves = moves
        self.current_move_index = 0

    def next_move(self):
        """Execute the next move in the list."""
        if self.current_move_index < len(self.moves):
            move = self.moves[self.current_move_index]
            print(f"Executing move: {move}")  # Log the move for debugging

            # Determine source and destination positions
            source = move.m_from
            destination = move.m_to

            # Adjust coordinates for grid logic
            source_row = source.m + 1
            source_col = source.n + 1
            dest_row = destination.m + 1
            dest_col = destination.n + 1

            # Check if the move is only for the crane
            if move.container.name == "UNUSED":
                # Only animate the crane moving
                print(f"Animating crane from {source} to {destination}")
                # Placeholder for crane animation logic
            else:
                # Handle movement based on source and destination locations
                if source.location == "SHIP" and destination.location == "SHIP":
                    # Move within the ship
                    self.update_right_grid(source_row, source_col, "", "white")  # Clear source cell
                    self.update_right_grid(dest_row, dest_col, move.container.name, "white")  # Update destination cell

                elif source.location == "SHIP" and destination.location == "TRUCK":
                    # Move from the ship to the truck
                    self.update_right_grid(source_row, source_col, "", "white")  # Clear the ship cell
                    self.truck_widget.update_container(move.container.name)  # Add container to the truck

                elif source.location == "TRUCK" and destination.location == "SHIP":
                    # Move from the truck to the ship
                    self.truck_widget.clear_container()  # Clear the truck
                    self.update_right_grid(dest_row, dest_col, move.container.name, "white")  # Add to the ship

                elif source.location == "CRANE_REST" or destination.location == "CRANE_REST":
                    # Handle crane rest movements if necessary (no visual update for now)
                    pass

                else:
                    print(f"Unhandled move: {move}")

            # Increment the move index
            self.current_move_index += 1
        else:
            print("No more moves.")
