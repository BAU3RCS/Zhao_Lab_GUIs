"""
Created: Aug 19 2020
Updated: Jan 17 2025

@authors: Kaifei Kang, Brandon Bauer

""" 
import sys
import clr
import time

clr.AddReference("System")
import System

sys.path.append(r"DLLs\Thorlabs")

clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.DCServoCLI")
clr.AddReference("ThorLabs.MotionControl.GenericMotorCLI")

# Further informatom under Classes: Thorlabs > MotionControl > kcube > DCServoCLI > KCubeDCServo
# Click List of All Members !!

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.KCube.DCServoCLI import *
# This is where the MotorDirection Enum is stored!!!
from Thorlabs.MotionControl.GenericMotorCLI  import*

class Kcube():
    def __init__(self, serial_number, motor):
        # Build device list to access controller
        try:
            DeviceManagerCLI.BuildDeviceList()
        except Exception as error:
            sys.exit(error)
        
        # Create and set variables
        self.ser        = serial_number
        self.motor      = motor
        self.controller = KCubeDCServo.CreateKCubeDCServo(self.ser)
        
        # Note: We might not immediately want to connect to the device.... ?
        self.connect()
 
    def connect(self):
        """
        This connects to the controller via its serial number and configures it to work with the given motor.
        Inputs: None.
        Outputs: None.
        """
        # Start the connection with the controller and wait for it to initialize.
        self.controller.Connect(self.ser)
        if not self.controller.IsSettingsInitialized():
                try:
                    self.controller.WaitForSettingsInitialized(100)
                    
                except Exception as error:
                    sys.exit(error)
                    
        # Polls the device every 250ms for status
        self.controller.StartPolling(250)
        # Wait 500ms to gaurentee first update is recieved
        time.sleep(0.5)
        
        # Enables device, otherwise commands are ignored
        self.controller.EnableDevice()
        time.sleep(0.5)
        
        # Call LoadMotorConfiguration on the device to initialize the DeviceUnitConverter object required for real world unit parameters
        # loads configuration information into channel
        motorConfiguration = self.controller.LoadMotorConfiguration(self.ser)
        motorConfiguration.DeviceSettingsName = self.motor

        # Get the device unit converter
        motorConfiguration.UpdateCurrentConfiguration() 
    
    def home(self, timeout):
        """
        This homes the controller and will error if the controller does not complete homing within the given time limit (in miliseconds).
        Inputs: Timeout in ms.
        Outputs: None.
        """
        try:
            self.controller.Home(timeout)
        except Exception as error:
            sys.exit(error)
        
    def enable(self):
        """
        Enables the controller to respond to commands.
        Input: None
        Output: None
        """
        try:
            self.controller.EnableDevice()
            # Wait for device to be ready for command
            time.sleep(0.5)
            
        except Exception as error:
            sys.exit(error)
            
    def disable(self):
        """
        Disables the controller. The controller will not respond to commands.
        Input: None
        Output: None
        """
        try:
            self.controller.DisableDevice()
        except Exception as error:
            sys.exit(error)
    
    def jog(self, direction, timeout):
        """
        This jogs the controller in the forward direction, and will error if not completed within the user
        specified timeout in miliseconds.
        Input: Direction ("Forward", "Backward") and timeout in miliseconds.
        Output: The position after command.
        """
        try:
            if direction == "Forward":
                self.controller.MoveJog(MotorDirection.Forward, timeout)
            elif direction == "Backward":
                self.controller.MoveJog(MotorDirection.Backward, timeout)
            else:
                raise Exception("Direction not defined")
            
        except Exception as error:
            sys.exit(error)
            
        return self.get_pos() 
    
    def move_continuous(self,direction):
        """
        Continuously jogs the motor in given direction.
        Input: Direction ("Forward", "Backward").
        Output: The position after command.
        """
        try:
            if direction == "Forward":
                self.controller.MoveContinuous(MotorDirection.Forward)
            elif direction == "Backward":
                self.controller.MoveContinuous(MotorDirection.Backward)
            else:
                raise Exception("Direction not defined")
            
        except Exception as error:
            sys.exit(error)
        
        return self.get_pos()
    
    def move_to(self, position, timeout):
        """
        This moves the controller to the specific target position relative to home in milimeters.
        The move must be compeleted in the timeout specified, which is in miliseconds.
        Input: The position to move to in milimeters, timeout in ms.
        Ouput: The position after.
        """
    
        try:
            self.controller.MoveTo(System.Decimal(position),timeout)
        except Exception as error:
            sys.exit(error)
        
        return self.get_pos()
    
    def set_velocity_params(self, max_velocity = 2.2, acceleration = 1.5):  
        """
        This sets the motors velocity parameters. Defaulted to company startup values, 2.2 mm/s and 1.5 mm/s^2 respectively.
        Input: Velocity in mm/s and Acceleration in  mm/s^2.
        Output: None.
        """
        acceleration = System.Decimal(acceleration)
        max_velocity = System.Decimal(max_velocity)

        self.controller.SetVelocityParams(max_velocity, acceleration)
    
    def get_velocity_params(self):
        """
        Returns the velocicty parameters max_velocity in mm/s and accleration in mm/s^2 in a tuple
        Input: None.
        Output: A tuple containing max_velocity in mm/s and acceleration in mm/s^2.
        """
        params           = self.controller.GetVelocityParams()
        max_velocity     = float(str(params.MaxVelocity))
        acceleration     = float(str(params.Acceleration))
        
        return (max_velocity, acceleration)
    
    def set_jog_velocity_params(self, step_size = 0.1 ,max_velocity = 2, acceleration = 2):
        """
        Sets the jog parameters of the controller/motor.
        Defaulted to company startup values of 0.1 milimeters, 2 mm/s, and 2 mm/s^2 respectively.
        Input: Step size in milimeters, max velocity in mm/s, and acceleration in mm/s^2.
        Output: None.
        """
        max_velocity  = System.Decimal(max_velocity)
        acceleration  = System.Decimal(acceleration)
        step_size     = System.Decimal(step_size)
        
        self.controller.SetJogStepSize(step_size)
        self.controller.SetJogVelocityParams(max_velocity, acceleration)

    def get_jog_params(self):
        """
        Returns the jog parameters: step size in mm, max velocity in mm/s, and acceleration in mm/s^2 as a tuple.
        Input: None.
        Output: A tuple containing step_size in mm, max_velocity in mm/s, acceleration in mm/s^2.
        """
        step_size        = float(str(self.controller.GetJogStepSize()))
        
        params           = self.controller.GetJogParams().VelocityParams
        max_velocity     = float(str(params.MaxVelocity))
        acceleration     = float(str(params.Acceleration))
    
        return (step_size, max_velocity, acceleration)

    def set_backlash(self, backlash = 0.3):
        """
        This sets the back lash of the controller/motor. Defaulted to the company startup value of 0.3 milimeters.
        Input: Backlash in milimeters
        Output: None.
        """
        backlash = System.Decimal(backlash)
        
        self.controller.SetBacklash(backlash)

    def get_backlash(self):
        """
        Returns the backlash of the motor/controller in milimeters.
        Input: None.
        Output: Backlash in mm.
        """
        backlash = float(str(self.controller.GetBacklash()))

        return backlash
    
    def get_pos(self):
        """
        Returns the position of the motor in milimeters.
        Input: None
        Output: Position of the motor in milimeters.
        """
        return float(str(self.controller.Position))
        
    def get_state(self):
        """
        Returns the state of the controller/motor.
        Input: None.
        Output: State of controller/motor.
        """
        return self.controller.State

    def disconnect(self):
        """
        Properly disconnects and shutsdown the controller/motor.
        Input: None.
        Ouutput: None.
        """
        self.controller.DisconnectTidyUp()
        self.controller.ShutDown()
