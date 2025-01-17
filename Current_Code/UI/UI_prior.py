"""
Created on Fri Jan 24 15:05:31 2020
Do not copy or modify without permission of the author!!!
@author: Kaifei Kang
"""

from __future__ import division
import sys
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QObject,pyqtSignal
import prior_driver
import KDC101, M30XY
import numpy as np

import Settings.Serial_Numbers as SN

SZ = KDC101.Motor(SN.SN_KDC101)
SXY = M30XY.Motor(SN.SN_M30XY)
RM = KDC101.Motor(SN.SN_KDC101)


SZ.set_vel_params(acc = 0.5, maxv = 5)
SZ.set_jog_params(vel = 0.5, accl = 5, stp_mode = 1)

RM.set_vel_params(acc = 1, maxv = 10)
#Focus.set_vel_params(acc = 1, maxv = 10)
#Focus.set_jog_params(vel = 25, accl = 25, stp_mode = 1)

SZ.set_jog_step(0.001)
RM.set_jog_step(1)
#Focus.set_jog_step(2)

pr = prior_driver.prior()






path = sys.path[0]
MC_GUI = path + r'\MC.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(MC_GUI)

class main(QtWidgets.QMainWindow, Ui_MainWindow,QtWidgets.QFileDialog,QtWidgets.QMessageBox,QtWidgets.QInputDialog):
    
    def __init__(self):
        
        super(main, self).__init__()
        self.setupUi(self)
        self.thread=QThread()
        self.paused=False
        self.show_pos()
        QtWidgets.QShortcut(QtCore.Qt.Key_Up, self, self.steppingSX)
        QtWidgets.QShortcut(QtCore.Qt.Key_Down, self, self.steppingSXN)
        QtWidgets.QShortcut(QtCore.Qt.Key_Left, self, self.steppingSY)
        QtWidgets.QShortcut(QtCore.Qt.Key_Right, self, self.steppingSYN)   
        
        QtWidgets.QShortcut(QtCore.Qt.Key_W, self, self.steppingX)
        QtWidgets.QShortcut(QtCore.Qt.Key_S, self, self.steppingXN)
        QtWidgets.QShortcut(QtCore.Qt.Key_A, self, self.steppingY)
        QtWidgets.QShortcut(QtCore.Qt.Key_D, self, self.steppingYN)   
        
#        QtWidgets.QShortcut(QtCore.Qt.Key_W, self, self.steppingZ)
#        QtWidgets.QShortcut(QtCore.Qt.Key_S, self, self.steppingZN)
        QtWidgets.QShortcut(QtCore.Qt.Key_1, self, self.steppingZ)
        QtWidgets.QShortcut(QtCore.Qt.Key_0, self, self.steppingZN)
        
        QtWidgets.QShortcut(QtCore.Qt.Key_O, self, self.steppingZL)
        QtWidgets.QShortcut(QtCore.Qt.Key_P, self, self.steppingZLN)
        
        QtWidgets.QShortcut(QtCore.Qt.Key_M, self, self.focus_up)
        QtWidgets.QShortcut(QtCore.Qt.Key_N, self, self.focus_down)
        
        
        self.stepX.clicked.connect(self.steppingX)
        self.stepY.clicked.connect(self.steppingY)
        
        self.stepSX.clicked.connect(self.steppingSX)
        self.stepSY.clicked.connect(self.steppingSY)     
        
        self.stepZ.clicked.connect(self.steppingZ)
        self.stepZ_3.clicked.connect(self.steppingZL)
        
        self.stepXN.clicked.connect(self.steppingXN)
        self.stepYN.clicked.connect(self.steppingYN)
        
        self.stepSXN.clicked.connect(self.steppingSXN)
        self.stepSYN.clicked.connect(self.steppingSYN)        
        
        self.stepZN.clicked.connect(self.steppingZN)
        self.stepZN_3.clicked.connect(self.steppingZLN)
        
        self.stepR.clicked.connect(self.steppingR)
        self.stepRN.clicked.connect(self.steppingRN)
        
        
        self.RABS.clicked.connect(self.moveR)
        
    def steppingX(self):
        try:
            stepsize=self.MX_step.value()
            pr.move_Xrel(stepsize)
            self.show_pos()
        except:
            pass
        
    def steppingY(self):
        try:
            stepsize=self.MY_step.value()
            pr.move_Yrel(stepsize)
            self.show_pos()
        except:
            pass

    def steppingSX(self):
        
        channel = SXY.mx
        stepsize = float(self.SX_step.value())*1e-3
        SXY.set_jog_step(channel, stepsize)
        SXY.jog_up(channel)
        self.show_pos()
        
    def steppingSY(self):

        channel = SXY.my
        stepsize = float(self.SY_step.value())*1e-3
        SXY.set_jog_step(channel, stepsize)
        SXY.jog_up(channel)
        self.show_pos()
          
    def steppingZ(self):
        
        stepsize = float(self.SZS_step.value())*1e-3
        SZ.set_jog_step(stepsize)
        SZ.jog_up()
        self.show_pos()
        
    def steppingZL(self):
        
        stepsize=float(self.SZL_step.value())*1e-3
        SZ.set_jog_step(stepsize)
        SZ.jog_up()
        self.show_pos()        
             
    def steppingXN(self):
        
        try:
            stepsize = -self.MX_step.value()
            pr.move_Xrel(stepsize)
            self.show_pos()
        except:
            pass
        
    def steppingYN(self):
        
        try:
            stepsize = -self.MY_step.value()
            pr.move_Yrel(stepsize)
            self.show_pos()
            
        except:
            pass

    def steppingSXN(self):
        
        channel = SXY.mx
        stepsize = float(self.SX_step.value())*1e-3
        SXY.set_jog_step(channel, stepsize)
        SXY.jog_down(channel)
        self.show_pos()
        
    def steppingSYN(self):

        channel = SXY.my
        stepsize = float(self.SY_step.value())*1e-3
        SXY.set_jog_step(channel, stepsize)
        SXY.jog_down(channel)
        self.show_pos()

    def steppingZN(self):
        
        stepsize = float(self.SZS_step.value())*1e-3
        SZ.set_jog_step(stepsize)
        SZ.jog_down()
        self.show_pos()
        
    def steppingZLN(self):
        
        stepsize=float(self.SZL_step.value())*1e-3
        SZ.set_jog_step(stepsize)
        SZ.jog_down()
        self.show_pos()        
        
    def steppingR(self):

        stepsize = float(self.R_step.value())
        RM.set_jog_step(stepsize)
        RM.jog_up()
        self.show_pos()
        
    def steppingRN(self):

        stepsize = float(self.R_step.value())
        RM.set_jog_step(stepsize)
        RM.jog_down()
        self.show_pos()
        
    def move_X(self):
        Xpos=self.absX.text()
        pr.move_X(Xpos)
        self.show_pos()
        
    def move_Y(self):
        Ypos=self.absY.text()
        pr.move_Y(Ypos)
        self.show_pos()
        
    def move_Z(self):
        Zpos=self.absZ.text()
        pr.move_Z(Zpos)        
        self.show_pos()

    def moveR(self):
        
        r_target = self.R_target.text()
        RM.move_to(float(r_target))   
        self.show_pos()

    def focus_up(self):
        Focus.jog_up()

    def focus_down(self):
        Focus.jog_down() 
        
    def show_pos(self):
        
        pos = pr.get_P()
        pos = pos.split(',')
        posz = np.round(SZ.pos()*1e3,3)
        pos_sx = np.round(SXY.pos(SXY.mx)*1e3,3)
        pos_sy = np.round(SXY.pos(SXY.my)*1e3,3)
        r = RM.pos()
        
        try:
#            self.stagePos.setText('The current stage position (x,y,z) = ({},{},{})'.format(pos[0],pos[1],posz))
            self.MX.setText(pos[0])
            self.MY.setText(pos[1])
            self.SX.setText(str(pos_sx))
            self.SY.setText(str(pos_sy))
            self.SZ.setText(str(posz))
            
            
            self.SXbar.setValue(pos_sx)
            self.SYbar.setValue(pos_sy)
            self.SZbar.setValue(posz)
            
            self.Rvalue.setValue(float(r))
            self.dial.setValue(float(r))
            
            self.R_target.setText(str(r))
            
            
            
            
            
        except Exception as error:
            print(error)



            

        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = main()    
    window.show()
       
    sys.exit(app.exec_())