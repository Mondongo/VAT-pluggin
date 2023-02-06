#======================================================================>
import maya.cmds as cmds


#global vars ----------->
winName = "VATwindow"
winTitle = "Vertex Animation Texture Generator (VAT)"
winWidth = 280


#main functs ----------->
def create_vat_window(*args):
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
 
    cmds.window(winName, width=winWidth, title=winTitle)
    mc = cmds.columnLayout()
    cmds.text(winTitle, align="center", width=winWidth, height=50, font="boldLabelFont")
    cmds.text(" 1. first select the mesh that you want to generate VAT")
    cmds.text(" 2. select timeline frame range")
    cmds.text(" 3. hit bake VAT texture")
    cmds.separator(height=20)
    cw = winWidth/2
    cmds.textFieldGrp( label='start frame:', columnWidth2=[cw,cw] ,columnAlign=[1,"center"])
    cmds.textFieldGrp( label='end frame:', columnWidth2=[cw,cw] ,columnAlign=[1,"center"])
    cmds.separator(height=20)
    cmds.button(label='Create VAT texture', command=create_vat_texture, width=winWidth, height=50)
    cmds.showWindow()

def create_vat_texture(*args):
    mesh = get_mesh()
    vertices = get_vertices(mesh)
    
    for x in range(1,21):
        cmds.currentTime(x, edit=True)
        vertxPos = get_vertxPos(vertices)
        print(vertxPos)



def get_mesh():
    sel = cmds.ls(sl=True,type='mesh',dag=True, long=True)
    if sel:
        cmds.select(sel[0])
        return sel[0]
    else:
        cmds.select(clear=True)
        raise Exception(">> First select an object type 'mesh'")
 
def get_vertices(mesh):
    return cmds.ls("%s.vtx[*]" % mesh, fl=True)    

def get_vertxPos(vertices):
    pos = []
    for vert in vertices:
        pos.append(cmds.xform(vert, query=True, worldSpace=True, translation=True))
    return pos






#run the plugin ----------->
create_vat_window()