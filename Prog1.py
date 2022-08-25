# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/robodk.html
# Note: It is not required to keep a copy of this file, your Python script is saved with your RDK project

from robodk.robolink import *  # RoboDK API
from robodk.robomath import *
from robodk.robodialogs import *
from time import sleep
RDK = Robolink()
robot = RDK.ItemUserPick('',ITEM_TYPE_ROBOT)    
def TCP_Attach(toolitem):
    """Attaches the closest object to the toolitem Htool pose,
    furthermore, it will output appropriate function calls on the generated robot program (call to TCP_On)"""
    toolitem.AttachClosest()
    toolitem.RDK().RunMessage('Grabbing part')
    toolitem.RDK().RunProgram('TCP_Attach');
        
def TCP_Detach(toolitem, itemleave=0):
    """Detaches the closest object attached to the toolitem Htool pose,
    furthermore, it will output appropriate function calls on the generated robot program (call to TCP_Off)"""
    toolitem.DetachAll(itemleave)
    toolitem.RDK().RunMessage('Releasing part')
    toolitem.RDK().RunProgram('TCP_Detach');



def letraA():
    k=1
    A00 = transl(0       ,0        , 0  ) 
    A0 = transl(5*k       ,10*k         , 0  ) 
    A1 = transl(10*k     , 0          , 0  ) 
    A2 = transl(10*k     , 0          , 20*k) 
    A3 = transl(1.95*k  , 3.68*k     , 20*k) 
    A4 = transl(1.95*k  , 3.68*k     , 0) 
    A5 = transl(8.10*k  , 3.68*k     , 0) 
    A6 = transl(8.10*k  , 3.68*k     , 20*k)
    A = [A00,A0, A1, A2, A3, A4, A5, A6]
    robot.setSpeed(50,20)
    RDK.RunProgram('WeldOn(-1)')
    sleep(1)
    robot.MoveJ(A[0]*roty(-pi))
    RDK.RunProgram('WeldOn(1)')
    sleep(1)
    for i in range(2):
        robot.MoveL(A[i+1]*roty(-pi))
    RDK.RunProgram('WeldOn(0)')
    sleep(1)
    for i in range(3):
        robot.MoveJ(A[i+3]*rotx(-pi))
    RDK.RunProgram('WeldOn(1)')
    sleep(1)
    robot.MoveJ(A[6]*rotx(-pi))
    RDK.RunProgram('WeldOn(0)')
    sleep(1)
    robot.MoveJ(A[7]*rotx(-pi))

if not robot.Valid(): 
    quit()

RDK.Render(False)
reference=robot.Parent()
robot.setPoseFrame(reference)

cajas=RDK.Item('cajas')
box1=RDK.Item('box 1')
box2=RDK.Item('box 2')
box3=RDK.Item('box 3')

box1.setPoseAbs(cajas.Pose())
box2.setPoseAbs(cajas.Pose()*transl(0,0,102))
box3.setPoseAbs(cajas.Pose()*transl(0,0,202))

t1=RDK.Item('aproxplace')
t2=RDK.Item('mid')
t3=RDK.Item('place')

fr1=RDK.Item('fr1')
fr2=RDK.Item('fr2')
fr3=RDK.Item('fr3')

gripper=robot.Childs()[1]
lapiz=robot.Childs()[0]
RDK.Render(True)
robot.setPoseFrame(fr1)
robot.MoveJ(t1)
TCP_Attach(robot.Childs()[1])
robot.setPoseFrame(fr1)
robot.MoveJ(transl(0,0,0)*rotx(-pi))
TCP_Detach(robot.Childs()[1])


robot.MoveJ(t2)
TCP_Attach(robot.Childs()[1])
robot.setPoseFrame(fr2)
robot.MoveJ(transl(0,0,0)*rotx(-pi))
TCP_Detach(robot.Childs()[1])
robot.setPoseFrame(fr1)
##
robot.MoveJ(t3)
TCP_Attach(robot.Childs()[1])
robot.setPoseFrame(fr3)
robot.MoveJ(transl(0,0,0)*rotx(-pi))
TCP_Detach(robot.Childs()[1])


robot.setPoseFrame(fr1)
letraA()


