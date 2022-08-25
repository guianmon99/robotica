from robodk.robolink import *  # RoboDK API
from robodk.robomath import *
from robodk.robodialogs import *

from time import sleep

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

def part_clone(PART_CLONE_NAME,parent,pos):
    """Cretate a clone of the part"""
    newpart = parent.Paste()
    newpart.setName(PART_CLONE_NAME)
    newpart.setPoseAbs(parent.Pose()*transl(0,0,pos))
    # set a random RGB color:
    import random
    color = [random.random(), random.random(), random.random()]
    newpart.Recolor(color)
    newpart.setVisible(True, False)
    return newpart

RDK = Robolink() 


objects = RDK.ItemList(ITEM_TYPE_OBJECT)
robot = RDK.ItemUserPick('',ITEM_TYPE_ROBOT)    #adquirir todos los parámetros d el robot 
if not robot.Valid(): 
    quit()

RDK.Render(False)

for obj in objects:
    if obj.Name().startswith("caja "):
        obj.Delete()
    



pos=robomath.Mat([[0.000000,    -1.000000,     0.000000,  float(2)],
      [1.000000,     0.000000,     0.000000,    float(2)],
      [0.000000,     0.000000,     1.000000,    float(2)],
      [0.000000,     0.000000,     0.000000,     1.000000 ]])
pos2=robomath.Mat([[0.000000,    -1.000000,     0.000000,  float(200)],
      [1.000000,     0.000000,     0.000000,    float(200)],
      [0.000000,     0.000000,     1.000000,    float(0)],
      [0.000000,     0.000000,     0.000000,     1.000000 ]])

frame=RDK.Item('Cajas')
frame.setPose(pos)
cantidad = mbox("ingrese cantidad de cajas:",entry="2")
cantidadf = mbox("ingrese cantidad de frames:",entry="2")

caja1=RDK.Item('box')
caja1.setPose(pos2)
RDK.Render(True)
for i in range(int(cantidad)):
    caja1.Copy()
    box=frame.Paste()
    box.setPose((caja1.Pose())*transl(int(0),int(0),int(100*(i+1))))
    box.setName("caja "+str(i+1))
    

x=0
y=200

fr1=RDK.Item('fr1')
fr1.setPose(pos2)
fr1.Copy()
for i in range(int(cantidadf)):
    frs=fr1.Paste()
    frs.setName("fr "+str(i+2))
    frs.setPose((fr1.Pose())*transl(int(x*i+2),int(y*i+2),0))
    
p1=RDK.Item('pick')
fr1=RDK.Item('fr1')
fr2=RDK.Item('fr 2')
fr3=RDK.Item('fr 3')
robot.MoveJ(p1.Pose())
TCP_Attach(robot.Childs()[1])
robot.setPoseFrame(fr1.Pose())

robot.MoveJ(fr2.Pose())
