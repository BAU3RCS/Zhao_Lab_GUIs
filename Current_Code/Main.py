"""
Main Application File

Author: Brandon Bauer
Written January 2025

Updated XXXXXXXXXXXX
"""
from PyQt6.QtWidgets import QApplication
from UI.Stage_MainWindow import Stage_MainWindow
from  UI.Logic.Button_To_Device_logic import device_commands

import serial.tools.list_ports

from Controllers.KDC101 import Kcube
from Controllers.M30XY import M30XY
from Controllers.prior_driver import prior

import Settings.Serial_Numbers as SN

if __name__ == "__main__":

        
    # You need one (and only one) QApplication instance per application.
    app = QApplication([])

    # Creating our devices
    commands = device_commands(Kcube(SN.SN_KDC101,SN.Z_motor), M30XY(SN.SN_M30XY))
    #commands = device_commands(SN.SN_KDC101, SN.SN_M30XY, "port 3")

    # Create our main window defined in Stage_MainWindow and show the window
    window = Stage_MainWindow(commands, prior())
    window.show()  

    # Start the event loop. 
    app.exec()

    #TODO:
    # Fix disabled behavoir
    # Add error prevention for moving out of bounds
    # Change to micrometer
    # Might need to change how com ports are loaded.
    # Might reorganize prior stuff into gui, logic, etc