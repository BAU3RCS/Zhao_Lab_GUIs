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
clr.AddReference("Thorlabs.MotionControl.IntegratedStepperMotorsCLI")
from Thorlabs.MotionControl.DeviceManagerCLI import *
# from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.IntegratedStepperMotorsCLI import *


def list_devices():
    DeviceManagerCLI.BuildDeviceList()
    return DeviceManagerCLI.GetDeviceList()
d_list=list_devices()
print(d_list)

class Motor():
    
    def __init__(self,ser=d_list[0]):

        self.ser=str(ser)
#        self.motor=KCubeDCServo.CreateKCubeDCServo(self.ser)
#        self.motor = KCubeDCServo.CreateKCubeDCServo(self.ser)
#        IntegratedStepperMotors.CreateIntegratedStepperMotors(self.ser)
#        self.motor = LongTravelStage.CreateLongTravelStage(self.ser)
        self.motor = Thorlabs.MotionControl.IntegratedStepperMotorsCLI.LongTravelStage.CreateLongTravelStage(self.ser)
        self.polling_time=250
        self.connect()
 
    def connect(self):
        
        self.motor.Connect(self.ser)
        self.motor.StartPolling(self.polling_time)
        self.motor.WaitForSettingsInitialized(50000);
        
        
#        print(self.motor.MotorDeviceSettings)
        
        
        
#        self.motor.LoadMotorConfiguration(self.ser)
        while True:
            try:
                

                self.motor.GetMotorConfiguration(self.ser, Thorlabs.MotionControl.DeviceManagerCLI.DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
                break
            except:
                pass
        self.motor.EnableDevice()
#        self.set_jog_params()
#        self.set_vel_params()
#        self.set_jog_step(0.001)
        
    def jog_up(self):
        
        stepsize=float(str(self.motor.GetJogStepSize()))
        print(stepsize)
        timewait=int(stepsize*500000)
        if timewait<self.polling_time:
            timewait=self.polling_time
            
        try:
            self.motor.MoveJog(1,timewait)
            return self.pos()
        except Exception as error:
            print(error)
    
    def jog_down(self):
        
        stepsize=float(str(self.motor.GetJogStepSize()))
        print(stepsize)
        timewait=int(stepsize*500000)
        print(stepsize,timewait)
        if timewait<self.polling_time:
            timewait=self.polling_time
        try:
            self.motor.MoveJog(2,timewait)
            return self.pos()      
        except Exception as error:
            print(error)
#            while self.motor_state()==1:
#                
#                time.sleep(0.1)
#                print('Motor is moving, current position: {}mm!'.format(self.pos()))
    
    def move_to(self,target):
        
        timewait=self.polling_time
        print(target)
        try:
            self.motor.MoveTo(System.Decimal(target),timewait)
        except Exception as error:
            print(error)
        
        return self.pos()
    
    def set_vel_params(self, acc = 200, maxv = 200):
        
        acc=System.Decimal(acc)
        maxv=System.Decimal(maxv)

        self.motor.SetVelocityParams(acc, maxv)

    
    
    
    
    
    
    
    
    def set_jog_params(self,vel=2000,accl=2000,stp_mode=1):
        
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

if len(d_list)>0:
    m=Motor('101366054')
