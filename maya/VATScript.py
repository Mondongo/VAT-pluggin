# ======================================================================>
import math
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds


#global vars ----------->
win_Name = "VATwindow"
win_Title = "Vertex Animation Texture Generator (VAT)"
win_Width = 300
export_location = 'C:/Users/rgugu/OneDrive/Desktop'


#functs ----------->
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
    
    cmds.checkBox('normal_checkbox',label='Generate also Vertex normal Texture', value=True)
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

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.button(label='  Create VAT UVs  ',command=create_vat_uvs, height=50)
    cmds.button(label='Create VAT texture',command=create_vat_textures, height=50)
    cmds.setParent(master_layout)
    cmds.separator(height=20)

    cmds.scrollField('info_text_input', editable=False, wordWrap=True, height=100, text='' )

    cmds.showWindow()

def normalizeVector3(x, y, z):
    mag = math.sqrt((x**2)+(y**2)+(z**2))
    nX = x/mag
    nY = y/mag
    nZ = z/mag
    return nX, nY, nZ

def remap(num, old_min, old_max, new_min, new_max):
    if old_min == old_max:
        return 0.5
    else:
        return (num - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

def floatToColor(num):
    col   = int(num * 255)
    return (col)

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
    return normal_checkbox, start_frame, end_frame

def get_mFnMesh():
    print('- get mesh')
    mSelectionList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(mSelectionList)
    if mSelectionList.isEmpty():
        cmds.select(clear=True)
        raise Exception("select an object type 'mesh'")
    else:
        mDagPath = OpenMaya.MDagPath()
        mSelectionList.getDagPath(0, mDagPath)
        meshObject = mDagPath.node()
        mFnMesh = OpenMaya.MFnMesh(mDagPath)
        return mFnMesh

def get_data(start_frame, end_frame, mFnMesh):
    print('- get vetex position and normal data')

    points = OpenMaya.MPointArray()
    mFnMesh.getPoints(points, OpenMaya.MSpace.kWorld)

    normals = OpenMaya.MFloatVectorArray()
    mFnMesh.getVertexNormals(True, normals, OpenMaya.MSpace.kWorld)

    #get first vertex reference pos ---------------->
    minX = maxX = points[0].x
    minY = maxY = points[0].y
    minZ = maxZ = points[0].z

    vertexPos = []
    vertexNor = []
    for f in range(start_frame, end_frame + 1):
        cmds.currentTime(f, edit=True)

        vPos = []
        vNor = []
        for i in range(points.length()):

            mFnMesh.getPoints(points, OpenMaya.MSpace.kWorld)
            pos = [points[i].x, points[i].y, points[i].z]
            vPos.append(pos)

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

            #get average vertex normal ---------------->
            mFnMesh.getVertexNormals(True, normals, OpenMaya.MSpace.kWorld)
            nX = remap(normals[i].x, -1, 1, 0, 1)
            nY = remap(normals[i].y, -1, 1, 0, 1)
            nZ = remap(normals[i].z, -1, 1, 0, 1)
            vNor.append([nX, nY, nZ])

        #append data to main ---------------->
        vertexPos.append(vPos)
        vertexNor.append(vNor)
    
    #remap positions base on BoundingBox ---------------->
    for f in vertexPos:
        for v in f:
            v[0] = remap(v[0], minX, maxX, 0, 1)
            v[1] = remap(v[1], minY, maxY, 0, 1)
            v[2] = remap(v[2], minZ, maxZ, 0, 1)

    return vertexPos, vertexNor, minX, maxX, minY, maxY, minZ, maxZ

def gen_Pos_Texture(vertexPos):
    print('- attempt to create vertex position texture')
    try:
        m_util = OpenMaya.MScriptUtil
        m_height = len(vertexPos)
        m_width = len(vertexPos[0])
        m_depth = 4
        m_image = OpenMaya.MImage()
        m_image.create(m_height, m_width, m_depth )
        m_pixels = m_image.pixels()
        m_arrayLen = m_width * m_height * m_depth
        
        index = 0
        for frame in vertexPos:
            for vertex in frame:

                m_util.setUcharArray(m_pixels, index+0, floatToColor(vertex[0]))
                m_util.setUcharArray(m_pixels, index+1, floatToColor(vertex[1]))
                m_util.setUcharArray(m_pixels, index+2, floatToColor(vertex[2]))
                m_util.setUcharArray(m_pixels, index+3, floatToColor(1))
                index = index + 4

        m_image.setPixels(m_pixels, m_width, m_height)
        m_image.writeToFile('{}/vert_pos_texture.png'.format(export_location), '.png')

    except:
        print('gen_Pos_Texture doesnt work')
        return False
    else:
        return True

def gen_Nor_Texture(vertexNor):
    print('- attempt to create vertex normal texture')
    try:
        m_util = OpenMaya.MScriptUtil
        m_height = len(vertexNor)
        m_width = len(vertexNor[0])
        m_depth = 4
        m_image = OpenMaya.MImage()
        m_image.create(m_height, m_width, m_depth )
        m_pixels = m_image.pixels()
        m_arrayLen = m_width * m_height * m_depth
        
        index = 0
        for frame in vertexNor:
            for vertex in frame:

                m_util.setUcharArray(m_pixels, index+0, floatToColor(vertex[0]))
                m_util.setUcharArray(m_pixels, index+1, floatToColor(vertex[1]))
                m_util.setUcharArray(m_pixels, index+2, floatToColor(vertex[2]))
                m_util.setUcharArray(m_pixels, index+3, floatToColor(1))
                index = index + 4

        m_image.setPixels(m_pixels, m_width, m_height)
        m_image.writeToFile('{}/vert_nor_texture.png'.format(export_location), '.png')

    except:
        print('gen_Pos_Texture doesnt work')
        return False
    else:
        return True

def create_vat_uvs(*args):
    print('- attempt to get mesh')
    sel = cmds.ls(sl=True, type='mesh', dag=True, long=True)
    if sel:
        print('- creating vat uvs on second UVSet')
        mesh = sel[0]
        cmds.polyUVSet(mesh, create=True, uvSet='vat')
        cmds.polyUVSet(mesh, create=False, uvSet='vat', currentUVSet=True)
        cmds.polyForceUV(uvSetName='vat', cp=True)
        cmds.select(cmds.polyListComponentConversion(tv=True), r=True)
        meshVertices = cmds.ls(selection=True, flatten=True)
        total_vertices = len(meshVertices)
        damp = float(1/total_vertices)
        u = damp*0.5
        v = 0
        for vertices in meshVertices:
            cmds.polyEditUV(vertices, uvSetName='vat', relative=False, u=u, v=v, r=True)
            u += damp
        cmds.select(mesh)
        log_Info('- VAT UVs created on second UVSet')
    else:
        cmds.select(clear=True)
        raise Exception("select an object type 'mesh'")

def log_Info(info_text):
    cmds.scrollField('info_text_input', edit=True, text=info_text)

def create_vat_textures(*args):
    print('- attempt to create VAT')
    normal_checkbox, start_frame, end_frame = get_input_data()
    mFnMesh = get_mFnMesh()
    vertexPos, vertexNor, minX, maxX, minY, maxY, minZ, maxZ = get_data(start_frame, end_frame, mFnMesh)
    gen_Pos_Texture(vertexPos)
    if normal_checkbox:
        gen_Nor_Texture(vertexNor)
    info_text = f'''min X -> {round(minX, 6)}
max X -> {round(maxX, 6)}
min Y -> {round(minY, 6)}
max Y -> {round(maxY, 6)}
min Z -> {round(minZ, 6)}
max Z -> {round(maxZ, 6)}'''
    log_Info(info_text)


# run the plugin ----------->
create_vat_window()