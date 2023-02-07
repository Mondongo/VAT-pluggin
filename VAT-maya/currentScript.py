#======================================================================>
import maya.cmds as cmds


#global vars ----------->
winName = "VATwindow"
winTitle = "Vertex Animation Texture Generator (VAT)"
winWidth = 280
start_frame_text = None
end_frame_text = None


#create window ----------->
def create_vat_window(*args):
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
 
    cmds.window(winName, width=winWidth, title=winTitle)
    cmds.columnLayout()
    cmds.text(winTitle, align="center", width=winWidth, height=50, font="boldLabelFont")
    cmds.text(" 1. first select the mesh that you want to generate VAT")
    cmds.text(" 2. select timeline frame range")
    cmds.text(" 3. hit bake VAT texture")
    cmds.separator(height=20)
    cw = winWidth/2
    global start_frame_text
    start_frame_text = cmds.textFieldGrp(label='start frame:', columnWidth2=[cw,cw] ,columnAlign=[1,"center"])
    global end_frame_text
    end_frame_text = cmds.textFieldGrp(label='end frame:', columnWidth2=[cw,cw] ,columnAlign=[1,"center"])
    cmds.separator(height=20)
    cmds.button(label='Create VAT texture', command=create_vat_texture, width=winWidth, height=50)
    cmds.showWindow()


#main funct ----------->
def create_vat_texture(*args):
    frame_range = sanitize_frame_values()
    mesh = get_mesh()
    vertices = get_vertices(mesh)


    return
    for x in range(1,21):
        cmds.currentTime(x, edit=True)
        vertxPos = get_vertxPos(vertices)
        print(vertxPos)



#misc functs ----------->
def sanitize_frame_values():
    sf_value = cmds.textFieldGrp(start_frame_text, query=True, text=True)
    ef_value = cmds.textFieldGrp(end_frame_text, query=True, text=True)

    if sf_value == "" or ef_value == "":
        raise Exception("start frame or end frame cant be empty")

    start_frame = int(sf_value)
    end_frame = int(ef_value)
    
    if end_frame < start_frame:
        raise Exception("start frame should be lower than end frame")

    return start_frame, end_frame

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