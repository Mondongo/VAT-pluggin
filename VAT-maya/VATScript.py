import maya.OpenMaya as OpenMaya

def main():
    m_color = float4Torgba(1.0, 0.0, 0.0, 1.0)
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
            m_util.setUcharArray(m_pixels, i+4, 1)

        m_image.setPixels(m_pixels, m_height, m_width)
        m_image.writeToFile( "{}/{}.png".format(m_path,m_fileName), '.png' )

    except:
        OpenMaya.MGlobal.displayWarning("Can't save file to {}/{}.png".format(m_path,m_fileName))
        return False
    else:
        return True

      

def float4Torgba(m_r, m_g, m_b, m_a):
    m_red   = int(m_r * 255.0)
    m_green = int(m_g * 255.0)
    m_blue  = int(m_b * 255.0)
    m_alpha = int(m_a * 255.0)
    return (m_red, m_green, m_blue, m_alpha)

main()