from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt
from ContainerData import ContainerData

class LoadUnloadSelectionScreen(QDialog):
    def __init__(self, manifest, confirm_callback):
        super().__init__()
        self.setWindowTitle("Select Containers to Load/Unload")
        self.setGeometry(100, 100, 600, 400)

        self.manifest = manifest 
        self.confirm_callback = confirm_callback
        self.offload_containers = []
        self.load_containers = [] 

        # Main layout
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Select Containers to Load/Unload")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Offload section
        offload_label = QLabel("Select Containers to Offload:")
        layout.addWidget(offload_label)

        self.offload_table = QTableWidget()
        self.offload_table.setColumnCount(2)
        self.offload_table.setHorizontalHeaderLabels(["Container", "Offload?"])
        self.offload_table.horizontalHeader().setStretchLastSection(True)
        self.populate_offload_table()
        layout.addWidget(self.offload_table)

        # Load setcion
        load_label = QLabel("Add Containers to Load:")
        layout.addWidget(load_label)

        load_input_layout = QHBoxLayout()
        self.container_name_input = QLineEdit()
        self.container_name_input.setPlaceholderText("Container Name")
        self.container_weight_input = QLineEdit()
        self.container_weight_input.setPlaceholderText("Weight")
        load_add_button = QPushButton("Add")
        load_add_button.clicked.connect(self.add_load_container)
        load_input_layout.addWidget(self.container_name_input)
        load_input_layout.addWidget(self.container_weight_input)
        load_input_layout.addWidget(load_add_button)
        layout.addLayout(load_input_layout)

        self.load_list_label = QLabel("Containers to Load:")
        layout.addWidget(self.load_list_label)

        # Confirm button
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm_selection)
        layout.addWidget(confirm_button)


        self.setLayout(layout)

    def populate_offload_table(self):
        """Populate the offload table with manifest data."""
        containers = self.manifest.get_containers()
        self.offload_table.setRowCount(len(containers))
        for i, container in enumerate(containers):
            self.offload_table.setItem(i, 0, QTableWidgetItem(container.name))
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(lambda state, c=container: self.toggle_offload_container(c, state))
            self.offload_table.setCellWidget(i, 1, checkbox)

    def toggle_offload_container(self, container, state):
        """Add or remove a container from the offload list."""
        if state == Qt.Checked:
            self.offload_containers.append(container)
        elif container in self.offload_containers:
            self.offload_containers.remove(container)

    def add_load_container(self):
        """Add a container to the load list."""
        name = self.container_name_input.text().strip()
        weight = self.container_weight_input.text().strip()

        # Validate input
        if not name or not weight.isdigit():
            self.show_message("Invalid Input", "Please enter a valid container name and weight.")
            return

        if name in {"NAN", "UNUSED"}:
            self.show_message("Invalid Container Name", "The container name cannot be 'NAN' or 'UNUSED'.")
            return

        # Add container
        container = ContainerData(name, weight)
        self.load_containers.append(container)
        self.container_name_input.clear()
        self.container_weight_input.clear()
        self.update_load_list()

    def update_load_list(self):
        """Update the list of containers to load."""
        self.load_list_label.setText("Containers to Load:\n" + "\n".join([f"{c.name} ({c.weight})" for c in self.load_containers]))


    def confirm_selection(self):
        """Confirm selection and pass data to the callback."""
        self.confirm_callback(self.offload_containers, self.load_containers)
        self.accept()

    def show_message(self, title, message):
        """Show a custom error message."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
                color: black;
            }
            QMessageBox QLabel {
                color: black;
            }
            QMessageBox QPushButton {
                background-color: #f0f0f0;
                border: 1px solid black;
                color: black;
            }
            """
        )
        msg_box.exec_()