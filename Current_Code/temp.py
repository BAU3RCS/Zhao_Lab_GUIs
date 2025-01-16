import Settings.Serial_Numbers as SN
import clr
import sys
import time

from Controllers.KDC101 import Motor

sys.path.append(r"C:\Program Files\Thorlabs\Kinesis")
clr.AddReference("System")
#clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")


from System import String
from System import Decimal
from System import Linq
from System import Text
from System import Threading
from System import Enum
from System.Threading import Tasks


# from System.Collections import *
# from Thorlabs.MotionControl.GenericMotorCLI.Settings import *
# from Thorlabs.MotionControl.GenericMotorCLI import *
# from Thorlabs.MotionControl.KCube.DCServoCLI import *
# # Generic device manager
# from Thorlabs.MotionControl.DeviceManagerCLI import *  

#DeviceManagerCLI.BuildDeviceList()

# Get a list of available devices
#print(list[String](DeviceManagerCLI.GetDeviceList()))

# kdc101 = KCubeDCServo.CreateKCubeDCServo(SN.SN_KDC101)

# kdc101.Connect(SN.SN_KDC101)

# kdc101.EnableDevice()

# time.sleep(0.5)

# kdc101.Home(60000)

KDC = Motor(SN.SN_KDC101)

print(KDC.motor_state())

print(KDC.home(60000))

print(KDC.motor_state())

print(KDC.pos())

print(KDC.jog_up(60000))

print(KDC.pos())

#print(KDC.move_to(10,60000))



print("hi")

#Thorlabs.MotionControl.DeviceManagerCLI.ThorlabsGenericCoreDeviceCLI.VerifyDeviceConnected()