from robodk.robolink import *  # RoboDK API
from robodk.robomath import *

from time import sleep
RDK = Robolink() 
# hay que nombrar un frame que se llame frame letras y un target que el robot
#pueda alcansar que se llame Letras el plano debe llamarse plane. 
 
robot = RDK.ItemUserPick('',ITEM_TYPE_ROBOT)    #adquirir todos los parámetros d el robot 
if not robot.Valid(): 
    quit() 

def elipse(): 
    frameletras = RDK.Item("FrameLetras") 
    robot.setPoseFrame(frameletras)
    Ref1 = RDK.Item("Letras") 
    RefTar = Ref1.Pose() 
    b1 = Pose_2_TxyzRxyz(RefTar)
    print(transl(b1))
    print(transl(b1)*roty(-pi))
    t = -pi/2     
    x0= b1[0]     
    y0= b1[1]     
    z0= b1[2]     
    a=100     
    b=50 
    RDK.RunProgram('WeldOn(-1)')     
    robot.MoveJ(transl(b1)*roty(-pi))
    robot.setSpeed(5050,2000)    
    while (t <=3*pi/2):         
        pos = transl(x0 + a*cos(t), y0 + b*sin(t), z0)*roty(-pi)         
        robot.MoveJ(pos)    
        if (t==-pi/2):
            RDK.RunProgram('WeldOn')               
            sleep(2) 
        t +=pi/360 
 
elipse() 
RDK.RunProgram('WeldOn(0)') 
