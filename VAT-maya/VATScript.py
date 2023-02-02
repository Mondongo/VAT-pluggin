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