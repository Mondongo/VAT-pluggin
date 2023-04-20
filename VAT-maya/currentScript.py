# ======================================================================>
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds


# global vars ----------->
win_Name = "VATwindow"
win_Title = "Vertex Animation Texture Generator (VAT)"
win_Width = 300
export_location = ''


# create window ----------->
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
    cmds.textFieldGrp('s_frame_input',label='start frame:', columnWidth2=[cw, cw], columnAlign=[1, "center"])
    cmds.textFieldGrp('e_frame_input',label='end frame:', columnWidth2=[cw, cw], columnAlign=[1, "center"])
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


# main funct ----------->
def get_export_location(*args):
    global export_location
    export_location = ''
    try:
        export_location = cmds.fileDialog2(dialogStyle=2, fileMode=3)[0]
    except:
        pass
    cmds.text('location_label', edit=True, label=export_location)


def create_vat_texture(*args):

    # get input values --------------------->
    # uv_checkbox = cmds.checkBox('uv_checkbox', q=True, value=True)
    # normal_checkbox = cmds.checkBox('normal_checkbox', q=True, value=True)
    # s_frame_input = cmds.textFieldGrp('s_frame_input', q=True, text=True)
    # e_frame_input = cmds.textFieldGrp('e_frame_input', q=True, text=True)

    print(export_location)

    try:
        m_util = OpenMaya.MScriptUtil
        m_height = 10
        m_width = 10
        m_depth = 4
        m_image = OpenMaya.MImage()
        m_image.create(m_height, m_width, m_depth )
        m_pixels = m_image.pixels()
        m_arrayLen = m_width * m_height * m_depth

        for pixel in range(0, m_arrayLen, m_depth):
            #set RGBA values
            m_util.setUcharArray(m_pixels, pixel + 0, 255)
            m_util.setUcharArray(m_pixels, pixel + 1, 0)
            m_util.setUcharArray(m_pixels, pixel + 2, 0)
            m_util.setUcharArray(m_pixels, pixel + 3, 255)

        m_image.setPixels(m_pixels, m_width, m_height)
        m_image.writeToFile('{}/test-image.png'.format(export_location), '.png')

    except:
        print('doesnt work')
        return False
    else:
        return True






# run the plugin ----------->
create_vat_window()
