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
    
    """
    In this file the thorlabs default units are mm, so instead of changing the default units I convert between
    µm and mm in the logic here. If someone in the future wants to change velocity or accelertation,
    keep in mind the need to possibly change units depending on the planed UI etc. Potentially one could implement
    a function that allows you to automatically switch and change units. I do not have time for this now.
    """
    
    # µm to mm
    um_to_mm_factor = 1e-3
    
    # mm to µm
    mm_to_um_factor = 1e3
    
    units = "µm"
    
    def __init__(self, KDC:Kcube, M30XY:M30XY):
        """
        """
        self.KDC   = KDC
        self.M30XY = M30XY
        
#   Thorlabs
#   region

#       Get Position
#       region
    def x_get_pos(self):
        return self.M30XY.get_pos("x") * self.mm_to_um_factor
        
    def y_get_pos(self):
        return self.M30XY.get_pos("y") * self.mm_to_um_factor
        
    def z_get_pos(self):
        return self.KDC.get_pos() * self.mm_to_um_factor
        
#       endregion

#       Set Step Size
#       region
    def x_set_step_size(self, lineedit:QLineEdit):
        self.M30XY.set_jog_velocity_params("x", step_size = float(lineedit.text()) * self.um_to_mm_factor)
    
    def y_set_step_size(self, lineedit:QLineEdit):
        self.M30XY.set_jog_velocity_params("y", step_size = float(lineedit.text()) * self.um_to_mm_factor)
        
    """
    This is now just a helper function for the step buttons in 
    """
    def z_set_step_size(self, lineedit:QLineEdit):
        self.KDC.set_jog_velocity_params(step_size = float(lineedit.text() * self.um_to_mm_factor))
    
#       endregion
    
#       Step Buttons
#       region
    def x_stepped_forward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("x", "Forward", self.minute))+" "+self.units)
         
    def x_stepped_backward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("x", "Backward", self.minute))+" "+self.units)

    def y_stepped_forward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("y", "Forward", self.minute))+" "+self.units)
         
    def y_stepped_backward(self, label:QLabel):
        label.setText(str(self.M30XY.jog("y", "Backward", self.minute))+" "+self.units)

    """
    Since we have two step sizes we must get the step size as we step unlike in the x and y directions
    """
    def z_stepped_forward(self, label:QLabel, lineedit:QLineEdit):
        self.z_set_step_size(lineedit)
        label.setText(str(self.KDC.jog("Forward", self.minute))+" "+self.units)
         
    def z_stepped_backward(self, label:QLabel, lineedit:QLineEdit):
        self.z_set_step_size(lineedit)
        label.setText(str(self.KDC.jog("Backward", self.minute))+" "+self.units)

#       endregion

#       Move To Buttons
#       region
    def x_move_to(self, lineedit:QLineEdit, label:QLabel):
        new_pos = self.M30XY.move_to("x", float(lineedit.text()) * self.um_to_mm_factor, self.minute)
        label.setText(str(new_pos)+" "+self.units)
    
    def y_move_to(self, lineedit:QLineEdit, label:QLabel):
        new_pos = self.M30XY.move_to("y", float(lineedit.text()) * self.um_to_mm_factor, self.minute)
        label.setText(str(new_pos)+" "+self.units)
        
    def z_move_to(self, lineedit:QLineEdit, label:QLabel):
         new_pos = self.KDC.move_to(float(lineedit.text()) * self.um_to_mm_factor, self.minute)
         label.setText(str(new_pos)+" "+self.units)

#       endregion

#       Bottom Buttons
#       region
    def home_all(self, button:QPushButton, X_label:QLabel, y_label:QLabel, z_label:QLabel):
        self.M30XY.home("x", self.minute)
        X_label.setText(str(self.x_get_pos())+" "+self.units)
        
        self.M30XY.home("y", self.minute)
        y_label.setText(str(self.y_get_pos())+" "+self.units)
        
        self.KDC.home(self.minute)
        z_label.setText(str(self.z_get_pos())+" "+self.units)
        
        button.setText("Homed")
        button.setStyleSheet("background-color: green; color: white; font-size: 14px; text-align: center;")

    def enable_toggle_all(self, button:QPushButton, checked):
        if not checked:
            self.M30XY.enable("x")
            self.M30XY.enable("y")
            self.KDC.enable()
            
            button.setText("Enabled")

        else: 
            self.M30XY.disable("x")
            self.M30XY.disable("y")
            self.KDC.disable()
            
            button.setText("Disabled")
            
        
#       endregion

#   endregion

#   Prior
#   region

#   endregion

