# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:44:29 2020

@author: kaifei Kang
"""
import time
import visa
import numpy as np
rm=visa.ResourceManager()

class prior():
    
    def __init__(self,addr='ASRL5::INSTR'):
        self.addr=addr 
#        self.inst=rm.open_resource(self.addr)
    def move_XY(self,x,y):
        self.set_value('G {},{}'.format(x,y))

    def move_X(self,x):
        self.set_value('GX {}'.format(x))
        
    def move_Y(self,y):
        self.set_value('GY {}'.format(y))
        
    def move_Z(self,z):
        self.set_value('GZ {}'.format(z))        

    def move_Xrel(self,x):
        x=float(x)
        if x>0:
            self.step_r(x)
        else:
            self.step_l(np.abs(x))
        
    def move_Yrel(self,x):
        x=float(x)
        if x>0:
            self.step_f(x)
        else:
            self.step_b(np.abs(x))
        
    def move_Zrel(self,z):
        z=float(z)
        if z>0:
            self.stepZ_up(z)
        else:
            self.stepZ_down(np.abs(z))

    def step_f(self,stepsize):
        try:
            self.set_value('F {}'.format(stepsize))
        except:
            self.inst.close()
         
    def step_b(self,stepsize):
        try:
            self.set_value('B {}'.format(stepsize))    
        except:
            self.inst.close()

    def step_l(self,stepsize):
        try:
            self.set_value('L {}'.format(stepsize))
        except:
            self.inst.close()
         
    def step_r(self,stepsize):
        try:
            self.set_value('R {}'.format(stepsize))
        except:
            self.inst.close()
        
    def stepZ_up(self,stepsize):
        try:
            self.set_value('U {}'.format(stepsize))
        except:
            self.inst.close()
        
    def stepZ_down(self,stepsize):
        try:
            self.set_value('D {}'.format(stepsize))        
        except:
            self.inst.close()
        
    def get_P(self):
        
        while True:    
            try:
                pos=self.get_value('PS?\r')+self.get_value('PS?\r')
                return pos.strip('R')
                break                                                                                                                                                           
            
            except:
                self.inst.close()
                continue
            
    def set_value(self,command):
        try:
            self.inst=rm.open_resource(self.addr,baud_rate = 9600)
            self.inst.write_termination='\r'
            self.inst.read_termination='\r'  
            self.inst.write(command)
            self.inst.close()
            time.sleep(0.01)
        except:
            pass
        
    def get_value(self,command):
        
        self.inst=rm.open_resource(self.addr,baud_rate = 9600)
        self.inst.write_termination='\r'
        self.inst.read_termination='\r'  
        return self.inst.query(command)
        self.inst.close()

    
#P=prior()
#print(P.get_P())