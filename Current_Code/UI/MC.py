# -*- coding: utf-8 -*-
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
import KDC101
import numpy as np
import time
import ctypes
import ctypes.util

import Settings.Serial_Numbers as SN

SM = KDC101.Motor(SN.SN_KDC101)
#RM = KDC101.Motor(SN.SN_KDC101)

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
        QtWidgets.QShortcut(QtCore.Qt.Key_Up, self, self.steppingY)
        QtWidgets.QShortcut(QtCore.Qt.Key_Down, self, self.steppingYN)
        QtWidgets.QShortcut(QtCore.Qt.Key_Left, self, self.steppingX)
        QtWidgets.QShortcut(QtCore.Qt.Key_Right, self, self.steppingXN)     
#        QtWidgets.QShortcut(QtCore.Qt.Key_W, self, self.steppingZ)
#        QtWidgets.QShortcut(QtCore.Qt.Key_S, self, self.steppingZN)
        QtWidgets.QShortcut(QtCore.Qt.Key_1, self, self.steppingZ)
        QtWidgets.QShortcut(QtCore.Qt.Key_0, self, self.steppingZN)
        
        self.stepX.clicked.connect(self.steppingX)
        self.stepY.clicked.connect(self.steppingY)
        self.stepZ.clicked.connect(self.steppingZ)
        self.stepZ_3.clicked.connect(self.steppingZL)
        
        self.stepXN.clicked.connect(self.steppingXN)
        self.stepYN.clicked.connect(self.steppingYN)
        self.stepZN.clicked.connect(self.steppingZN)
        self.stepZN_3.clicked.connect(self.steppingZLN)
        
        self.moveX.clicked.connect(self.move_X)
        self.moveY.clicked.connect(self.move_Y)
        self.moveZ.clicked.connect(self.move_Z)
        
        self.absX.returnPressed.connect(self.move_X)
        self.absY.returnPressed.connect(self.move_Y)
        self.absZ.returnPressed.connect(self.move_Z)
        
        self.setPL.clicked.connect(self.set_start)
        self.setPR.clicked.connect(self.set_end)
        self.saveCoord.clicked.connect(self.save_point)
        self.coordList.itemDoubleClicked.connect(self.move_to_saved)
        
        self.startScan.clicked.connect(self.mapping)
        self.setPause.clicked.connect(self.pause_map)
        self.setContinue.clicked.connect(self.resume_map)
        self.abortMap.clicked.connect(self.abort_map)
        
        p1=self.PL.text().split(',')
        p2=self.PR.text().split(',')
        xstep=self.stepSizeX.text()
        ystep=self.stepSizeY.text()
        waittime=self.waitTime.value()
        self.map_XY=Map(p1,p2,xstep,ystep,-0.03,0.07,waittime)
        
    def steppingX(self):
        try:
            stepsize=self.stepSizeX.text()
            pr.move_Xrel(stepsize)
            xratio=self.xRatio.text()
            zstep=float(stepsize)*float(xratio)*1e-3
            
            if self.focusLink.isChecked():
                if zstep>0:
                    SM.set_jog_step(zstep)
                    SM.jog_up()
                else:
                    SM.set_jog_step(abs(zstep))
                    SM.jog_down()                
                
            self.show_pos()
        except:
            pass
        
        
        
    def steppingSX(self):
        try:
            stepsize=self.stepSizeX.text()
            pr.move_Xrel(stepsize)
            xratio=self.xRatio.text()
            zstep=float(stepsize)*float(xratio)*1e-3
            
            if self.focusLink.isChecked():
                if zstep>0:
                    SM.set_jog_step(zstep)
                    SM.jog_up()
                else:
                    SM.set_jog_step(abs(zstep))
                    SM.jog_down()                
                
            self.show_pos()
        except:
            pass
        
        
    def steppingY(self):
        try:
            stepsize=self.stepSizeY.text()
            yratio=self.yRatio.text()
            zstep=float(stepsize)*float(yratio)*1e-3
            pr.move_Yrel(stepsize)
            
            if self.focusLink.isChecked():
                if zstep>0:
                    SM.set_jog_step(zstep)
                    SM.jog_up()
                else:
                    SM.set_jog_step(abs(zstep))
                    SM.jog_down()  
            self.show_pos()
        except:
            pass
        
    def steppingZ(self):
        
        stepsize=float(self.stepSizeZ.text())*1e-3
        SM.set_jog_step(stepsize)
        SM.jog_up()
        self.show_pos()
        
    def steppingZL(self):
        
        stepsize=float(self.stepSizeZ_3.text())*1e-3
        SM.set_jog_step(stepsize)
        SM.jog_up()
        self.show_pos()        
        
        
        
    def steppingXN(self):
        try:
            stepsize='-'+self.stepSizeX.text()
            pr.move_Xrel(stepsize)
            
            xratio=self.xRatio.text()
            zstep=float(stepsize)*float(xratio)*1e-3
    
            if self.focusLink.isChecked():
                if zstep>0:
                    SM.set_jog_step(zstep)
                    SM.jog_up()
                else:
                    SM.set_jog_step(abs(zstep))
                    SM.jog_down()  
            self.show_pos()
        except:
            pass
    def steppingYN(self):
        try:
            stepsize='-'+self.stepSizeY.text()
            yratio=self.yRatio.text()
            
            zstep=float(stepsize)*float(yratio)*1e-3
    #        zstep=int(zstep)
            pr.move_Yrel(stepsize)
            
            if self.focusLink.isChecked():
                if zstep>0:
                    SM.set_jog_step(zstep)
                    SM.jog_up()
                else:
                    SM.set_jog_step(abs(zstep))
                    SM.jog_down()  
                    
            self.show_pos()
        except:
            pass
        
    def steppingZN(self):
        
        stepsize=float(self.stepSizeZ.text())*1e-3
        SM.set_jog_step(stepsize)
        SM.jog_down()
        self.show_pos()
        
    def steppingZLN(self):
        
        stepsize=float(self.stepSizeZ_3.text())*1e-3
        SM.set_jog_step(stepsize)
        SM.jog_down()
        self.show_pos()


        
    def set_start(self):
        self.PL.setText(pr.get_P())
        
    def set_end(self):
        self.PR.setText(pr.get_P())        
                      
    def pause_map(self):
        self.map_XY.pause_map()
        
    def resume_map(self):
        self.map_XY.resume_map()    
        
    def abort_map(self):
        self.map_XY.stop_map()
        
        
    def save_point(self):
        ad=pr.get_value('P')
        self.coordList.addItem(pr.get_P())

        
    def move_to_saved(self):
        
        coord=self.coordList.currentItem().text().split(',')
        pr.move_X(coord[0])
        pr.move_Y(coord[1])
        pr.move_Z(coord[2])
        
    
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
        
    def show_pos(self):
        
        pos=pr.get_P()
        pos=pos.split(',')
        posz=np.round(SM.pos()*1e3,3)
        
        
        try:
            self.stagePos.setText('The current stage position (x,y,z) = ({},{},{})'.format(pos[0],pos[1],posz))
            self.absX.setText(pos[0])
            self.absY.setText(pos[1])
            self.absZ.setText(str(posz))
        except Exception as error:
            print(error)
#            pass
#    
    def refresh_pos(self):
        
        if SM.motor_state()==1:
            self.label_8.setText('Motor is moving!')
            self.show_pos()
        if SM.motor_state()==0:
            self.label_8.setText('Motor stopped moving!')
            self.show_pos()
    
    
    def mapping(self):
        
        p1=self.PL.text().split(',')
        p2=self.PR.text().split(',')
        xstep=self.stepSizeX.text()
        ystep=self.stepSizeY.text()
        x_ratio=self.xRatio.text()
        y_ratio=self.yRatio.text()
        waittime=self.waitTime.value()
        
        self.map_XY=Map(p1,p2,xstep,ystep,x_ratio,y_ratio,waittime)
        self.map_XY.moveToThread(self.thread)
        self.map_XY.finished.connect(self.thread.quit)
        self.thread.started.connect(self.map_XY.map_image)
        self.map_XY.stepped.connect(self.show_pos)
        self.thread.start() 


        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = main()    
    window.show()
    
    timer = QtCore.QTimer()
    timer.timeout.connect(window.refresh_pos)
    timer.start(250)   
    sys.exit(app.exec_())