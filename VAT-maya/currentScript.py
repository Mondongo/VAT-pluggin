# ======================================================================>
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

    print(vertexDataNor)

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


# run the plugin ----------->
create_vat_window()
