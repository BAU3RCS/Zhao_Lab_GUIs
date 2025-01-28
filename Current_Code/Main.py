"""
Main Application File

Author: Brandon Bauer
Written January 2025

Updated XXXXXXXXXXXX
"""
from PyQt6.QtWidgets import QApplication
from UI.Stage_MainWindow import Stage_MainWindow
from  UI.Logic.Button_To_Device_logic import device_commands

from Controllers.KDC101 import Kcube
from Controllers.M30XY import M30XY
# to be implemented later when the codes combine
#from Controllers.prior_driver import prior

import Settings.Serial_Numbers as SN

# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)
# app = QApplication([])

# Creating our devices
commands = device_commands(Kcube(SN.SN_KDC101,SN.Z_motor), M30XY(SN.SN_M30XY), "port 3")
#commands = device_commands(SN.SN_KDC101, SN.SN_M30XY, "port 3")

# Create our main window defined in Stage_MainWindow and show the window
window = Stage_MainWindow(commands)
window.show()  

# Start the event loop. 
app.exec()

#TODO:
# Fix disabled behavoir
# Add error prevention for moving out of bounds
# Change to micrometer