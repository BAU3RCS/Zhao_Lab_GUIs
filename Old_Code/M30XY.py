# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 02:42:31 2020

@author: Kaifei Kang


"""

import sys
import clr
import ctypes
import numpy as np
import System
import time

sys.path.append("C:\Program Files\Thorlabs\Kinesis")

clr.AddReference("Thorlabs.MotionControl.Controls")
import Thorlabs.MotionControl.Controls

clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")

clr.AddReference("Thorlabs.MotionControl.Benchtop.DCServoCLI")

#clr.AddReference("Thorlabs.MotionControl.IntegratedStepperMotorsCLI")
from Thorlabs.MotionControl.DeviceManagerCLI import *
# from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.DCServoCLI import *


def list_devices():
    DeviceManagerCLI.BuildDeviceList()
    return DeviceManagerCLI.GetDeviceList()
d_list=list_devices()
print(d_list)

class Motor():
    
    def __init__(self,ser):

        self.ser=str(ser)
        self.motors = BenchtopDCServo.CreateBenchtopDCServo(self.ser)
        self.mx = self.motors.GetChannel(1)
        self.my = self.motors.GetChannel(2)
        self.polling_time=250
        self.connect(self.mx, self.ser+'-1')
        self.connect(self.my, self.ser+'-2')
        
    def connect(self, channel, chID):
        
        channel.Connect(self.ser)
        channel.StartPolling(self.polling_time)
        channel.WaitForSettingsInitialized(50000);
        channel.LoadMotorConfiguration(chID)
        channel.EnableDevice()
        self.set_jog_params(channel)
        self.set_vel_params(channel)
        self.set_jog_step(channel, 0.001)
        
    def jog_up(self, motor):
        
        stepsize=float(str(motor.GetJogStepSize()))
        print(stepsize)
        timewait=int(stepsize*500000)
        if timewait<self.polling_time:
            timewait=self.polling_time
            
        try:
            motor.MoveJog(1,timewait)
            return self.pos(motor)
        except Exception as error:
            print(error)
    
    def jog_down(self, motor):
        
        stepsize=float(str(motor.GetJogStepSize()))
        print(stepsize)
        timewait=int(stepsize*500000)
        print(stepsize,timewait)
        if timewait<self.polling_time:
            timewait=self.polling_time
        try:
            motor.MoveJog(2,timewait)
            return self.pos(motor)      
        except Exception as error:
            print(error)
#            while self.motor_state()==1:
#                
#                time.sleep(0.1)
#                print('Motor is moving, current position: {}mm!'.format(self.pos()))
    
    def move_to(self,motor, target):
        
        timewait=self.polling_time
        print(target)
        try:
            motor.MoveTo(System.Decimal(target),timewait)
        except Exception as error:
            print(error)
        
        return self.pos(motor)
    
    def set_vel_params(self, motor, acc = 0.1, maxv = 1):
        
        acc=System.Decimal(acc)
        maxv=System.Decimal(maxv)

        motor.SetVelocityParams(acc, maxv)

    
    def set_jog_params(self,motor, vel=0.1,accl=1,stp_mode=1):
        
        vel=System.Decimal(vel)
        accl=System.Decimal(accl)
        new_pa=motor.GetJogParams()
        new_pa.StopMode= 1
        motor.SetJogParams(new_pa)
        motor.SetJogVelocityParams(vel,accl)

    
    
    def set_jog_step(self, motor, step):
        step=((step)*1)
        print(step)
	
        return motor.SetJogStepSize(System.Decimal(step))
        

    def set_backlash(self,motor, lash):
        motor.SetBacklash(System.Decimal(lash))

    def pos(self, motor):
        return float(str(motor.Position))
        
    def motor_state(self, motor):
        state=motor.State
        return state

    def get_jog_params(self, motor):
        
        vel=motor.GetJogVelocityParams()[0]
        accl=motor.GetJogVelocityParams()[1]
        stop_mode=motor.GetJogParams().StopMode
        return(vel,accl,stop_mode)
    
    def get_vel_params(self, motor):
        return motor.GetVelocityParams()

    def disconnect(self,):
        self.motors.ShutDown()

#if len(d_list)>0:
#    m=Motor('101366054')
