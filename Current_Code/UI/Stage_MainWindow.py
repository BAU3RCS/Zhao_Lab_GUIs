"""
Main Stage Control GUI Window

Author: Brandon Bauer and Musarate Shams
Written January 2025

Updated XXXXXXXXXXXX
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
from PyQt6.QtWidgets import QLabel, QPushButton

from UI.Custom_Widgets.Custom_Widgets import CustomLineEdit
from UI.Logic.Button_To_Device_logic import device_commands
from UI.prior_gui import priorGUI

# Subclass QMainWindow to customize your application's main window
class Stage_MainWindow(QMainWindow):
    
    # Visual Settings
    
    # Title bar heading settings
    max_height_title_bar = 30
    title_fontsize       = 13
    
    # Axis Label settings
    min_axis_width = 75
    
    # Button sizes
    min_button_height = 32
    min_step_button_width  = 75
    
    # Input Box Settings
    max_lineedit_width = 200
    
    # Label Settings
    min_label_width = 100
    
    def __init__(self, commands:device_commands, prior_stage):
        super().__init__()

        # Class connected to devices
        self.commands    = commands
        self.prior_stage = prior_stage
        
        self.setWindowTitle(" Thorlabs and Prior Stage Controls")
        
        # Toplevel Layout
        self.toplevel_layout = QVBoxLayout()
        
        
        # Main Divisions and Widgets
        # region
        
        #   Thorlabs
        #   region
        self.thorlabs_layout = QGridLayout()
        self.thorlabs_frame  = QFrame(self)
        self.thorlabs_frame.setFrameShape(QFrame.Shape.Box)  # Set the frame shape
        self.thorlabs_frame.setFrameShadow(QFrame.Shadow.Raised)  # Add a shadow effect
        self.thorlabs_frame.setLayout(self.thorlabs_layout)
        
        self.thorlabs_label = QLabel("Thorlabs")
        self.thorlabs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thorlabs_label.setMaximumHeight(self.max_height_title_bar)
        self.thorlabs_font = QFont()
        self.thorlabs_font.setPointSize(self.title_fontsize)
        self.thorlabs_font.setBold(True)
        self.thorlabs_label.setFont(self.thorlabs_font)
        
        self.toplevel_layout.addWidget(self.thorlabs_label)
        self.toplevel_layout.addWidget(self.thorlabs_frame)
        
        # Here we will have a 5 x 6 grid
        #
        # 0      0 1 2 3 4 5 
        # 1      0 1 2 3 4 5
        # 2      0 1 2 3 4 5
        # 3      0 1 2 3 4 5
        # 4      0 1 2 3 4 5
        
        #       Thorlabs subdivisions
        
        #           Titles row 0
        #           region
        self.title_row     = []
        
        # Title labels and adding them to the layout
        self.title_row.append(QLabel("Axis"))
        self.title_row.append(QLabel("Current Position"))
        self.title_row.append(QLabel("Step Size"))
        self.title_row.append(QLabel("Step"))
        self.title_row.append(QLabel("Move To"))
        
        # subtracting one here to allow me to stretch the last titlte across 2 columns
        for i in range(len(self.title_row)-1):
            self.title_row[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.title_row[i].setMaximumHeight(self.max_height_title_bar)
            self.thorlabs_layout.addWidget(self.title_row[i], 0, i)
        
        self.title_row[4].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_row[4].setMaximumHeight(self.max_height_title_bar)
        self.thorlabs_layout.addWidget(self.title_row[4], 0, 4, 1, 2)
        
            
        #           endregion
        
        #           x-axis row 1
        #           region
        self.x_row        = []
        
        self.x_row.append(QLabel("X:"))
        self.x_row[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_row[0].setMinimumWidth(self.min_axis_width)
        
        self.x_row.append(QLabel(str(self.commands.x_get_pos())+" mm"))
        self.x_row[1].setStyleSheet("border: 2px solid grey;")
        self.x_row[1].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_row[1].setMinimumWidth(self.min_label_width)
        
        self.x_row.append(CustomLineEdit("mm"))
        self.x_row[2].setMaxLength(10)
        self.x_row[2].setPlaceholderText("0.5")
        self.x_row[2].setText("0.5")
        self.x_row[2].setMaximumWidth(self.max_lineedit_width)
        
        self.x_row[2].editingFinished.connect(lambda: self.commands.x_set_step_size(self.x_row[2]))
        
        self.x_stepbuttons = QHBoxLayout()
        self.x_step_left   = QPushButton("- X",self)
        self.x_step_right  = QPushButton("+ X",self)
        self.x_step_right.setMinimumHeight(self.min_button_height)
        self.x_step_right.setMinimumWidth(self.min_step_button_width)
        self.x_step_left.setMinimumHeight(self.min_button_height)
        self.x_step_left.setMinimumWidth(self.min_step_button_width)
        self.x_stepbuttons.addWidget(self.x_step_left)
        self.x_stepbuttons.addWidget(self.x_step_right)
        
        self.x_step_left.clicked.connect( lambda: self.commands.x_stepped_backward(self.x_row[1]))
        self.x_step_right.clicked.connect(lambda: self.commands. x_stepped_forward(self.x_row[1]))
        
        self.x_row.append(self.x_stepbuttons)
        
        self.x_row.append(CustomLineEdit("mm"))
        self.x_row[4].setMaxLength(10)
        self.x_row[4].setPlaceholderText("coordinate")
        self.x_row[4].setMaximumWidth(self.max_lineedit_width)
        
        self.x_move_button  = QPushButton("Move",self)
        self.x_move_button.setMinimumHeight(self.min_button_height)
        self.x_row.append(self.x_move_button)
        
        self.x_row[5].clicked.connect(lambda: commands.x_move_to(self.x_row[4], self.x_row[1])) 
        
        for i in range(len(self.x_row)):
            if i == 3:
                self.thorlabs_layout.addLayout(self.x_row[i], 1, i)
            else:
                self.thorlabs_layout.addWidget(self.x_row[i], 1, i)
        
        # Widgets
        
        
        #           endregion
        
        #           y-axis row 2
        #           region
        self.y_row         = []
        
        self.y_row.append(QLabel("Y:"))
        self.y_row[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_row[0].setMinimumWidth(self.min_axis_width)
        
        self.y_row.append(QLabel(str(self.commands.y_get_pos())+" mm"))
        self.y_row[1].setStyleSheet("border: 2px solid grey;")
        self.y_row[1].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_row[1].setMinimumWidth(self.min_label_width)
        
        self.y_row.append(CustomLineEdit("mm"))
        self.y_row[2].setMaxLength(10)
        self.y_row[2].setPlaceholderText("0.5")
        self.y_row[2].setText("0.5")
        self.y_row[2].setMaximumWidth(self.max_lineedit_width)
        
        self.y_row[2].editingFinished.connect(lambda: self.commands.y_set_step_size(self.y_row[2]))
        
        self.y_stepbuttons = QHBoxLayout()
        self.y_step_left   = QPushButton("- Y",self)
        self.y_step_right  = QPushButton("+ Y",self)
        self.y_step_right.setMinimumHeight(self.min_button_height)
        self.y_step_right.setMinimumWidth(self.min_step_button_width)
        self.y_step_left.setMinimumHeight(self.min_button_height)
        self.y_step_left.setMinimumWidth(self.min_step_button_width)
        self.y_stepbuttons.addWidget(self.y_step_left)
        self.y_stepbuttons.addWidget(self.y_step_right)
        self.y_row.append(self.y_stepbuttons)
        
        self.y_step_left.clicked.connect( lambda: self.commands.y_stepped_backward(self.y_row[1]))
        self.y_step_right.clicked.connect(lambda: self.commands.y_stepped_forward(self.y_row[1]))
        
        self.y_row.append(CustomLineEdit("mm"))
        self.y_row[4].setMaxLength(10)
        self.y_row[4].setPlaceholderText("coordinate")
        self.y_row[4].setMaximumWidth(self.max_lineedit_width)
      
        self.y_move_button  = QPushButton("Move",self)
        self.y_move_button.setMinimumHeight(self.min_button_height)
        self.y_row.append(self.y_move_button)
        
        self.y_row[5].clicked.connect(lambda: commands.y_move_to(self.y_row[4], self.y_row[1])) 
        

    
        for i in range(len(self.y_row)):
            if i ==3:
                self.thorlabs_layout.addLayout(self.y_row[i], 2, i)
            else:
                self.thorlabs_layout.addWidget(self.y_row[i], 2, i)
        #           endregion

        #           z-axis row 3
        #           region
        self.z_row         = []
        
        self.z_row.append(QLabel("Z:"))
        self.z_row[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_row[0].setMinimumWidth(self.min_axis_width)
        
        self.z_row.append(QLabel(str(self.commands.z_get_pos())+" mm"))
        self.z_row[1].setStyleSheet("border: 2px solid grey;")
        self.z_row[1].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.z_row[1].setMinimumWidth(self.min_label_width)
        
        self.z_row.append(QVBoxLayout())
        self.z_big_step = CustomLineEdit("mm")
        self.z_big_step.setMaxLength(10)
        self.z_big_step.setPlaceholderText("0.1")
        self.z_big_step.setText("0.1")
        self.z_big_step.setMaximumWidth(self.max_lineedit_width)
        self.z_small_step = CustomLineEdit("mm")
        self.z_small_step.setMaxLength(10)
        self.z_small_step.setPlaceholderText("0.05")
        self.z_small_step.setText("0.05")
        self.z_small_step.setMaximumWidth(self.max_lineedit_width)
        self.z_row[2].addWidget(self.z_big_step)
        self.z_row[2].addWidget(self.z_small_step)
        
        
        self.z_row.append(QVBoxLayout())
        self.z_big_steps = QHBoxLayout()
        self.z_big_step_left   = QPushButton("- Z", self)
        self.z_big_step_right  = QPushButton("+ Z", self)
        self.z_big_step_right.setMinimumHeight(self.min_button_height)
        self.z_big_step_right.setMinimumWidth(self.min_step_button_width)
        self.z_big_step_left.setMinimumHeight(self.min_button_height)
        self.z_big_step_left.setMinimumWidth(self.min_step_button_width)
        self.z_big_steps.addWidget(self.z_big_step_left)
        self.z_big_steps.addWidget(self.z_big_step_right)
        self.z_row[3].addLayout(self.z_big_steps)
        self.z_small_steps = QHBoxLayout()
        self.z_small_step_left = QPushButton("- Z", self)
        self.z_small_step_right = QPushButton("+ Z", self)
        self.z_small_step_right.setMinimumHeight(self.min_button_height)
        self.z_small_step_right.setMinimumWidth(self.min_step_button_width)
        self.z_small_step_left.setMinimumHeight(self.min_button_height)
        self.z_small_step_left.setMinimumWidth(self.min_step_button_width)
        self.z_small_steps.addWidget(self.z_small_step_left)
        self.z_small_steps.addWidget(self.z_small_step_right)
        self.z_row[3].addLayout(self.z_small_steps)
        
        self.z_big_step_left.clicked.connect( lambda: self.commands.z_stepped_backward(self.z_row[1], self.z_big_step))
        self.z_big_step_right.clicked.connect(lambda: self.commands.z_stepped_forward(self.z_row[1], self.z_big_step))
        self.z_small_step_left.clicked.connect( lambda: self.commands.z_stepped_backward(self.z_row[1], self.z_small_step))
        self.z_small_step_right.clicked.connect(lambda: self.commands.z_stepped_forward(self.z_row[1], self.z_small_step))
        
        self.z_row.append(CustomLineEdit("mm"))
        self.z_row[4].setMaxLength(10)
        self.z_row[4].setPlaceholderText("coordinate")
        self.z_row[4].setMaximumWidth(self.max_lineedit_width)
        
        self.z_move_button = QPushButton("Move",self)
        self.z_move_button.setMinimumHeight(self.min_button_height)
        self.z_row.append(self.z_move_button)
        
        self.z_row[5].clicked.connect(lambda: commands.z_move_to(self.z_row[4], self.z_row[1])) 
        
        
        for i in range(len(self.z_row)):
            if i == 2 or i == 3:
                self.thorlabs_layout.addLayout(self.z_row[i], 3, i)
            else:
                self.thorlabs_layout.addWidget(self.z_row[i], 3, i)
        #           endregion

        #           Buttons row 4
        #           region
        self.thorlabs_buttons = QHBoxLayout()
        self.button_row    = []
        
        self.button_row.append(QPushButton("Enabled" ,self))
        self.button_row.append(QPushButton("Home"    ,self))
        
        self.button_row[0].setCheckable(True)
        self.button_row[0].setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                font-size: 14px;
                text-align: center;
            }
            QPushButton:checked {
                background-color: red;
                color: white;
                font-size: 14px;
                text-align: center;
            }
        """)
        
        self.button_row[1].setStyleSheet("background-color: red; color: white; font-size: 14px; text-align: center;")
        
        # Connecting to logic
        self.button_row[0].toggled.connect(lambda checked: self.commands.enable_toggle_all(self.button_row[0], checked))
        self.button_row[1].clicked.connect(lambda: self.commands.home_all(self.button_row[1], self.x_row[1], self.y_row[1], self.z_row[1]))
            
        self.thorlabs_layout.addWidget(self.button_row[0], 4, 0, 1, 3)
        self.thorlabs_layout.addWidget(self.button_row[1], 4, 3, 1, 3)
        
        #           endregion
        
        # endregion
        
        #   Prior
        #   region
        self.prior_layout = QVBoxLayout()
        self.prior_frame  = QFrame(self)
        self.prior_frame.setFrameShape(QFrame.Shape.Box)  # Set the frame shape
        self.prior_frame.setFrameShadow(QFrame.Shadow.Raised)  # Add a shadow effect
        self.prior_frame.setLayout(self.prior_layout)
        
        self.prior_label = QLabel("Prior")
        self.prior_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prior_label.setMaximumHeight(self.max_height_title_bar)
        self.prior_font = QFont()
        self.prior_font.setPointSize(self.title_fontsize)
        self.prior_font.setBold(True)
        self.prior_label.setFont(self.prior_font)
        
        self.toplevel_layout.addWidget(self.prior_label)
        self.toplevel_layout.addWidget(self.prior_frame)
        
        self.prior_layout.addWidget(priorGUI(self.prior_stage))
        
        
        #   endregion
        
        # endregion

        
        # Main Widget
        self.toplevel_widget = QWidget()
        self.toplevel_widget.setLayout(self.toplevel_layout)
        self.setCentralWidget(self.toplevel_widget)    
    
    # Functions