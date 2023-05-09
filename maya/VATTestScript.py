import maya.OpenMaya as OpenMaya

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