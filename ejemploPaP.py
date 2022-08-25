#type help("robolink") or help("robodk") for more information
#(note: you do not need to keep a copy of this file, your python script is saved with the station)
from robolink import *    # API to communicate with robodk
from robodk import *      # basic matrix operations

# This example shows how to simualate a pick and place application with Python
# The same program used for simulation can be used to generate the robot program

# Define global variables
APPROACH = 100      # approach distance with the robot, in mm
# Number of cycles (station parameter): right click station and select "Station parameters" to modify)
N_CYCLES = 'PartCycles'

# Robot to use for pick and place
ROBOT_NAME = 'ABB IRB 360-3/800 3D'

# Target names:
TARGET_GRAB_PART = 'GetPart'
TARGET_LEAVE_PART = 'FeedConv'

# Reference to leave the object to be picked by the conveyor
CONVEYOR_REFERENCE = 'ConveyorReference'

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

#----------------------------------------------------------
# the program starts here:


RDK = Robolink()

# Grab the first robot available
robot = RDK.Item(ROBOT_NAME, ITEM_TYPE_ROBOT)

# Get the first TCP available (robot child item)
tool = robot.Childs()[0]

# Get the robot reference frame (parent)
uframe = robot.Parent()

# Targets
target_grab = RDK.Item(TARGET_GRAB_PART, ITEM_TYPE_TARGET)
target_leave = RDK.Item(TARGET_LEAVE_PART, ITEM_TYPE_TARGET)

# Target leave pose (position + orientation)
target_leave_pose = target_leave.Pose()

# Calculate approach targets
target_grab_approach = target_grab.Pose()*transl(0,0,-APPROACH)
target_leave_approach = target_leave.Pose()*transl(0,0,-APPROACH)

# Get the conveyor reference (objects will be left there)
conveyor = RDK.Item(CONVEYOR_REFERENCE, ITEM_TYPE_FRAME)

# --------------------------------------
# The robot program starts here
robot.setPoseTool(tool) # this is automatic if there is only one tool
robot.setPoseFrame(uframe)

ncycles = int(RDK.getParam(N_CYCLES))

# loop for as many cycles (parts) as required
for i in range(ncycles):
    # Approach and grab a part     
    robot.MoveJ(target_grab_approach)
    robot.MoveL(target_grab)
    TCP_Attach(tool)
    robot.MoveL(target_grab_approach)
    
    # Leave the part
    shift = transl(-100*(i % 4),0,0)
    robot.MoveJ(target_leave_approach*shift)
    robot.MoveL(target_leave_pose*shift)
    TCP_Detach(tool, conveyor)
    robot.MoveL(target_leave_approach*shift)
    
    
