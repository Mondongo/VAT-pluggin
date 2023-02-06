
#======================================================================>
import maya.cmds as cmds


#global vars ----------->
winName = "VATwindow"
winTitle = "Vertex Animation Texture Generator (VAT)"
winWidth = 400


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
    cmds.button(label='Create VAT texture', command=create_vat_texture, width=winWidth, height=50)
    cmds.showWindow()


def create_vat_texture(*args):
    select_mesh_vertices()


def select_mesh_vertices(*args):    
# Obtener el nombre del objeto seleccionado
selected = cmds.ls(sl=True)

# Verificar si hay un objeto seleccionado
if len(selected) > 0:
    # Obtener la lista de vértices
    vertices = cmds.ls(cmds.polyListComponentConversion(tv=True), fl=True)

    # Seleccionar los vértices
    cmds.select(vertices)
else:
    print("No hay objeto seleccionado.")





#run the plugin ----------->
create_vat_window()