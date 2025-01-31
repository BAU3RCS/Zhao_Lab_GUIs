"""
Created: Aug 19 2020
Updated: Jan 2025

@authors: Kaifei Kang, Brandon Bauer

""" 

import sys
import clr
import time

clr.AddReference("System")
import System # type: ignore

sys.path.append(r"DLLs\Thorlabs")

clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("ThorLabs.MotionControl.Benchtop.DCServoCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")

# Further informatom under Classes: Thorlabs > MotionControl > Benchtop > DCServoCLI > IntegratedXYStageChannel
# Click List of All Members !! 
# Note that we must do things by channel here. Ie. I do not think we can call a command that will work on both motors... which
# doesn't make sense in many situations anyways.

from Thorlabs.MotionControl.DeviceManagerCLI import * # type: ignore
from Thorlabs.MotionControl.Benchtop.DCServoCLI import * # type: ignore
from Thorlabs.MotionControl.GenericMotorCLI import * # type: ignore


class M30XY():
    def __init__(self,serial_number):
        # Build device list to access controller
        try:
            DeviceManagerCLI.BuildDeviceList() # type: ignore
        except Exception as error:
            sys.exit(error)
        
        # Create and set variables
        self.ser   = serial_number
        self.mx    = None
        self.my    = None
        self.stage = BenchtopDCServo.CreateBenchtopDCServo(self.ser) # type: ignore
        
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
            self.channels["x"] = self.stage.GetChannel(1)
        except Exception as error:
            sys.exit(error)
            
        try:
            self.channels["y"] = self.stage.GetChannel(2)
        except Exception as error:
            sys.exit(error)
        
        self._initialize_channel(self.channels["x"])
        self._initialize_channel(self.channels["y"])
        
    def _initialize_channel(self, channel):
        """
        Connects to a specific channel or motor on the stage and initilizes settings etc.
        Input: Channel object to be initialized.
        Output: None.
        """    
        # Wait for channel to initialize settings
        if not channel.IsSettingsInitialized():
                try:
                    channel.WaitForSettingsInitialized(100)
                    
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
        Inputs: Channel("x", "y"), Timeout in ms.
        Outputs: None.
        """
        try:
            self.channels[channel].Home(timeout)
        except Exception as error:
            sys.exit(error)
            
    def is_enabled(self, channel):
        """
        Enables the controller to respond to commands.
        Input: Channel ("x", "y")
        Output: Returns true if enabled and flase if disabled.
        """
        return self.channels[channel].IsEnabled()

    def enable(self, channel):
        """
        Enables the stage to respond to commands.
        Input: Channel ("x", "y")
        Output: None
        """
        try:
            self.channels[channel].EnableDevice()
            # Wait for device to be ready for command
            time.sleep(0.5)
            
        except Exception as error:
            sys.exit(error)
    
    def disable(self, channel):
        """
        Disables the controller. The controller will not respond to commands.
        Input: Channel to be disabled ("x", "y")
        Output: None
        """
        try:
            self.channels[channel].DisableDevice()
        except Exception as error:
            sys.exit(error)
    
    
    def jog(self, channel, direction, timeout):
        """
        This jogs the channel motor in the forward direction, and will error if not completed within the user
        specified timeout in miliseconds.
        Input: Channel ("x", "y"), direction ("Forward", "Backward") and timeout in miliseconds.
        Output: The position after command.
        """
        try:
            if direction == "Forward":
                self.channels[channel].MoveJog(MotorDirection.Forward, timeout) # type: ignore
            elif direction == "Backward":
                self.channels[channel].MoveJog(MotorDirection.Backward, timeout) # type: ignore
            else:
                raise Exception("Direction not defined")
            
        except Exception as error:
            sys.exit(error)
            
        return self.get_pos(channel) 
    
    def move_continuous(self, channel, direction):
        """
        Continuously jogs the channel motor in given direction.
        Input: Channel ("x", "y"), direction ("Forward", "Backward").
        Output: The position after command.
        """
        try:
            if direction == "Forward":
                self.channels[channel].MoveContinuous(MotorDirection.Forward) # type: ignore
            elif direction == "Backward":
                self.channels[channel].MoveContinuous(MotorDirection.Backward) # type: ignore
            else:
                raise Exception("Direction not defined")
            
        except Exception as error:
            sys.exit(error)
        
        return self.get_pos(channel)
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
            
        return self.get_pos(channel)
   
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
        
        return self.get_pos(channel)
    
    def set_velocity_params(self, channel,max_velocity = 2.3, acceleration = 5.0):
        """
        This sets the motors velocity parameters. Defaulted to company startup values, 2.3 mm/s and 5.0 mm/s^2 respectively.
        Input: Channel ("x", "y"),velocity in mm/s, acceleration in  mm/s^2.
        Output: None.
        """
        acceleration = System.Decimal(acceleration)
        max_velocity = System.Decimal(max_velocity)

        self.channels[channel].SetVelocityParams(max_velocity, acceleration)
        
    def get_velocity_params(self, channel):
        """
        Returns the velocicty parameters max_velocity in mm/s and accleration in mm/s^2 in a tuple
        Input: Channel ("x", "y").
        Output: A tuple containing max_velocity in mm/s and acceleration in mm/s^2.
        """
        params           = self.channels[channel].GetVelocityParams()
        max_velocity     = float(str(params.MaxVelocity))
        acceleration     = float(str(params.Acceleration))
    
        return (max_velocity, acceleration)

    def set_jog_velocity_params(self, channel, step_size = 0.5, max_velocity = 2.6, acceleration = 4.0):
        """
        Sets the jog parameters (step size, max velocity, acceleration) of the controller/motor.
        Defaulted to company startup values of 0.5 milimeters, 2.6 mm/s, and 4.0 mm/s^2 respectively.
        Input: Channel ("x", "y"), step size in milimeters, max velocity in mm/s, and acceleration in mm/s^2.
        Output: None.
        """
        max_velocity  = System.Decimal(max_velocity)
        acceleration  = System.Decimal(acceleration)
        step_size = System.Decimal(step_size) 
        
        self.channels[channel].SetJogStepSize(step_size)
        self.channels[channel].SetJogVelocityParams(max_velocity, acceleration)
        
    def get_jog_params(self, channel):
        """
        Returns the jog parameters: step size in mm, max velocity in mm/s, and acceleration in mm/s^2 as a tuple.
        Input: Channel ("x", "y").
        Output: A tuple containing step_size in mm, max_velocity in mm/s, acceleration in mm/s^2.
        """
        step_size        = float(str(self.channels[channel].GetJogStepSize()))
        
        params           = self.channels[channel].GetJogParams().VelocityParams
        max_velocity     = float(str(params.MaxVelocity))
        acceleration     = float(str(params.Acceleration))
    
        return (step_size, max_velocity, acceleration)
        
    def set_backlash(self, channel, backlash = 0):
        """
        This sets the back lash of the controller/motor. Defaulted to the company startup value of 0.3 milimeters.
        Input: channel ("x", "y") and backlash in milimeters.
        Output: None.
        """
        backlash = System.Decimal(backlash)
        
        self.channels[channel].SetBacklash(backlash)

    def get_backlash(self, channel):
        """
        Returns the backlash of the given channel in milimeters.
        Input: Channel ("x", "y").
        Output: Backlash in mm.
        """
        backlash = float(str(self.channels[channel].GetBacklash()))
    
        return backlash

    def get_pos(self, channel):
        """
        Returns the position of the motor in milimeters.
        Input: Channel ("x", "y").
        Output: Position of the motor in milimeters.
        """
        
        return float(str(self.channels[channel].Position))
        
    def get_state(self, channel):
        """
        Returns the state of the controller/motor.
        Input: Channel ("x", "y").
        Output: State of controller/motor.
        """
        return self.channels[channel].State

    def disconnect(self, channel):
        """
        Properly disconnects and shutsdown the controller/motor.
        Input: Channel ("x", "y").
        Ouutput: None.
        """
        self.channels[channel].DisconnectTidyUp()
        self.channels[channel].ShutDown()
