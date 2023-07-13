import pymel.core as pm
import maya.cmds as cmds

# Get all model editors in Maya and reset the editorChanged event
for item in pm.lsUI(editors=True):
   if isinstance(item, pm.ui.ModelEditor):
       pm.modelEditor(item, edit=True, editorChanged="")
       
       
       
unknownNodes=cmds.ls(type = "unknown")
unknownNodes+=cmds.ls(type = "unknownDag")
for item in unknownNodes:
    if cmds.objExists(item):
        #print item
        cmds.lockNode(item, lock=False)
        print ('delete - ' + item)
        cmds.delete(item)
        
        
unknown_plugins = cmds.unknownPlugin(q=True, list=True) or []
for up in unknown_plugins:
    print ('delete - ' + up)
    cmds.unknownPlugin(up, remove=True)