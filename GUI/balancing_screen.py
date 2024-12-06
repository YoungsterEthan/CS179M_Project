from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPointF, QEasingCurve
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

        # Add a circle to indicate the crane/container
        self.circle_label = QLabel(self)
        self.circle_label.setFixedSize(40, 40)  # Circle size (same as grid cells)
        self.circle_label.setStyleSheet("background-color: rgba(255, 165, 0, 180); border-radius: 20px;")
        self.circle_label.hide()  # Initially hidden

        # Initialize circle animation
        self.circle_animation = QPropertyAnimation(self.circle_label, b"geometry")
        self.circle_animation.setDuration(500)  # Set animation duration (e.g., 500ms)
        self.circle_animation.setEasingCurve(QEasingCurve.InOutQuad)  # Smooth transition

    def setup_circle(self, row, col):
        """Place the circle at a specific grid cell."""
        x, y = self.get_cell_position(row, col)
        self.circle_label.move(x, y)
        self.circle_label.show()

    def animate_circle(self, row, col, destination):
        """Animate the circle to move to a specific grid cell."""
        # Calculate the position of the target cell
        x = 0
        y = 0


        if destination == "CRANE_REST":
            x,y = 1152, 280
        elif destination == "TRUCK":
            x,y = 1045, 430
        else:
            x, y = self.get_cell_position(row, col)

        # Calculate the center of the cell for the circle
        circle_diameter = 40  # Adjust this to match the circle size
        x_center = x
        y_center = y


        # Animate the circle to the new position
        self.circle_animation.stop()  # Stop any ongoing animation
        self.circle_animation.setStartValue(self.circle_label.geometry())
        self.circle_animation.setEndValue(QRect(x_center, y_center, circle_diameter, circle_diameter))
        self.circle_animation.start()
        self.circle_label.show()



    def get_cell_position(self, row, col):
        """Calculate the top-left position of a grid cell for the circle."""
        # Get grid geometry (top-left corner position of the grid)
        # self.right_grid_layout.
 
        grid_bottom_left_x = 1252
        grid_bottom_left_y = 655

        # Cell dimensions
        cell_width = 40  # Fixed size for grid cells
        cell_height = 40

        # Calculate position of the top-left corner of the cell
        x = grid_bottom_left_x + (col - 1) * 40
        y = grid_bottom_left_y - (row - 1) * 50
        # print(f"Cell ({row}, {col}) calculated position: ({x}, {y})")

        return x, y



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
        """Execute the next move in the list and animate the circle."""
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



            # Animate the crane to the destination cell
            self.animate_circle(dest_row, dest_col, destination.location)

            # Handle container movement
            if move.container.name != "UNUSED":
                if source.location == "SHIP" and destination.location == "SHIP":
                    self.update_right_grid(source_row, source_col, "", "white")  # Clear source cell
                    self.update_right_grid(dest_row, dest_col, move.container.name, "white")  # Update destination cell

                elif source.location == "SHIP" and destination.location == "TRUCK":
                    self.update_right_grid(source_row, source_col, "", "white")  # Clear the ship cell
                    self.truck_widget.update_container(move.container.name)  # Add container to the truck

                elif source.location == "TRUCK" and destination.location == "SHIP":
                    self.truck_widget.clear_container()  # Clear the truck
                    self.update_right_grid(dest_row, dest_col, move.container.name, "white")  # Add to the ship

            # Increment the move index
            self.current_move_index += 1
        else:
            print("No more moves.")



    def get_crane_position(self):
        """Get the absolute pixel position of the crane."""
        return self.crane.geometry().center().x(), self.crane.geometry().center().y()

    def get_truck_position(self):
        """Get the absolute pixel position of the truck."""
        return self.truck_widget.geometry().center().x(), self.truck_widget.geometry().center().y()
    
    # def mousePressEvent(self, event):
    #     """Capture mouse click and print the screen coordinates."""
    #     x = event.globalX()
    #     y = event.globalY()
    #     print(f"Screen coordinates: x={x}, y={y}")


