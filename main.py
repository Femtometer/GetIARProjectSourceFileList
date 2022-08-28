import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
import re


def search_file(file_type, dir):
    if os.path.exists(dir):
        for entry in os.scandir(dir):
            if entry.is_file():
                if entry.name.endswith(file_type):
                    prj_name = entry.name
                    break
        return prj_name
    else:
        return None


def open_xml_file(wsdtfile, TOOLKIT_PATH):
    si4filelist = []

    tree = ET.ElementTree(file=wsdtfile)
    ConfigDictionary = tree.find('ConfigDictionary')
    CurrentConfigs = ConfigDictionary.find('CurrentConfigs')
    TargetName = CurrentConfigs.find('Project').text.split('/')[1]

    if TargetName in CurrentConfigs.find('Project').text:
        output_tag = tree.find('Desktop').find("Editor").find("Pane")

        for elem in output_tag.findall('Tab'):
            file = elem.find("Filename").text
            if file.startswith('$WS_DIR$'):
                if file.endswith('.c') or file.endswith('.s') or file.endswith('.h'):
                    si4filelist.append(os.path.abspath(file.replace('$WS_DIR$', os.getcwd())) + '\r\n')
            elif TOOLKIT_PATH != '' and file.startswith('$TOOLKIT_DIR$'):
                if file.endswith('.c') or file.endswith('.s') or file.endswith('.h'):
                    si4filelist.append(file.replace('$TOOLKIT_DIR$', TOOLKIT_PATH) + '\r\n')
        print(si4filelist)


if __name__ == '__main__':
    IAR_Path = "C:/IARSystems/EmbeddedWorkbench7.2/"

    prj = search_file('.eww', ".")
    xml_file = search_file('.wsdt', "./settings/")
    # 找到匹配的文件
    if prj[:-4] == xml_file[:-5]:
        open_xml_file("./settings/" + xml_file, IAR_Path)
