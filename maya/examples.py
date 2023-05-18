# ======================================================================>
from maya.api.OpenMaya import MVector, MMatrix, MPoint
import maya.cmds as cmds

def get_world_transform (obj):
 return MMatrix ( cmds.xform( obj, q=True, matrix=True, ws=True ) )

selected_object = (cmds.ls(sl=1,sn=True))[0]

print ( get_world_transform( selected_object ) )












# ======================================================================>
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds


def remap(num, old_min, old_max, new_min, new_max):
    if old_min == old_max:
        return 0.5
    else:
        return (num - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

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


mesh = get_mesh()
vertices = get_vertices(mesh)


vNor = []
for v in vertices:

    #get smooth vertex normal ---------------->
    normals = cmds.polyNormalPerVertex(v, query=True, xyz=True)
    nX = nY = nZ = 0
    for n in range(0, len(normals), 3):
        nX += normals[n+0]
        nY += normals[n+1]
        nZ += normals[n+2]
    totalNormals = len(normals) / 3
    nX = nX / totalNormals
    nY = nY / totalNormals
    nZ = nZ / totalNormals
    vNor.append([nX, nY, nZ])

print(vNor)
















# ======================================================================>
import   as OpenMaya

# Obtener el objeto MObject de la malla seleccionada
selList = OpenMaya.MSelectionList()
OpenMaya.MGlobal.getActiveSelectionList(selList)
dagPath = OpenMaya.MDagPath()
selList.getDagPath(0, dagPath)
meshObject = dagPath.node()

# Crear un objeto MFnMesh a partir del objeto MObject de la malla
meshFn = OpenMaya.MFnMesh(dagPath)

# Obtener las posiciones de los vértices de la malla
points = OpenMaya.MPointArray()
meshFn.getPoints(points, OpenMaya.MSpace.kWorld)

# Iterar a través de los vértices de la malla y obtener sus normales
normals = OpenMaya.MFloatVectorArray()
meshFn.getVertexNormals(True, normals, OpenMaya.MSpace.kWorld)


# for i in range(normals.length()):
#     normal = normals[i]
#     print("Normal del vértice {}: ({}, {}, {})".format(i, normal.x, normal.y, normal.z))


# for i in range(points.length()):
#     point = points[i]
#     print("Posición del vértice {}: ({}, {}, {})".format(i, point.x, point.y, point.z))

print(normals)
















# -------------------------------------------------------->
import maya.OpenMaya as om


mSelectionList = om.MSelectionList()
om.MGlobal.getActiveSelectionList(mSelectionList)

if mSelectionList.isEmpty():
    print("No hay objetos seleccionados.")
else:
    mDagPath = om.MDagPath()
    mSelectionList.getDagPath(0, mDagPath)
    meshObject = mDagPath.node()
    mFnMesh = om.MFnMesh(mDagPath)

    points = om.MPointArray()
    mFnMesh.getPoints(points, om.MSpace.kWorld)

    normals = om.MFloatVectorArray()
    mFnMesh.getVertexNormals(True, normals, om.MSpace.kWorld)

    for i in range(normals.length()):
        normal = normals[i]
        print("Normal del vértice {}: ({}, {}, {})".format(i, normal.x, normal.y, normal.z))    
    for i in range(points.length()):
        point = points[i]
        print("Posición del vértice {}: ({}, {}, {})".format(i, point.x, point.y, point.z))