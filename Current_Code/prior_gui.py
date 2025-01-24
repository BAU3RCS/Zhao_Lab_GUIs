from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QGridLayout, QSpinBox, QComboBox, QGraphicsOpacityEffect)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
import sys
import serial.tools.list_ports

from Controllers.prior_driver import prior

def get_active_usb_serial_port():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "USB" in desc:
            return port
    return None

try: 
    port = int(list(filter(str.isdigit, get_active_usb_serial_port()))[0])
except TypeError: 
    raise RuntimeError("USB COM not connected")

stage = prior()

class priorGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.goto_x_changed = False
        self.goto_y_changed = False
        self.step_size = 100
        self.xpos, self.ypos = 0, 0
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        self.interface()
        self.connect_signals()

        for widget in self.findChildren(QWidget):
            if widget != self.port_spinbox and widget != self.connect_button:
                widget.setDisabled(True)


    def interface(self):
        self.setWindowTitle("Prior Optiscan Stage Controller")
        self.resize(500,300)

        # Main Layout
        main_layout = QHBoxLayout()

        # Step Size Entry
        self.stepsize_layout = QHBoxLayout()
        self.stepsize_layout.addWidget(QLabel(" Step size (microns):"))
        self.step_size_spinbox = QSpinBox()
        self.step_size_spinbox.setRange(0, int(stage.x_lim / 2)) 
        self.step_size_spinbox.setValue(self.step_size)
        self.stepsize_layout.addWidget(self.step_size_spinbox)

        # Arrow-shaped buttons
        self.up_button = QPushButton("↑")
        self.down_button = QPushButton("↓")
        self.left_button = QPushButton("←")
        self.right_button = QPushButton("→")

        # Customize button size
        button_size = 80  # Define a square size
        for button in [self.up_button, self.down_button, self.left_button, self.right_button]:
            button.setFixedSize(button_size, button_size)
            button.setStyleSheet("font-size: 20px; font-weight: bold; background-color: cyan; color: blue") 

        # Layout for 2x2 arrow matrix
            
        self.arrow_group  = QGroupBox()
        self.arrow_layout = QGridLayout()
        self.arrow_layout.addWidget(self.up_button, 0, 1)    # Up button
        self.arrow_layout.addWidget(self.left_button, 1, 0)  # Left button
        self.arrow_layout.addWidget(self.right_button, 1, 2) # Right button
        self.arrow_layout.addWidget(self.down_button, 2, 1)  # Down button


        self.arrow_group.setLayout(self.arrow_layout)

        # Current Coordinates Display
        self.coordinates_group  = QGroupBox()
        self.coordinates_layout = QGridLayout()
        self.xpos_label, self.ypos_label = QLabel(f"X: {self.xpos}"), QLabel(f"Y: {self.ypos}") 
        self.coordinates_layout.addWidget(QLabel("Current coordinates"), 0, 0)
        self.coordinates_layout.addWidget(self.xpos_label, 1, 0)
        self.coordinates_layout.addWidget(self.ypos_label, 1, 1)

        self.coordinates_group.setLayout(self.coordinates_layout)

        # Connect button

        self.connect_button = QPushButton("CONNECT")
        self.connect_button.setCheckable(True)
        self.connect_button.setStyleSheet("font-size: 15px; font-weight: bold; background-color: green")

        # port box
        self.port_layout = QHBoxLayout()
        self.port_label = QLabel("Port")
        self.port_layout.addWidget(self.port_label)
        self.port_spinbox = QSpinBox()
        self.port_spinbox.setRange(1, 4)
        self.port_spinbox.setValue(port)
        self.port_layout.addWidget(self.port_spinbox)
        
        # Position Box
        position_group = QGroupBox()
        position_layout = QGridLayout()
        
        self.x_input = QSpinBox()
        self.y_input = QSpinBox()
        self.x_input.setRange(int(-108000 / 2), int(108000 / 2))
        self.y_input.setRange(int(-108000 / 2), int(108000 / 2))
        self.gotopos_button = QPushButton("GO TO POSITION")
        self.gotopos_button.setStyleSheet("font-size: 10px; font-weight: bold; background-color: orange; color: black;") 

        position_layout.addWidget(self.gotopos_button, 0, 1)
        position_layout.addWidget(QLabel("X:"), 1, 0)
        position_layout.addWidget(self.x_input, 1, 1)
        position_layout.addWidget(QLabel("Y:"), 2, 0)
        position_layout.addWidget(self.y_input, 2, 1)

        position_group.setLayout(position_layout)

        # Stop and Home Buttons

        #self.stop_button = QPushButton("STOP")
        #self.arrow_layout.addWidget(self.stop_button, 1, 1)  # stop button
        #self.stop_button.setFixedSize(button_size, button_size)
        #self.stop_button.setStyleSheet("font-size: 15px; font-weight: bold; background-color: lightblue; color: red")

        self.home_button = QPushButton("HOME") # home button
        self.home_button.setStyleSheet("font-size: 15px; font-weight: bold; background-color: #D8D33E; color: black")


         # Left panel
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel(" Move stage"))
        left_panel.addWidget(self.arrow_group)
        left_panel.addLayout(self.stepsize_layout)

        # Right panel
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.home_button)
        right_panel.addWidget(self.coordinates_group)
        right_panel.addWidget(position_group)
        right_panel.addWidget(self.connect_button)
        right_panel.addLayout(self.port_layout)

        # main panel
        main_layout.addLayout(left_panel)
        main_layout.addLayout(right_panel)
        self.setLayout(main_layout)

    def connect_signals(self):
        """
        Connects signals of all widgets to their respective functions or handlers.
        """
        # Buttons
        self.up_button.clicked.connect(self.move_up)
        self.down_button.clicked.connect(self.move_down)
        self.left_button.clicked.connect(self.move_left)
        self.right_button.clicked.connect(self.move_right)
        #self.stop_button.clicked.connect(self.stop)
        self.home_button.clicked.connect(self.home)
        self.gotopos_button.clicked.connect(self.go_to_position)
        self.connect_button.toggled.connect(self.connect_hardware)

        # Spin Boxes
        self.step_size_spinbox.editingFinished.connect(self.update_step_size)



    def connect_hardware(self, checked):
        # Update the label based on the toggle button state
        self.devport = self.port_spinbox.value()

        if checked:
            stage.connect(self.devport)
            self.connect_button.setText("DISCONNECT")
            self.connect_button.setStyleSheet("background-color: red")
            self.xpos_label.setText(f"X: {self.xpos}")
            self.ypos_label.setText(f"Y: {self.ypos}")
        
        else:
            stage.disconnect()
            self.connect_button.setText("CONNECT")
            print("Disconnected")
            self.connect_button.setStyleSheet("background-color: green")

        for widget in self.findChildren(QWidget):
            if widget != self.connect_button:
                widget.setDisabled(not checked)

        self.port_label.setDisabled(checked)
        self.port_spinbox.setDisabled(checked)

    def move_left(self):
        stage.move_rel(self.step_size, 0)
        print("Move Left button clicked")
        self.update_pos_label()

    def move_right(self):
        stage.move_rel(-self.step_size, 0)
        print("Move Right button clicked")
        self.update_pos_label()

    def move_up(self):
        stage.move_rel(0, self.step_size)
        print("Move Up button clicked")
        self.update_pos_label()

    def move_down(self):
        stage.move_rel(0, -self.step_size)
        print("Move Down button clicked")
        self.update_pos_label()

    #def stop(self):
     #   stage.stop_moving()
      #  print("Stop button clicked")

    def home(self):
        stage.calibrate()
        stage.wait()
        self.update_pos_label()
        print("Home button clicked")

    def update_step_size(self):
        self.step_size = self.step_size_spinbox.value()
        print(f"Step size updated to {self.step_size} microns.")

    def go_to_position(self):
        x = self.x_input.value()
        y = self.y_input.value()
        print(f"Going to position: X={x}, Y={y}")
        stage.goto_pos(x, y)
        self.update_pos_label()

    def update_pos_label(self):
        stage.wait()
        self.xpos, self.ypos = stage.get_pos()
        self.xpos_label.setText(f"X: {self.xpos}")
        self.ypos_label.setText(f"Y: {self.ypos}") 

    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key.Key_Right:
            self.move_right()
        if event.key() == Qt.Key.Key_Left:
            
            self.move_left()
        if event.key() == Qt.Key.Key_Down:
            self.move_down()
        if event.key() == Qt.Key.Key_Up:
            self.move_up()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = priorGUI()
    window.show()
    sys.exit(app.exec())
