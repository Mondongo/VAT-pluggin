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


