import os
from os.path import basename

def buildTestItems(settings, files):
    test_items = []
    for file in files:
        if file['on'] == '1' :
            setting_names = file['tests']
            for setting_name in setting_names :
                setting = settings[setting_name]
                if (setting) :
                    test_item = {}            
                    test_item['input'] = file['url']
                    base_name = basename(file['url'])

                    extension = ''
                    if setting['encoder'] == 'x265' : extension = 'hevc'
                    elif setting['encoder'] == 'x264':  extension = 'h264'
                    else : extension = 'bin'
                    
                    test_item['output'] = os.path.splitext(base_name)[0] + setting['suffix'] + '.' + extension
                    test_item['file_property'] = file['property']
                    test_item['encoder'] = setting['encoder']
                    test_item['encoder_param'] = setting['param']
                    test_items.append(test_item)

    return test_items
                



