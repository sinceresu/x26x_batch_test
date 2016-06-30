from xml.dom.minidom import parse
import xml.dom.minidom
import parse_config
import testitem_builder
import x264
from result_recorder import Recorder


DOMTree = xml.dom.minidom.parse('enc_config.xml')
root = DOMTree.documentElement
presets = parse_config.getSettings(root)
#print(presets)

files = parse_config.getFiles(root)
#print(files)

test_items = testitem_builder.buildTestItems(presets, files)
#print(test_items)

recorder = Recorder('result.csv')

for item in test_items:
    enc_result = {}      
    if item['encoder'] == 'x264' : 
        result = x264.encode(item['output'], item['input'], \
                item['file_property'], item['encoder_param'], \
                enc_result)
        recorder.record(item['output'], item['input'], \
                item['file_property'], item['encoder_param'], \
                enc_result)


