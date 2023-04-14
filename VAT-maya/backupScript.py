#------------------------------------------------------------------------------------------->
import maya.cmds as mc
def buildUI():
  winName = 'myWindow'
  winWidth = 400 # set a target width and reference this when you specify width
  if mc.window(winName, exists=True):
      mc.deleteUI(winName)
  mc.window(winName, width=winWidth, title='Test Window')
  # i always have keep a reference to the main columnLayout
  mainCL = mc.columnLayout() 
  mc.text(label='text row 1')

  # tmpRowWidth controls the width of my columns in the rowLayout
  # with reference to winWidth
  tmpRowWidth = [winWidth*.5, winWidth*.5]
  mc.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
  # at this point our UI pointer is under the rowLayout
  mc.text(label='row column1', align='center', width=tmpRowWidth[0])
  mc.button(label='column 2', width=tmpRowWidth[1])
  # we've used up number of children components, if you add 1 more, 
  # Maya will throw an error
  # now to move our pointer back up the hierarchy, 
  # which is our main columnLayout, mainCL
  mc.setParent('..') # also can use mc.setParent(mainCL)

  tmpRowWidth = [winWidth*0.5, winWidth*0.5]
  mc.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
  mc.text(label='row column1', align='center', width=tmpRowWidth[0])
  mc.button(label='column 2', width=tmpRowWidth[1])
  mc.setParent('..')

  tmpRowWidth = [winWidth*0.7, winWidth*0.3]
  mc.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
  mc.text(label='row column1', align='center', width=tmpRowWidth[0])
  mc.button(label='column 2', width=tmpRowWidth[1])
  mc.setParent('..')

  mc.text(label='text row 3')

  tmpWidth = [winWidth*0.3, winWidth*0.5, winWidth*0.2]
  mc.textFieldButtonGrp(label='txt field', w=winWidth, columnWidth3=tmpWidth, buttonLabel='okay')
  mc.button('full width button', width=winWidth)

  mc.showWindow(winName)
  mc.window(winName, e=True, width=winWidth, height=1)
  return
buildUI()





#al window UI items -------------------------->
import maya.cmds as cmds

def createUI():
    window = cmds.window(title="UI Elements", width=300, height=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label='Hello World', backgroundColor=(1, 0.5, 0.5))
    cmds.textField()
    cmds.separator()
    cmds.text(label="Slider:")
    cmds.floatSlider()
    cmds.separator()
    cmds.text(label="Checkbox:")
    cmds.checkBox()
    cmds.separator(height=100)
    cmds.text(label="Radio Button:")
    cmds.radioButtonGrp(labelArray3=["Option 1", "Option 2", "Option 3"], onCommand1="print('Option 1 selected')", onCommand2="print('Option 2 selected')", onCommand3="print('Option 3 selected')")
    cmds.separator()
    cmds.text(label="Option Menu:")
    cmds.optionMenu(label="Select an option:")
    cmds.menuItem(label="Option 1")
    cmds.menuItem(label="Option 2")
    cmds.menuItem(label="Option 3")
    cmds.showWindow(window)
    
createUI()




#text fiel funcionando -------------------------->
import maya.cmds as cmds

def get_text_field_value(*args):
    text_field_value = cmds.textField(text_field, query=True, text=True)
    print(text_field_value)

window = cmds.window(title="Example Window")
cmds.columnLayout()

text_field = cmds.textField(text="Enter text here")
cmds.button(label="Print Text Field Value", command=get_text_field_value)

cmds.showWindow(window)









#try except -------------------------->
import maya.cmds as cmds

def get_text_field_value(*args):
    try:
        text_field_value = cmds.textField(text_field, query=True, text=True)
        print(text_field_value)
    except Exception as e:
        print("Error:", e)
    

window = cmds.window(title="Example Window")
cmds.columnLayout()
text_field = cmds.textField(text="Enter text here")
cmds.button(label="Print Text Field Value", command=get_text_field_value)
cmds.showWindow(window)








#VAT WINDOW------------------------------------------------------------------------>
import maya.cmds as cmds

winName = "VATwindow"
winTitle = "Vertex Animation Texture Generator (VAT)"
winWidth = 400

#if window already exist delete
if cmds.window(winName, exists=True):
    cmds.deleteUI(winName)
    
#create the window
cmds.window(winName, width=winWidth, title=winTitle)
mainCL = cmds.columnLayout()

cmds.text(winTitle, align="center", width=winWidth, height=50)
cmds.text(" 1. first select the mesh that you want to generate VAT")
cmds.text(" 2. hit bake VAT texture")
cmds.separator(height=20)


#new row layout 3 col
mc.rowLayout(numberOfColumns=3)
mc.text(label='row column1', align='left', width=winWidth/3)
mc.text(label='row column1', align='center', width=winWidth/3)
mc.text(label='row column1', align='right', width=winWidth/3)
mc.setParent(mainCL)

#show the window
cmds.showWindow()




























#======================================================================>
import maya.cmds as cmds


#global vars ----------->
winName = "VATwindow"
winTitle = "Vertex Animation Texture Generator (VAT)"
winWidth = 400


#main functs ----------->
def create_vat_window(*args):
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
        
    cmds.window(winName, width=winWidth, title=winTitle)
    mainCL = cmds.columnLayout()

    cmds.text(winTitle, align="center", width=winWidth, height=50)
    cmds.text(" 1. first select the mesh that you want to generate VAT")
    cmds.text(" 2. hit bake VAT texture")
    cmds.separator(height=20)
    cmds.button(label='Create VAT texture', command=create_vat_texture, width=winWidth, height=50)
    cmds.showWindow()


def create_vat_texture(*args):
    select_mesh_vertices()


def select_mesh_vertices(*args):    
    # Obtener el nombre del objeto seleccionado
    selected = cmds.ls(sl=True)
    
    # Verificar si hay un objeto seleccionado
    if len(selected) > 0:
        # Obtener la lista de vértices
        vertices = cmds.ls(cmds.polyListComponentConversion(tv=True), fl=True)

        # Seleccionar los vértices
        cmds.select(vertices)
    else:
        print("No hay objeto seleccionado.")





#run the plugin ----------->
create_vat_window()











import maya.cmds as cmds
winWidth = 280
cmds.window(width=winWidth)
cmds.columnLayout()
cmds.rowLayout(numberOfColumns=2, columnWidth2=(winWidth/2, winWidth/2))
cmds.textFieldGrp( label='Group 1')
cmds.textFieldGrp( label='Group 2')
cmds.showWindow()



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

    cmds.text(winTitle, align="center", width=winWidth, height=50)
    cmds.separator(height=20)


    tmpWidth = [winWidth*0.3, winWidth*0.5, winWidth*0.2]
    mc.textFieldGrp(label='txt field', w=winWidth, columnWidth3=tmpWidth)

    tmpWidth = [winWidth*0.3, winWidth*0.5, winWidth*0.2]
    cmds.rowLayout(numberOfColumns=4, columnWidth3=tmpWidth)
    sep = winWidth*.4
    cmds.text(label='first frame', align='center', width=sep)
    cmds.textField(width=sep)
    cmds.text(label='last frame', align='center', width=sep)
    cmds.textField(width=sep)
    cmds.setParent(mc)

    cmds.separator(height=20)
    cmds.button(label='Create VAT texture', command=create_vat_texture, width=winWidth, height=50)
    cmds.showWindow()



#run the plugin ----------->
create_vat_window()








# return
# for x in range(1,21):
# cmds.currentTime(x, edit=True)
# vertxPos = get_vertxPos(vertices)
# print(vertxPos)








# save an image ------------------------------------------------------->
import maya.OpenMaya as OpenMaya

def main():
    m_color = float4Torgba(1, 0, 0, 1)
    generateTexture("c:/Users/rgugu/OneDrive/Desktop", "color01", m_color)


def generateTexture(m_path, m_fileName, m_color):
    try:
        m_util = OpenMaya.MScriptUtil
        m_height = 16
        m_width = 16
        m_depth = 4
        m_image = OpenMaya.MImage()
        m_image.create(m_height, m_width, m_depth )
        m_pixels = m_image.pixels()
        m_arrayLen = m_width * m_height * m_depth

        for i in range(0, m_arrayLen, m_depth):
            m_util.setUcharArray(m_pixels, i+0, m_color[0])   
            m_util.setUcharArray(m_pixels, i+1, m_color[1])
            m_util.setUcharArray(m_pixels, i+2, m_color[2])
            m_util.setUcharArray(m_pixels, i+3, m_color[3])

        m_image.setPixels(m_pixels, m_height, m_width)
        m_image.writeToFile('c:/Users/rgugu/OneDrive/Desktop/test-image.png', '.png')

    except:
        OpenMaya.MGlobal.displayWarning("Can't save file to {}/{}.png".format(m_path,m_fileName))
        return False
    else:
        return True

def float4Torgba(m_r, m_g, m_b, m_a):
    m_red   = int(m_r * 255)
    m_green = int(m_g * 255)
    m_blue  = int(m_b * 255)
    m_alpha = int(m_a * 255)
    return (m_red, m_green, m_blue, m_alpha)

main()










#------------------------------------------------------------------------------------>
import maya.cmds as cmds

#get selected mesh
mesh = cmds.ls(selection=True)[0]

#create new uv set
cmds.polyUVSet(mesh, create=True, uvSet='vat')
#cmds.polyUVSet(mesh, create=False, uvSet='vat', currentUVSet=True)

#create uv camera projection
cmds.polyForceUV(uvSetName='vat', cp=True)

# Selecciona los vértices del mesh seleccionado
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





#------------------------------------------------------------------------------->
import maya.cmds as cmds

mesh = cmds.ls(sl=True, type='mesh', dag=True, long=True)[0]
#vertices = cmds.polyListComponentConversion(mesh, toVertex=True)
vertices = cmds.ls("%s.vtx[*]" % mesh, fl=True)

for vertex in vertices:
    print('vertex name: ', vertex)
    vertexNormals = cmds.polyNormalPerVertex(vertex, query=True, xyz=True)
    for index, vertexN in enumerate(vertexNormals):
        print('    vertex normal: ',index, ' > ', vertexN)





#------------------------------------------------------------------------------->
import maya.cmds as cmds

cmds.polySoftEdge( a=180 )