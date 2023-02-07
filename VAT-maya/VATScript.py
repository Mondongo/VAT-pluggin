import maya.cmds as cmds

winName = "win"

def funct_A(arg):
    print(arg)
    

def funct_B():
    print("funct b")
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
 
    window = cmds.window(winName)
    cmds.columnLayout()
    textTxt = "mi texto aca"
    
    cmds.button(label="Print Text", command='funct_A(textTxt)')
    cmds.showWindow(window)


funct_B()