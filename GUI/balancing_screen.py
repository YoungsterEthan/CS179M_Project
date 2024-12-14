from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout, QTextEdit, QToolTip, QLineEdit
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPointF, QEasingCurve, QTimer, QEvent
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont

from Logger import Logger

class GridWidget(QGridLayout):
    """Customizable grid for displaying containers."""
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols

        # Remove spacing between cells
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        # Store metadata for containers
        self.container_metadata = {}  # Key: (row, col), Value: dict with container info

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
                cell.setAttribute(Qt.WA_Hover)  # Enable hover events
                cell.installEventFilter(self)  # Install the event filter
                self.addWidget(cell, row, col)

    def update_cell(self, row, col, text, color="white", metadata=None):
        """Update a specific cell with text, background color, and optional metadata."""
        text_color = "black" if color == "white" else "white"
        cell = self.itemAtPosition(row, col).widget()
        if cell:
            cell.setText(text)
            cell.setStyleSheet(
                f"border: 1px solid black; background-color: {color}; color: {text_color}; font-size: 12px; text-align: center;"
            )

            self.container_metadata[(row, col)] = metadata

    def eventFilter(self, obj, event):
        """Handle hover events to display tooltips."""
        if event.type() == QEvent.HoverEnter or event.type() == QEvent.HoverMove:
            # Get the position of the hover event relative to the widget
            hover_pos = obj.mapToGlobal(event.pos())

            # Check if the object has metadata
            for (row, col), metadata in self.container_metadata.items():
                cell = self.itemAtPosition(row, col)
                if cell and cell.widget() == obj:
                    # If metadata exists, display it
                    tooltip_text = "\n".join(f"{key}: {value}" for key, value in metadata.items())
                    QToolTip.showText(hover_pos, tooltip_text, obj)
                    return True

            # If no metadata, show "Empty Cell"
            QToolTip.showText(hover_pos, "Empty Cell", obj)
            return True
        elif event.type() == QEvent.HoverLeave:
            QToolTip.hideText()
            return True

        return super().eventFilter(obj, event)
    
class TruckWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(50, 50)
        self.container_name = ""

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
    def __init__(self, main_window, title, switch_to_home, grid_left_dims, grid_right_dims, show_manifest_viewer):
        super().__init__()
        self.main_window = main_window

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Initialize logger
        self.logger = Logger()

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # dims
        self.left_grid_dims = grid_left_dims
        self.right_grid_dims = grid_right_dims

        self.moves = []
        self.time_remaining = 0

        # Horizontal layout for grids, crane, and truck
        main_layout = QHBoxLayout()
        main_layout.setSpacing(30)  # Space between sections

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

        # Back to Login Button
        back_to_login_button = QPushButton("Back to Login")
        back_to_login_button.setFont(QFont("Arial", 12, QFont.Bold))
        back_to_login_button.setFixedSize(250, 40)
        back_to_login_button.setStyleSheet(
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
        back_to_login_button.clicked.connect(self.switch_to_login)
        controls_layout.addWidget(back_to_login_button)

        # Next Move Button
        next_button = QPushButton("Next Move")
        next_button.setFont(QFont("Arial", 12, QFont.Bold))
        next_button.setFixedSize(350, 40)
        next_button.setStyleSheet(
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
        next_button.clicked.connect(self.next_move)
        controls_layout.addWidget(next_button)

        # Estimated Time Remaining
        self.time_label = QLabel("Estimated Time Remaining: N/A")
        self.time_label.setStyleSheet("font-size: 14px; color: black;")
        controls_layout.addWidget(self.time_label)

        # Manifest Button
        manifest_button = QPushButton("View Manifest")
        manifest_button.setFont(QFont("Arial", 12, QFont.Bold))
        manifest_button.setFixedSize(250, 40)
        manifest_button.setStyleSheet(
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
        manifest_button.clicked.connect(show_manifest_viewer)
        controls_layout.addWidget(manifest_button)


        # Back Button
        back_button = QPushButton("Back to Home")
        back_button.setFont(QFont("Arial", 12, QFont.Bold))
        back_button.setFixedSize(250, 40)
        back_button.setStyleSheet(
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
        back_button.clicked.connect(switch_to_home)
        controls_layout.addWidget(back_button)

        layout.addLayout(controls_layout)
        self.setLayout(layout)

        # Store the grid layouts for customization
        self.left_grid_layout = left_grid_layout
        self.right_grid_layout = right_grid_layout

        # Add a circle to indicate the crane/container
        self.circle_label = QLabel(self)
        self.circle_label.setFixedSize(40, 40)
        self.circle_label.setStyleSheet("background-color: rgba(255, 165, 0, 180); border-radius: 20px;")
        self.circle_label.hide()  # Initially hidden

        # Initialize circle animation
        self.circle_animation = QPropertyAnimation(self.circle_label, b"geometry")
        self.circle_animation.setDuration(500) 
        self.circle_animation.setEasingCurve(QEasingCurve.InOutQuad)  # Smooth transition

        # Timer for alternating animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.toggle_animation_position)
        self.is_animating_to_source = True 

        self.current_source = None  
        self.current_destination = None  #

        #Console for logging moves
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFixedSize(500, 100) 
        self.console.setStyleSheet(
            """
            QTextEdit {
                background-color: #4682B4;  /* Steel Blue */
                color: white;  /* White text */
                font-family: Arial, sans-serif;
                font-size: 12px;
                border-radius: 8px;  /* Rounded corners */
                padding: 10px;
                border: 2px solid #1E90FF;  /* Dodger Blue border for focus */
            }
            """
        )

        # Comment box for operator input
        self.comment_box = QLineEdit()
        self.comment_box.setPlaceholderText("Enter your comment here and press Enter...")
        self.comment_box.setFixedSize(500, 30)
        self.comment_box.setStyleSheet(
            """
            QLineEdit {
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
                font-size: 12px;
                border-radius: 5px;
                padding: 5px;
                border: 2px solid #4682B4;  /* Steel Blue border */
            }
            """
        )
        self.comment_box.returnPressed.connect(self.log_comment)

        # Add the console and comment box in a bottom-centered position
        console_layout = QVBoxLayout()
        console_layout.addWidget(self.console)
        console_layout.addWidget(self.comment_box)

        layout.addLayout(console_layout)
        self.setLayout(layout)

    def switch_to_login(self):
        """Switch to the login screen and save the current state."""
        self.main_window.show_login_screen()



    def toggle_animation_position(self):
            """Alternate the circle's position between source and destination."""
            if self.is_animating_to_source:
                if self.current_source:
                    self.animate_circle(*self.current_source, self.source.location)
            else:
                if self.current_destination:
                    self.animate_circle(*self.current_destination, self.destination.location)
            self.is_animating_to_source = not self.is_animating_to_source

    def animate_circle(self, row, col, location):
            """Animate the circle to move to a specific grid cell."""
            # Calculate the position of the target cell
            x = 0
            y = 0

            if location == "CRANE_REST":
                x, y = 1125, 280
            elif location == "TRUCK":
                x, y = 1020, 475
            elif location == "SHIP":
                x, y = self.get_cell_position(row, col)
            else:
                x, y = self.get_left_cell_position(row, col)
                

            # Animate the circle to the new position
            circle_diameter = 40 
            x_center = x
            y_center = y

            self.circle_animation.stop()  # Stop any ongoing animation
            self.circle_animation.setStartValue(self.circle_label.geometry())
            self.circle_animation.setEndValue(QRect(x_center, y_center, circle_diameter, circle_diameter))
            self.circle_animation.start()
            self.circle_label.show()

    def get_cell_position(self, row, col):
        """Calculate the top-left position of a grid cell for the circle."""
        grid_bottom_left_x = 1190
        grid_bottom_left_y = 695


        x = grid_bottom_left_x + (col - 1) * 40
        y = grid_bottom_left_y - (row - 1) * 50

        return x, y
    
    def get_left_cell_position(self, row, col):
        """Calculate the top-left position of a grid cell for the circle."""
        grid_bottom_left_x = 13
        grid_bottom_left_y = 685


        # Calculate position of the top-left corner of the cell
        x = grid_bottom_left_x + (col - 1) * 40
        y = grid_bottom_left_y - (row - 1) * 60

        return x, y

    def update_left_grid(self, row, col, text, color="white", metadata={}):
        """Update a cell in the left grid."""
        self.left_grid_layout.update_cell(row, col, text, color)
        n_row, n_col = self.right_grid_dims
        r = n_row - row
        c = col - 1
        self.left_grid_layout.update_cell(r, c, text, color, metadata)

    def update_right_grid(self, row, col, text, color="white", metadata={}):
        """Update a cell in the right grid."""
        n_row, n_col = self.right_grid_dims
        r = n_row - row
        c = col - 1
        self.right_grid_layout.update_cell(r, c, text, color, metadata)

    def set_moves(self, moves):
        """Set the moves for the screen."""
        self.moves = moves
        self.current_move_index = 0
        self.calculate_total_time()
        self.update_time_label

    def calculate_total_time(self):
        """Calculate the total time for all moves."""
        self.total_time = sum(move.time_to_move for move in self.moves)

    def calculate_remaining_time(self):
        """Calculate the remaining time for the moves."""
        remaining_moves = self.moves[self.current_move_index:]
        return sum(move.time_to_move for move in remaining_moves)

    def update_time_label(self):
        """Update the time label with the remaining time."""
        remaining_time = self.calculate_remaining_time()
        self.time_label.setText(f"Estimated Time Remaining: {remaining_time} minutes")

    def log_comment(self):
            """Log the comment entered in the comment box."""
            comment = self.comment_box.text().strip()
            if comment:
                self.logger.log_comment(comment)  # Log the comment using Logger
                self.console.append(f"Comment logged: {comment}")  # Display confirmation in the console
                self.comment_box.clear()  # Clear the comment box


    def next_move(self):
        """Execute the next move in the list, animate the circle, and log the move."""
        
        if self.current_move_index < len(self.moves):
            move = self.moves[self.current_move_index]
            print(f"Executing move: {move}")
            self.main_window.save_move_progress()

            # Determine source and destination positions
            source = move.m_from
            destination = move.m_to

            # Log the move details in the console
            move_text = f"Executing move: Move {move.container.name} " \
                        f"from {source.location}[{source.m + 1}, {source.n + 1}] " \
                        f"to {destination.location}[{destination.m + 1}, {destination.n + 1}] " \
                        f"in {move.time_to_move} minutes"
            self.console.append(move_text)

            # Adjust coordinates for grid logic
            source_row = source.m + 1
            source_col = source.n + 1
            dest_row = destination.m + 1
            dest_col = destination.n + 1
            # Save the source and destination positions for animation
            self.current_source = (source_row, source_col)
            self.current_destination = (dest_row, dest_col)
            self.source = source
            self.destination = destination

            # Start the animation timer
            self.animation_timer.start(1000)

            # Handle container movement
            self._handle_container_movement(move)

            # Increment the move index
            self.current_move_index += 1

            # Update time label
            self.update_time_label()

            if self.current_move_index >= len(self.moves):
                print("All moves completed.")
                self.main_window.recovery_logger.delete()
                self.main_window.delete_last()
        else:
            self.console.append("No more moves.")  # Notify when there are no more moves
            print("No more moves.")

    def _handle_container_movement(self, move):
        if move.container.name != "UNUSED":
            if self.source.location == "SHIP" and self.destination.location == "SHIP":
                self.update_right_grid(*self.current_source, "", "white")  # Clear source cell
                self.update_right_grid(*self.current_destination, move.container.name, "white", {"Name": move.container.name, "Weight": move.container.weight})  # Update destination cell

            elif self.source.location == "SHIP" and self.destination.location == "TRUCK":
                self.update_right_grid(*self.current_source, "", "white")  # Clear the ship cell
                self.truck_widget.update_container(move.container.name)  # Add container to the truck

            elif self.source.location == "TRUCK" and self.destination.location == "SHIP":
                self.truck_widget.clear_container()  # Clear the truck
                self.update_right_grid(*self.current_destination, move.container.name, "white", {"Name": move.container.name, "Weight": move.container.weight})  # Add to the ship

            elif self.source.location == "SHIP" and self.destination.location == "BUFFER":
                self.update_right_grid(*self.current_source, "", "white")  # Clear source cell
                self.update_left_grid(*self.current_destination, "", "white", {"Name": move.container.name, "Weight": move.container.weight})  # update buffer


