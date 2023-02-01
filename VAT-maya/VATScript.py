import maya.cmds as cmds

def arrange_uv_vertices(mesh_name, uv_set_name):
    # Obtener una lista de todos los vértices del objeto de malla
    vertices = cmds.ls("{0}.vtx[*]".format(mesh_name), fl=True)
    
    # Obtener el número total de vértices
    num_vertices = len(vertices)
    
    # Calcular el intervalo entre cada vértice en el espacio U
    u_interval = 1.0 / (num_vertices - 1)
    
    # Recorrer cada vértice y asignar su coordenada U en el rango de 0 a 1
    for i, vertex in enumerate(vertices):
        u_coord = i * u_interval
        cmds.polyEditUV(vertex, u=u_coord, v=0, uvSetName=uv_set_name)

# Obtener el nombre del objeto de malla actualmente seleccionado
mesh_name = cmds.ls(sl=True)[0]

# Obtener el nombre del conjunto de UV actualmente activo
uv_set_name = cmds.polyUVSet(mesh_name, q=True, currentUVSet=True)

# Acomodar los vértices del UV map
arrange_uv_vertices(mesh_name, uv_set_name)
