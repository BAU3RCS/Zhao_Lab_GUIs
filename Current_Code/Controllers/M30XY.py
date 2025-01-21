"""
Created on Wed Aug 19 02:42:31 2020

@author: Kaifei Kang


"""

import sys
import clr
import time

clr.AddReference("System")
import System

sys.path.append(r"DLLs\Thorlabs")

clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("ThorLabs.MotionControl.Benchtop.DCServoCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")

# Further informatom under Classes: Thorlabs > MotionControl > Benchtop > DCServoCLI > IntegratedXYStageChannel
# Click List of All Members !! 
# Note that we must do things by channel here. Ie. I do not think we can call a command that will work on both motors... which
# doesn't make sense in many situations anyways.

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.Benchtop.DCServoCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *


class M30XY():
    def __init__(self,serial_number):
        # Build device list to access controller
        try:
            DeviceManagerCLI.BuildDeviceList()
        except Exception as error:
            sys.exit(error)
        
        # Create and set variables
        self.ser   = serial_number
        self.mx    = None
        self.my    = None
        self.stage = BenchtopDCServo.CreateBenchtopDCServo(self.ser)
        
        # This allows us to just use keys to reference the channels later instead of needing the channel object
        # outside of the class.
        self.channels = {
            "x"  : self.mx,
            "y"  : self.my,
            "xy" : self.stage
        }
        
        # Note: we might not immediately want to connect the device?
        self.connect()
        
    def connect(self):
        """
        Connects to stage and initializes the stage channels.
        Input: None.
        Output: None.
        """
        
        # Connect to the stage
        try:
            self.stage.Connect(self.ser)
        except Exception as error:
            sys.exit(error)
        
        # Channels correspond to a specific motion direction or motor controller
        # Here we have x and y.
        try:
            self.mx = self.stage.GetChannel(1)
        except Exception as error:
            sys.exit(error)
            
        try:
            self.my = self.stage.GetChannel(2)
        except Exception as error:
            sys.exit(error)
        
        self._initialize_channel(self.mx)
        self._initialize_channel(self.my)
        
    def _initialize_channel(self, channel):
        """
        Connects to a specific channel or motor on the stage and initilizes settings etc.
        Input: Channel object to be initialized.
        Output: None.
        """    
        # Wait for channel to initialize settings
        if not channel.IsSettingsInitialized():
                try:
                    self.controller.WaitForSettingsInitialized(100)
                    
                except Exception as error:
                    sys.exit(error)
        
        # Polls the device every 250ms for status
        channel.StartPolling(250)
        # Wait 500ms to gaurentee first update is recieved
        time.sleep(0.5)
        
        # Enables device, otherwise commands are ignored
        channel.EnableDevice()
        time.sleep(0.5)
        
        # Call LoadMotorConfiguration on the device to initialize the DeviceUnitConverter object required for real world unit parameters
        # - loads configuration information into channel
        # Use the channel.DeviceID "79xxxxxx-1" to get the channel 1 settings. This is different to the serial number
        motorConfiguration = channel.LoadMotorConfiguration(channel.DeviceID)

    def home(self, channel, timeout):
        """
        This homes the controller and will error if the controller does not complete homing within the given time limit (in miliseconds).
        Inputs: Channel("x", "y", "xy"), Timeout in ms.
        Outputs: None.
        """
        try:
            self.channels[channel].Home(timeout)
        except Exception as error:
            sys.exit(error)

    # TODO: Can you enable and disable the whole stage?
    def enable(self, channel):
        """
        Enables the stage to respond to commands.
        Input: Channel ("x", "y", "xy")
        Output: None
        """
        try:
            self.channels[channel].EnableDevice()
        except Exception as error:
            sys.exit(error)
    
    def disable(self, channel):
        """
        Disables the controller. The controller will not respond to commands.
        Input: Channel to be disabled ("x", "y", "xy")
        Output: None
        """
        try:
            channel.DisableDevice()
        except Exception as error:
            sys.exit(error)
    
    def jog_forward(self, channel, timeout):
        """
        This jogs the controller in the forward direction, and will error if not completed within the user
        specified timeout in miliseconds.
        Input: Channel ("x", "y"), timeout in miliseconds.
        Output: The position after command.
        """
        try:
            self.channels[channel].MoveJog(MotorDirection.Forward,timeout)
        except Exception as error:
            sys.exit(error)
            
        return self.pos()
    
    def jog_backward(self, channel, timeout):
        """
        This jogs the controller in the backward direction, and will error if not completed within the user
        specified timeout in miliseconds.
        Input: Channel ("x", "y"), timeout in miliseconds.
        Output: The position after command.
        """
        try:
            self.channels[channel].MoveJog(MotorDirection.Backward,timeout)
        except Exception as error:
            sys.exit(error)
            
        return self.pos()
   
    def move_to(self, channel, position, timeout):
        """
        This moves the controller to the specific target position relative to home in milimeters.
        The move must be compeleted in the timeout specified, which is in miliseconds.
        Input: Channel ("x", "y"), the position to move to in milimeters, timeout in ms.
        Ouput: The position after.
        """
    
        try:
            self.channels[channel].MoveTo(System.Decimal(position),timeout)
        except Exception as error:
            sys.exit(error)
        
        return self.pos()
    
    #TODO: Check the max velocity parm defaults
    # See if the command is per channel or stage
    def set_velocity_params(self, channel,max_velocity = 2.2, acceleration = 1.5):
        """
        This sets the motors velocity parameters. Defaulted to company startup values, 2.2 mm/s and 1.5 mm/s^2 respectively.
        Input: Channel ("x", "y", "xy"),velocity in mm/s, acceleration in  mm/s^2.
        Output: None.
        """
        acceleration = System.Decimal(acceleration)
        max_velocity = System.Decimal(max_velocity)

        self.channels[channel].SetVelocityParams(max_velocity, acceleration)

    def set_jog_velocity_params(self, channel, max_velocity = 2, acceleration = 2):
        """
        Sets the jog parameters of the controller/motor. Defaulted to company startup values of 2 mm/s and 2 mm/s^2 respectively.
        Input: Channel ("x", "y", "xy"), max velocity in mm/s, and acceleration in mm/s^2.
        Output: None.
        """
        max_velocity  = System.Decimal(max_velocity)
        acceleration  = System.Decimal(acceleration)
        
        self.channels[channel].SetJogVelocityParams(max_velocity, acceleration)

    def set_jog_step(self, channel, step_size = 0.1):
        """
        Sets the jog step size of the controller/motor. Defaulted to the company startup value of 0.1 milimeters.
        Input: Channel ("x", "y", "xy"), Step size in milimeters.
        Output: None.
        """
        step_size = System.Decimal(step_size) 
        
        self.channels[channel].SetJogStepSize(step_size)
        
    def set_backlash(self, channel, backlash = 0.3):
        """
        This sets the back lash of the controller/motor. Defaulted to the company startup value of 0.3 milimeters.
        Input: channel ("x", "y", "xy") and backlash in milimeters.
        Output: None.
        """
        backlash = System.Decimal(backlash)
        
        self.channels[channel].SetBacklash(backlash)

    def get_pos(self, channel):
        """
        Returns the position of the motor in milimeters.
        Input: Channel ("x", "y", "xy").
        Output: Position of the motor in milimeters.
        """
        
        return float(self.channels[channel].Position)
        
    def get_state(self, channel):
        """
        Returns the state of the controller/motor.
        Input: Channel ("x", "y", "xy").
        Output: State of controller/motor.
        """
        return self.channels[channel].State

    #TODO: Check how things work with channels I'm guessing just one
    def get_jog_params(self, channel):
        """
        Returns the jog parameters: step size in mm, max velocity in mm/s, and acceleration in mm/s^2 as a tuple.
        Input: Channel ("x", "y", "xy").
        Output: A tuple containing step_size in mm, max_velocity in mm/s, acceleration in mm/s^2.
        """
        step_size        = self.channels[channel].GetJogStepSize()
        max_velocity     = self.channels[channel].GetJogVelocityParams()[0]
        acceleration     = self.channels[channel].GetJogVelocityParams()[1]
    
        return (step_size, max_velocity, acceleration)
    
    def get_vel_params(self, channel):
        """
        Returns the velocicty parameters max_velocity in mm/s and accleration in mm/s^2 in a tuple
        Input: Channel ("x", "y", "xy").
        Output: A tuple containing max_velocity in mm/s and acceleration in mm/s^2.
        """
        return self.channels[channel].GetVelocityParams()

    def disconnect(self, channel):
        """
        Properly disconnects and shutsdown the controller/motor.
        Input: Channel ("x", "y", "xy").
        Ouutput: None.
        """
        self.channels[channel].DisconnectTidyUp()
        self.channels[channel].ShutDown()
