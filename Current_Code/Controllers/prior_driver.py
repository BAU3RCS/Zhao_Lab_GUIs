from ctypes import WinDLL, create_string_buffer
import os
import sys
import time

dll_path = r"DLLs\Prior\PriorScientificSDK.dll"

class prior():
    
    def __init__(self):

        # Movement limits specificied by company in microns
        self.x_lim = 108000
        self.y_lim = -108000
        self.SDKPrior = None
        self.sessionID = None 
        self.ret = None 
        self.rx = None 

        if os.path.exists(dll_path):
            self.SDKPrior = WinDLL(dll_path)
            print("DLL loaded.")

        else:
            raise RuntimeError("DLL could not be loaded.")
        
        self.rx = create_string_buffer(1000)

        self.ret = self.SDKPrior.PriorScientificSDK_Initialise()

        if self.ret:
            print(f"Error initialising {self.ret}")
            sys.exit()
        else:
            print(f"Ok initialising {self.ret}")

        self.ret = self.SDKPrior.PriorScientificSDK_Version(self.rx)
        print(f"dll version api self.ret={self.ret}, version={self.rx.value.decode()}")


        self.sessionID = self.SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.sessionID < 0:
            print(f"Error getting self.sessionID {self.ret}")
        else:
            print(f"Self.sessionID = {self.sessionID}")


        self.ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(b"dll.apitest 33 goodresponse"), self.rx
        )
        print(f"api response {self.ret}, self.rx = {self.rx.value.decode()}")

        self.ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(b"dll.apitest -300 stillgoodresponse"), self.rx
        )
        print(f"api response {self.ret}, self.rx = {self.rx.value.decode()}")

    def cmd(self, msg):
        #executes commands to hardware

        self.ret = self.SDKPrior.PriorScientificSDK_cmd(
        self.sessionID, create_string_buffer(msg.encode()), self.rx
        )
        
        if self.ret:
            raise RuntimeError(f"Api error {self.ret}")
            
        return self.ret, self.rx.value.decode()
    
    def connect(self, port):
        # connects to specified port

        self.cmd(f"controller.connect.nd {port}")
        print(f"Connected to port {port}.")


    def disconnect(self):
        # disconnects the hardware 
        self.cmd("controller.disconnect")

    def goto_ref(self):
        # move stage to reference point (top right corner)
        self.cmd("controller.stage.reference.set")

    def set_cur_pos(self, x, y):
        # sets the current position to specified coordinates
        self.cmd(f"controller.stage.position.set {x} {y}")
    
    def goto_pos(self, x, y):
        # moves stage to specified position 
        self.cmd(f"controller.stage.goto-position {x} {y}")
    
    def move_rel(self, x, y):
        # moves stage relative to current position
        self.cmd(f"controller.stage.move-relative {x} {y}")

    def stop_moving(self):
        # stops moving stage if it is moving 
        self.cmd("controller.stop.smoothly")

    def calibrate(self):
        # center the stage and set as (0,0)

        self.goto_ref()
        self.wait()
        self.set_cur_pos(0, 0)
        self.wait()
        self.goto_pos(self.x_lim/2, self.y_lim/2)
        self.wait()
        self.set_cur_pos(0, 0)

    def get_pos(self):
        # returns x and y values of current position
        return map(int, (self.cmd("controller.stage.position.get")[1].split(",")))
    
    def wait(self):
        # wait until stage is not busy 

        print("Waiting ...")
        while int(self.cmd("controller.stage.busy.get")[1]):
            time.sleep(0.1)
        print("Ready.")