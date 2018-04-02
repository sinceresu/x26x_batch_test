# -*- coding: cp936 -*-
from xml.dom.minidom import parse
import xml.dom.minidom

def getNodeValue(parent, node_name) :
    nodes = parent.getElementsByTagName(node_name)
    if not nodes:
        return None
    node = nodes[0].childNodes;
    if not node :
        return None
    return node[0].data

def getEncoderParam(parent_node) :
    enc_param = {}
    enc_param['profile'] = getNodeValue(parent_node, 'profile')
    enc_param['preset'] = getNodeValue(parent_node, 'preset')
    enc_param['bitrate'] = getNodeValue(parent_node, 'bitrate')
    enc_param['keyint'] = getNodeValue(parent_node, 'keyint')
    enc_param['ref'] = getNodeValue(parent_node, 'ref')
    enc_param['bframes'] = getNodeValue(parent_node, 'bframes')
    enc_param['cmd'] = getNodeValue(parent_node, 'cmd')
    return enc_param

def getSettings(parent_node) :
    settings_node = parent_node.getElementsByTagName('settings')[0]
    setting_nodes = settings_node.getElementsByTagName('setting')   
    settings = {};
    for setting_node in setting_nodes:
        setting = {}
        setting['encoder'] = setting_node.getAttribute('encoder')
        setting['name'] = setting_node.getAttribute('name')
        setting['suffix'] = setting_node.getAttribute('suffix')
        setting['on'] = setting_node.getAttribute('on')
        setting['param'] = getEncoderParam(setting_node)
        settings[setting['name']] = setting

    return settings
    
 
def getFiles(parent_node) :
    files_node = parent_node.getElementsByTagName("files")[0]
    file_nodes = files_node.getElementsByTagName("file")
    files = [];
    for file_node in file_nodes:
        file = {}
        file['url'] = file_node.getAttribute('url')
        file['on'] = file_node.getAttribute('on')
        file_property = {}
        file_property['width'] = getNodeValue(file_node, 'width')
        file_property['height'] = getNodeValue(file_node, 'height')
        file_property['framerate'] = getNodeValue(file_node, 'framerate')
        file['property'] = file_property
        test_settings = []
        tests_node = parent_node.getElementsByTagName("tests")[0]
        test_nodes = tests_node.getElementsByTagName("setting")
        for test_node in test_nodes:
            setting = {}
            setting['name'] = test_node.getAttribute('name')
            setting['on'] = test_node.getAttribute('on')
            test_settings.append(setting)
        file['tests'] = test_settings
        files.append(file)
    return files
