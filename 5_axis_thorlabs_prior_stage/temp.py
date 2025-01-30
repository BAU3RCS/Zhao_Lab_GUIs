import Settings.Serial_Numbers as SN
from Controllers.KDC101 import Kcube
from Controllers.M30XY import M30XY

Testing = "KDC"

if Testing == "KDC":

    KDC = Kcube(SN.SN_KDC101,SN.Z_motor)

    KDC.home(60000)

    KDC.disconnect()

    print("ending")
    
elif Testing == "M30XY":
    
    M30XY = M30XY(SN.SN_M30XY)
    
    print("connected")
    
    M30XY.home('x',60000)
    M30XY.home('y',60000)
    
    print(M30XY.get_state("y"))
    
    M30XY.disconnect("y")
    
    print("exiting")