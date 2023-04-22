# ======================================================================>
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds


#global vars ----------->
win_Name = "VATwindow"
win_Title = "Vertex Animation Texture Generator (VAT)"
win_Width = 300
export_location = 'C:/Users/rgugu/OneDrive/Desktop'


#create window ----------->
def create_vat_window(*args):
    if cmds.window(win_Name, exists=True):
        cmds.deleteUI(win_Name)

    cmds.window(win_Name, width=win_Width, title=win_Title)
    master_layout = cmds.columnLayout(columnAttach=('both', 10), adjustableColumn=True)
    
    cmds.text(win_Title, align="center", width=win_Width, height=50, font="boldLabelFont")
    cmds.text("1. first select the mesh that you want to generate VAT",align="left")
    cmds.text("2. select the timeline range you want to bake",align="left")
    cmds.text("3. hit bake VAT texture",align="left")
    cmds.separator(height=20)
    
    cmds.checkBox('uv_checkbox',label='Generate new UVSet and apply VAT UV map', value=True)
    cmds.checkBox('normal_checkbox',label='Generate Vertex normal Texture', value=True)
    cmds.separator(height=20)

    cmds.text("Select frame range for the animation texture",align="left", height=30)
    cmds.rowLayout(numberOfColumns=4)
    cw = win_Width/4
    cmds.textFieldGrp('s_frame_input',label='start frame:', text=1, columnWidth2=[cw, cw], columnAlign=[1, "center"])
    cmds.textFieldGrp('e_frame_input',label='end frame:', text=1, columnWidth2=[cw, cw], columnAlign=[1, "center"])
    cmds.setParent(master_layout)
    cmds.separator(height=20)

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.button(label='Select export folder',command=get_export_location)
    cmds.text('location_label', label='')
    cmds.setParent(master_layout)
    cmds.separator(height=20)

    cmds.button(label='Create VAT texture',command=create_vat_texture, width=win_Width, height=50)
    cmds.separator(height=20)

    cmds.showWindow()


#misc functs ----------->
def get_export_location(*args):
    print('- get export location')
    global export_location
    export_location = ''
    try:
        export_location = cmds.fileDialog2(dialogStyle=2, fileMode=3)[0]
    except:
        pass
    cmds.text('location_label', edit=True, label=export_location)

def get_input_data():
    print('- getting input data')
    uv_checkbox = cmds.checkBox('uv_checkbox', q=True, value=True)
    normal_checkbox = cmds.checkBox('normal_checkbox', q=True, value=True)
    try:
        start_frame = int(cmds.textFieldGrp('s_frame_input', q=True, text=True))
        end_frame = int(cmds.textFieldGrp('e_frame_input', q=True, text=True))
    except:
        raise Exception('error with start frame or end frame values')
    if end_frame < start_frame:
        raise Exception('end frame cant be lower than start frame')
    
    if export_location == '':
        raise Exception('export folder path cant be empty')
    return uv_checkbox, normal_checkbox, start_frame, end_frame

def get_mesh():
    print('- get mesh')
    sel = cmds.ls(sl=True, type='mesh', dag=True, long=True)
    if sel:
        cmds.select(sel[0])
        return sel[0]
    else:
        cmds.select(clear=True)
        raise Exception("select an object type 'mesh'")

def get_vertices(mesh):
    print('- get vertices')
    return cmds.ls("%s.vtx[*]" % mesh, fl=True)

def get_data(start_frame, end_frame, vertices):
    
    firstVPos = cmds.xform(vertices[0], query=True, worldSpace=True, translation=True)
    minX = maxX = firstVPos[0]
    minY = maxY = firstVPos[1]
    minZ = maxZ = firstVPos[2]
    damp = 0

    framesPos = []
    framesNor = []
    for f in range(start_frame, end_frame + 1):
        cmds.currentTime(f, edit=True)

        vertexPos = []
        vertexNor = []
        for v in vertices:
            #get raw vertex pos ---------------->
            pos = cmds.xform(v, query=True, worldSpace=True, translation=True)
            vertexPos.append(pos)

            # min max X -------->
            if pos[0] < minX:
                minX = pos[0]
            if pos[0] > maxX:
                maxX = pos[0]

            # min max Y -------->
            if pos[1] < minY:
                minY = pos[1]
            if pos[1] > maxY:
                maxY = pos[1]

            # min max Z -------->
            if pos[2] < minZ:
                minZ = pos[2]
            if pos[2] > maxZ:
                maxZ = pos[2]

            #get smooth vertex normal ---------------->
            normals = cmds.polyNormalPerVertex(v, query=True, xyz=True)
            nX = 0
            nY = 0
            nZ = 0
            for n in range(0, len(normals), 3):
                nX += normals[n+0]
                nY += normals[n+1]
                nZ += normals[n+2]
            nX = nX/(len(normals)/3)
            nY = nY/(len(normals)/3)
            nZ = nZ/(len(normals)/3)
            vertexNor.append([nX,nY,nZ])

        #append data to main ---------------->
        framesPos.append(vertexPos)
        framesNor.append(vertexNor)
    
    #calculate damp ----------->
    dampX = maxX - minX
    dampY = maxY - minY
    dampZ = maxZ - minZ
    if damp < dampX:
        damp = dampX
    if damp < dampY:
        damp = dampY
    if damp < dampZ:
        damp = dampZ
    

    print('framesPos > ', framesPos)
    print('framesNor > ', framesNor)
    print('minX > ', minX)
    print('maxX > ', maxX)
    print('minY > ', minY)
    print('maxY > ', maxY)
    print('minZ > ', minZ)
    print('maxZ > ', maxZ)
    print('damp > ', damp)



    return vertexPos, vertexNor, damp, minX, maxX, minY, maxY, minZ, maxZ





#create_vat_texturc ----------->
def create_vat_texture(*args):
    print('- attempt to create VAT')
    
    uv_checkbox, normal_checkbox, start_frame, end_frame = get_input_data()
    mesh = get_mesh()
    vertices = get_vertices(mesh)
    vPos, vNor, damp, minX, maxX, minY, maxY, minZ, maxZ = get_data(start_frame, end_frame, vertices)






# run the plugin ----------->
create_vat_window()
