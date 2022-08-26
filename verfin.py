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
    A00 = transl(-50       ,0        , 0  ) 
    A0 = transl(50       ,0         , 0  ) 
    A = [A00,A0]
    robot.setSpeed(50,20)
    RDK.RunProgram('WeldOn(-1)')
    sleep(1)
    robot.MoveJ(A[0]*roty(-pi))
    RDK.RunProgram('WeldOn(1)')
    sleep(1)
    robot.MoveL(A[1]*roty(-pi))
    RDK.RunProgram('WeldOn(0)')
    

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

t1=RDK.Item('aprox')

t2=RDK.Item('place2')
t3=RDK.Item('aproxplace')
t4=RDK.Item('place')



fr1=RDK.Item('fr1')
fr2=RDK.Item('fr2')
fr3=RDK.Item('fr3')

gripper=robot.Childs()[1]
lapiz=robot.Childs()[0]
lapiz.setVisible(0)
gripper.setVisible(1)


#caja 1 
RDK.Render(True)
robot.MoveJ(t1)
TCP_Attach(gripper)
robot.setPoseFrame(fr1)
robot.MoveJ(t3)
robot.MoveJ(t4)
TCP_Detach(gripper, itemleave=0)
#caja 2
robot.setPoseFrame(reference)
robot.MoveJ(t1.Pose()*transl(0,0,150))
TCP_Attach(gripper)
robot.setPoseFrame(fr2)
robot.MoveJ(t3)
robot.MoveJ(t4)
TCP_Detach(gripper, itemleave=0)
## caja 3
robot.setPoseFrame(reference)
robot.MoveJ(t2)
TCP_Attach(gripper)
robot.setPoseFrame(fr3)
robot.MoveJ(t3)
robot.MoveJ(t4)
TCP_Detach(gripper, itemleave=0)

lapiz.setVisible(1)
gripper.setVisible(0)

## sello 1
robot.setPoseFrame(fr1)
robot.MoveJ(t3)
robot.MoveJ(t4)
letraA()

##robot.MoveJ
##robot.MoveJ(t1)
##TCP_Attach(robot.Childs()[1])
##robot.setPoseFrame(fr1)
##robot.MoveJ(transl(0,0,0)*rotx(-pi))
##TCP_Detach(robot.Childs()[1])
##
##
##robot.MoveJ(t2)
##TCP_Attach(robot.Childs()[1])
##robot.setPoseFrame(fr2)
##robot.MoveJ(transl(0,0,0)*rotx(-pi))
##TCP_Detach(robot.Childs()[1])
##robot.setPoseFrame(fr1)
####
##robot.MoveJ(t3)
##TCP_Attach(robot.Childs()[1])
##robot.setPoseFrame(fr3)
##robot.MoveJ(transl(0,0,0)*rotx(-pi))
##TCP_Detach(robot.Childs()[1])
##
##
##robot.setPoseFrame(fr1)
##letraA()
##

