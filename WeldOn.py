# Constant variables for the first parameter:
ACTION_RESET    = -1    # Same as: RESET (clear all traces)
ACTION_OFF      =  0    # Same as: OFF (turn on)
ACTION_ON       =  1    # Same as: ON (turn off)

# Define the default Action (ACTION_OFF to deactivate, ACTION_ON to activate, ACTION_RESET to clear any spray gun/trace)
# Setting it to None will display a message
Action = ACTION_ON

# Define the default color as a named color or as #AARRGGBB (Alpha, Red, Green Blue)
# COLOR = 'blue'
COLOR = '#CC3344FF' # AARRGGBB

# Use a specific tool as a spray gun
Tool_Name = "Pencil"    # Use the active tool
#Tool_Name = 'Torch1'

# Use a specific object to project particles:
Object_Name = "Plane"  # Use the first object in the active reference frame
#Object_Name = 'Part'

# --------------------------------------------------
# Program start:
from robolink import *    # API to communicate with RoboDK
from robodk import *      # basic matrix operations
RDK = Robolink()

# quit if we are not in simulation mode
if RDK.RunMode() != RUNMODE_SIMULATE:
    quit()

# Check command input (parameters passed in the call). This is the same as if we were doing a command line call passing parameters.
import sys
if len(sys.argv) > 1:
    Action_str = sys.argv[1].strip().upper()
    if 'ON' in Action_str:
        Action = ACTION_ON
    elif 'OFF' in Action_str:
        Action = ACTION_OFF
    elif 'RESET' in Action_str:
        Action = ACTION_RESET
    else:
        Action = int(Action_str)
    
    if len(sys.argv) > 2:
        Tool_Name = sys.argv[2].strip()
        if Tool_Name == '':
            Tool_Name = None
            
        if len(sys.argv) > 3:
            COLOR = sys.argv[3].lower().strip()

# Display summary
print("Applying action: " + str(Action))
print("Using tool: " + str(Tool_Name))
print("Using color: " + COLOR)

# Get any previously added spray gun simulations and display statistics (spray on the part vs spray falling out of the part)
info, data = RDK.Spray_GetStats()
n_sprays = data.size(1)
spray_id = -1
if n_sprays > 0 and Tool_Name is not None:
    spray_id = RDK.getParam(Tool_Name)
    if spray_id is None or Action == ACTION_ON or type(spray_id) == str or spray_id >= n_sprays:
        spray_id = -1
        
    print("Spray gun statistics:")
    print(info)
    print(data.tr())
    # # Diplay statistics
    # RDK.ShowMessage("Material used: %.1f%%<br>Material waisted: %.1f%%<br>Total particles: %.1f" % (data[1,0],data[2,0],data[3,0]), True)
    # # Clear previous spray
    # RDK.Spray_Clear() 


# If the default Action is None, display a message to activate/deactivate the spray gun
if Action is None:
    print('Note: This macro can be called as ArcStart(1) or ArcStart(0) or ArcStart(-1)')
    entry = mbox('Turn gun ON or OFF', ('On', '1'), ('Off', '0'))
    if not entry:
        quit()
    Action = int(entry)    

# Apply the desired action
if Action == ACTION_OFF:
    # Turn the gun off
    RDK.Spray_SetState(SPRAY_OFF, spray_id)
    
elif Action == ACTION_RESET:
    # Clear all spray simulations (same as pressing ESC key)
    RDK.Spray_Clear(spray_id)
    
elif Action == ACTION_ON:
    # Create a new spray gun object in RoboDK
    # by using RDK.Spray_Add(tool, object, options_command, volume, geometry)
    # tool: tool item (TCP) to use
    # object: object to project the particles
    # options_command (optional): string to specify options. Example:
    #     STEP=AxB: Defines the grid to be projected 1x1 means only one line of particle projection (for example, for welding)
    #     PARTICLE: Defines the shape and size of particle (sphere or particle), unless a specific geometry is provided:
    #       a- SPHERE(radius, facets)
    #       b- SPHERE(radius, facets, scalex, scaley, scalez)
    #       b- CUBE(sizex, sizey, sizez)
    #     RAND=factor: Defines a random factor factor 0 means that the particles are not deposited randomly
    #     ELLYPSE: defines the volume as an ellypse (default)
    #     RECTANGLE: defines the volume as a rectangle
    #     PROJECT: project the particles to the surface (default) (for welding, painting or scanning)
    #     NO_PROJECT: does not project the particles to the surface (for example, for 3D printing)
    #
    # volume (optional): Matrix of parameters defining the volume of the spray gun
    # geometry (optional): Matrix of vertices defining the triangles.

    if spray_id < 0:
        tool = 0    # auto detect active tool
        obj = 0     # auto detect object in active reference frame
        if Tool_Name is not None:
            tool = RDK.Item(Tool_Name, ITEM_TYPE_TOOL)
        
        if Object_Name is not None:
            obj = RDK.Item(Object_Name, ITEM_TYPE_OBJECT)
        # We can specify a given tool object and/or object
        #robot = RDK.Item("ABB IRB 2600-12/1.85", ITEM_TYPE_ROBOT)
        #tools = robot.Childs()
        #if len(tools) > 0:
        #    tool = tools[0]
        #obj = RDK.Item('object', ITEM_TYPE_OBJECT)

        # Create volume parameters
        options_command = "NO_PROJECT PARTICLE=SPHERE(2,8,1,1,1) STEP=1x0 RAND=0 COLOR=" + COLOR
        
        spray_id = RDK.Spray_Add(tool, obj, options_command)
    
    # Remember the ID of the spray gun for later
    if Tool_Name is not None:
        RDK.setParam(Tool_Name, spray_id)
        
    # Apply the state to activate the trace
    RDK.Spray_SetState(SPRAY_ON, spray_id)
