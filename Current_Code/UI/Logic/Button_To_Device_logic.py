"""
Methods used to control aspects of the Main UI

Author: Brandon Bauer
Written January 2025

Updated XXXXXXXXXXXX
"""

"""
Brandon:
Now lets be honest with each other, this code probably won't ever change and if it does.... not much.
It could evolve and I've considered that in the layout, but I figure the frameworks being used will not since
equipment is expensive etc. and if its commented and it works well, why would we change or update unless forced.... (oh Bob save me).
Considering this and the time restraints in making a working file, this file will be marrying the GUI framework b/c
implementing abstract classes at this point in time is a bit overkill.

At somepoint in time I wish to comeback through this file and and several others to tidy up and create actual boundaries....
I hope future me is not too upset with myself right now and this ode is never sung by another. Good luck out there
"""
from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit

from Controllers.KDC101 import Kcube
from Controllers.M30XY import M30XY
# to be implemented later when the codes combine
#from Controllers.prior_driver import prior


class device_commands():
    """
    This class stitches together UI commands
    """
    # minute in miliseconds
    minute = 60_000
    
    def __init__(self, KDC:Kcube, M30XY:M30XY, Prior):
        """
        """
        self.KDC   = KDC
        self.M30XY = M30XY
        self.Prior = Prior
        
#   Thorlabs
#   region


#       Set Step Size
#       region
    def x_set_step_size(self, lineedit:QLineEdit):
        self.M30XY.set_jog_velocity_params("x", step_size = float(lineedit.text))
    
    def y_set_step_size(self, lineedit:QLineEdit):
        self.M30XY.set_jog_velocity_params("y", step_size = float(lineedit.text))
        
    """
    This is now just a helper function for the step buttons in 
    """
    def z_set_step_size(self, lineedit:QLineEdit):
        self.KDC.set_jog_velocity_params(step_size = float(lineedit.text))
    
#       endregion
    
#       Step Buttons
#       region
    def x_stepped_Forward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("x", "Forward", self.minute))+" mm")
         
    def x_stepped_backward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("x", "Backward", self.minute))+" mm")

    def y_stepped_Forward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("y", "Forward", self.minute))+" mm")
         
    def y_stepped_backward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("y", "Backward", self.minute))+" mm")

    """
    Since we have two step sizes we must get the step size as we step unlike in the x and y directions
    """
    def z_stepped_Forward(self, label:QLabel, lineedit:QLineEdit):
        self.z_set_step_size(lineedit)
        label.setText(str(self.KDC.jog("Forward", self.minute))+" mm")
         
    def z_stepped_backward(self, label:QLabel, lineedit:QLineEdit):
        self.z_set_step_size(lineedit)
        label.setText(str(self.KDC.jog("Backward", self.minute))+" mm")

#       endregion

#       Move To Buttons
#       region
    def x_move_to(self, lineedit:QLineEdit, label:QLabel):
        new_pos = self.M30XY.move_to("x", float(lineedit.text), self.minute)
    
    def y_move_to(self, lineedit:QLineEdit, label:QLabel):
        new_pos = self.M30XY.move_to("y", float(lineedit.text), self.minute)
        
    def z_move_to(self, lineedit:QLineEdit, label:QLabel):
         new_pos = self.KDC.move_to(float(lineedit.text), self.minute)

#       endregion

#       Bottom Buttons
#       region
    def home_all(self, button:QPushButton):
        self.M30XY.home("x", self.minute)
        self.M30XY.home("y", self.minute)
        self.KDC.home(self.minute)
        
        button.setText("Homed")
        button.setStyleSheet("background-color: green; color: white; font-size: 14px; text-align: center;")

    def enable_toggle_all(self, button:QPushButton):
        if button.isChecked:
            self.M30XY.enable("x")
            self.M30XY.enable("y")
            self.KDC.enable()
            
            button.setText("Enabled")
            button.setStyleSheet("background-color: green; color: white; font-size: 14px; text-align: center;")
        else: 
            self.M30XY.disable("x")
            self.M30XY.disable("y")
            self.KDC.disable()
            
            button.setText("Disabled")
            button.setStyleSheet("background-color: red; color: white; font-size: 14px; text-align: center;")
            
        
#       endregion

#   endregion

#   Prior
#   region

#   endregion

