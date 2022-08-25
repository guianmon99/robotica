from robodk.robolink import *  # RoboDK API
from robodk.robomath import *
RDK = Robolink()

objects = RDK.ItemList(ITEM_TYPE_OBJECT)
RDK.Render(False)

for obj in objects:
    if obj.Name().startswith("box "):
        obj.Delete()

RDK.Render(True)

framepaste= RDK.Item('Frame 2')
object1=RDK.Item('box')
object1.Recolor([0,1,1,1])
object1.Copy()

box1 = framepaste.Paste()
box1.setName('box 1')

box2 = framepaste.Paste()
box2.setName('box 2')
box2.setPose(box2.Pose()*transl(0,100,0))
