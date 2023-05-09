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