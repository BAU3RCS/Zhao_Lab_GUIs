"""
Created: Aug 19 2020
Updated: Jan XX 2025

@authors: Kaifei Kang, Brandon Bauer

""" 

import sys
import clr
import numpy as np

#TODO: Change to stored DLLs so we do not need Kinesis installed
sys.path.append(r"..\DLLs\Thorlabs")

clr.AddReference("System")
clr.AddReference("Thorlabs.MotionControl.KCube.DCServoCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")

#TODO: Don't think I need this
#clr.AddReference("Thorlabs.MotionControl.KCube.DCServoUI")


# Further informatom under Classes: Thorlabs > MotionControl > kcube > DCServoCLI > KCubeDCServo
# Click List of All Members !!

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.KCube.DCServoCLI import *

# This is where the MotorDirection Enum is stored!!!
from Thorlabs.MotionControl.GenericMotorCLI  import*

#TODO: Need to see if this is needed, TEST IT
#from Thorlabs.MotionControl.KCube.DCServoUI import *

import System

#TODO: fix try-except blocks for proper behavoir

class Motor():
    
    #TODO: Need to fix and setup device initilization properly, follow example in documentation
    def __init__(self,ser):
        DeviceManagerCLI.BuildDeviceList()
        
        # This should not be needed but I'm not quite sure yet so I'm leaving this
        #DeviceManagerCLI.GetDeviceList()
        
        self.ser   = ser
        self.motor = KCubeDCServo.CreateKCubeDCServo(self.ser)
        self.polling_time = 250
        self.connect()
 
    def connect(self):
        
        self.motor.Connect(self.ser)
        self.motor.WaitForSettingsInitialized(50000)
        self.motor.GetMotorConfiguration(self.ser,DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        self.motor.StartPolling(self.polling_time)
        self.motor.EnableDevice()
        
        #TODO: Remove and add this settings to the proper spot
#        self.set_jog_params()
#        self.set_vel_params()
#        self.set_jog_step(0.001)
        
    
    
    def home(self,time_limit):
        """
        This home the motor and will error if the motor does not complete homing within the given time limit (in miliseconds).
        """
        self.motor.Home(time_limit)
        
    def jog_forward(self,timeout):
        """
        This jogs the motor in the forward, and will error if not completed within the user
        specified timeout in miliseconds.
        Input: timeout(ms)
        Return: position after running.
        """
        try:
            self.motor.MoveJog(MotorDirection.Forward,timeout)
            return self.pos()
        except Exception as error:
            print(error)
            
    
    def jog_backward(self,timeout):
        """
        This jogs the motor in the forward, and will error if not completed within the user
        specified timeout in miliseconds. 
        Input: timeout(ms)
        Return: position after running.
        """
        try:
            self.motor.MoveJog(MotionDirection.Backward,timeout)
            return self.pos()      
        except Exception as error:
            print(error)
    
    def move_to(self,target,timeout):
        """
        This moves the motor to the specific target position relative to home in milimeters.
        The move must be compeleted in time_limit, which is in miliseconds.
        """
        
        # Why is this being done? I think this needs to be a parameter to allow the time to complete properly
        # timewait=self.polling_time
        print(target)
        try:
            self.motor.MoveTo(System.Decimal(target),time_limit)
        except Exception as error:
            print(error)
        
        return self.pos()
    
    def set_vel_params(self, acc = 1, maxv = 10):
        
        acc=System.Decimal(acc)
        maxv=System.Decimal(maxv)

        self.motor.SetVelocityParams(acc, maxv)
    
    def set_jog_params(self,vel=0.1,accl=1,stp_mode=1):
        
        vel=System.Decimal(vel)
        accl=System.Decimal(accl)
        new_pa=self.motor.GetJogParams()
        new_pa.StopMode= 1
        self.motor.SetJogParams(new_pa)
        self.motor.SetJogVelocityParams(vel,accl)

    def set_jog_step(self,step):
        step=((step)*1)
        print(step)
	
        return self.motor.SetJogStepSize(System.Decimal(step))

    def set_backlash(self,lash):
        self.motor.SetBacklash(System.Decimal(lash))

    def pos(self):
        return float(str(self.motor.Position))
        
    def motor_state(self):
        state=self.motor.State
        return state

    def get_jog_params(self):
        
        vel=self.motor.GetJogVelocityParams()[0]
        accl=self.motor.GetJogVelocityParams()[1]
        stop_mode=self.motor.GetJogParams().StopMode
        return(vel,accl,stop_mode)
    
    def get_vel_params(self):
        return self.motor.GetVelocityParams()

    def disconnect(self):
        self.motor.ShutDown()
        
    def callables(self):
        """
        This method prints all the callable members of the motor object.
        crtl-f to find one you are looking for.
        """
        all_members = dir(self.motor)
        # Filter to get only callable members (methods)
        methods = [member for member in all_members if callable(getattr(self.motor, member))]

        print(methods)

#if len(d_list)>0:
#    m=Motor(d_list[2])
