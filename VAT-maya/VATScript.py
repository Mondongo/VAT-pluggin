
#======================================================================>
import maya.cmds as cmds


#global vars ----------->
winName = "VATwindow"
winTitle = "Vertex Animation Texture Generator (VAT)"
winWidth = 400
myText = None


#main functs ----------->
def create_vat_window(*args):
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
        
    cmds.window(winName, width=winWidth, title=winTitle)
    mainCL = cmds.columnLayout()

    cmds.text(winTitle, align="center", width=winWidth, height=50)
    cmds.text(" 1. first select the mesh that you want to generate VAT")
    cmds.text(" 2. hit bake VAT texture")
    cmds.separator(height=20)
    cmds.button(label='Create VAT texture', command=update_text, width=winWidth, height=50)
    cmds.showWindow()
    myText = cmds.text(label="hola mundo")


def update_text(*args):
    print("textura creada exitosamente")
    


#run the plugin ----------->
create_vat_window()