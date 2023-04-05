# ======================================================================>
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds


# global vars ----------->
winName = "VATwindow"
winTitle = "Vertex Animation Texture Generator (VAT)"
winWidth = 280
start_frame_text = None
end_frame_text = None


# create window ----------->
def create_vat_window(*args):
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)

    cmds.window(winName, width=winWidth, title=winTitle)
    cmds.columnLayout()
    cmds.text(winTitle, align="center", width=winWidth,
              height=50, font="boldLabelFont")
    cmds.text(" 1. first select the mesh that you want to generate VAT")
    cmds.text(" 2. select the timeline range you want to bake")
    cmds.text(" 3. hit bake VAT texture")
    cmds.separator(height=20)
    cw = winWidth/2
    global start_frame_text
    start_frame_text = cmds.textFieldGrp(label='start frame:', columnWidth2=[
                                         cw, cw], columnAlign=[1, "center"])
    global end_frame_text
    end_frame_text = cmds.textFieldGrp(label='end frame:', columnWidth2=[
                                       cw, cw], columnAlign=[1, "center"])
    cmds.separator(height=20)
    cmds.button(label='Create VAT texture',
                command=create_vat_texture, width=winWidth, height=50)
    cmds.showWindow()


# main funct ----------->
def create_vat_texture(*args):
    start_frame, end_frame = sanitize_frame_values()
    mesh = get_mesh()
    vertices = get_vertices(mesh)
    vertexDataRaw, damp, minX, maxX, minY, maxY, minZ, maxZ = get_vertex_data_raw(start_frame, end_frame, vertices)
    vertexDataNor = get_vertex_data_nor(vertexDataRaw, damp, minX, maxX, minY, maxY, minZ, maxZ)
    generatePosTexture(vertexDataNor)
    gererate2UV(mesh)


    

# misc functs ----------->


def sanitize_frame_values():
    sf_value = cmds.textFieldGrp(start_frame_text, query=True, text=True)
    ef_value = cmds.textFieldGrp(end_frame_text, query=True, text=True)

    if sf_value == "" or ef_value == "":
        raise Exception("start frame or end frame cant be empty")

    start_frame = int(sf_value)
    end_frame = int(ef_value)

    if end_frame < start_frame:
        raise Exception("start frame should be lower than end frame")

    # total_frames = (end_frame - start_frame)+1

    return start_frame, end_frame

def get_mesh():
    sel = cmds.ls(sl=True, type='mesh', dag=True, long=True)
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
        pos.append(cmds.xform(vert, query=True,
                   worldSpace=True, translation=True))
    return pos

def get_vertex_data_raw(start_frame, end_frame, vertices):
    firstVPos = cmds.xform(vertices[0], query=True, worldSpace=True, translation=True)
    minX = firstVPos[0]
    maxX = firstVPos[0]
    minY = firstVPos[1]
    maxY = firstVPos[1]
    minZ = firstVPos[2]
    maxZ = firstVPos[2]
    damp = 0
    vertexDataRaw = []

    for f in range(start_frame, end_frame + 1):
        cmds.currentTime(f, edit=True)
        vPosList = []

        for v in vertices:
            vPos = cmds.xform(v, query=True, worldSpace=True, translation=True)

            # min max X -------->
            if vPos[0] < minX:
                minX = vPos[0]
            if vPos[0] > maxX:
                maxX = vPos[0]

            # min max Y -------->
            if vPos[1] < minY:
                minY = vPos[1]
            if vPos[1] > maxY:
                maxY = vPos[1]

            # min max Z -------->
            if vPos[2] < minZ:
                minZ = vPos[2]
            if vPos[2] > maxZ:
                maxZ = vPos[2]

            # add vPos to vertex list -------->
            vPosList.append(vPos)

        vertexDataRaw.append(vPosList)

    dampX = maxX - minX
    dampY = maxY - minY
    dampZ = maxZ - minZ

    if damp < dampX:
        damp = dampX
    if damp < dampY:
        damp = dampY
    if damp < dampZ:
        damp = dampZ
    
    print('damp is: ', damp)
    print('minX is: ', minX)
    print('maxX is: ', maxX)
    print('minY is: ', minY)
    print('maxY is: ', maxY)
    print('minZ is: ', minZ)
    print('maxZ is: ', maxZ)

    return vertexDataRaw, damp, minX, maxX, minY, maxY, minZ, maxZ

def get_vertex_data_nor(vertexDataRaw, damp, minX, maxX, minY, maxY, minZ, maxZ):
    norMinX = (((maxX - minX)*0.5) + minX) - (damp*0.5)
    norMaxX = (((maxX - minX)*0.5) + minX) + (damp*0.5)
    norMinY = (((maxY - minY)*0.5) + minY) - (damp*0.5)
    norMaxY = (((maxY - minY)*0.5) + minY) + (damp*0.5)
    norMinZ = (((maxZ - minZ)*0.5) + minZ) - (damp*0.5)
    norMaxZ = (((maxZ - minZ)*0.5) + minZ) + (damp*0.5)

    vertexDataNor = []

    for f in vertexDataRaw:
        vPosNor = []

        for vPos in f:
            vPosNorX = remap(vPos[0], norMinX, norMaxX, 0, 1)
            vPosNorY = remap(vPos[1], norMinY, norMaxY, 0, 1)
            vPosNorZ = remap(vPos[2], norMinZ, norMaxZ, 0, 1)
            vPosNor.append([vPosNorX, vPosNorY, vPosNorZ])

        vertexDataNor.append(vPosNor)

    return vertexDataNor

def remap(num, old_min, old_max, new_min, new_max):
    return (((num - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

def floatToColor(num):
    col   = int(num * 255)
    return (col)

def generatePosTexture(vertexDataNor):
    try:
        m_util = OpenMaya.MScriptUtil
        m_height = len(vertexDataNor)
        m_width = len(vertexDataNor[0])
        m_depth = 4
        m_image = OpenMaya.MImage()
        m_image.create(m_height, m_width, m_depth )
        m_pixels = m_image.pixels()
        m_arrayLen = m_width * m_height * m_depth
        
        index = 0
        for frame in vertexDataNor:
            for vertex in frame:

                m_util.setUcharArray(m_pixels, index+0, floatToColor(vertex[0]))
                m_util.setUcharArray(m_pixels, index+1, floatToColor(vertex[1]))
                m_util.setUcharArray(m_pixels, index+2, floatToColor(vertex[2]))
                m_util.setUcharArray(m_pixels, index+3, floatToColor(1))
                index = index + 4

        m_image.setPixels(m_pixels, m_width, m_height)
        m_image.writeToFile('c:/Users/rgugu/OneDrive/Desktop/test-image.png', '.png')


        print('total frames: ', len(vertexDataNor))
        print('mesh vertices: ', len(vertexDataNor[0]))
        print('deph (RGBA): 4')
        print('total RGBA values: ',m_arrayLen)


    except:
        print('doesnt work')
        return False
    else:
        return True

def gererate2UV(mesh):
    cmds.polyUVSet(mesh, create=True, uvSet='vat')
    cmds.polyUVSet(mesh, create=False, uvSet='vat', currentUVSet=True)
    cmds.polyForceUV(uvSetName='vat', cp=True)
    cmds.select(cmds.polyListComponentConversion(tv=True), r=True)

    # Guarda los vértices seleccionados en una variable
    meshVertices = cmds.ls(selection=True, flatten=True)

    # modificar los uvs de los vertices selecionados
    total_vertices = len(meshVertices)
    damp = float(1/total_vertices)
    u = damp*0.5
    v = 0
    for vertices in meshVertices:
        cmds.polyEditUV(vertices, uvSetName='vat', relative=False, u=u, v=v, r=True)
        u += damp

    

# run the plugin ----------->
create_vat_window()
