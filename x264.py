#!/usr/bin/python3
import os
import re 
import sys,subprocess
from subprocess import Popen,PIPE

def getPsnr(output) :
    index = output.rfind('Avg:')
    line = output[index:index + 20]
    matchObj = re.match( r'Avg:(.*?) .*', line, re.M|re.I)
    if (matchObj) :
        return float(matchObj.group(1))
    
#def getRealBitrate(output) :
#    index = output.rfind('encoded ')
#    line = output[index:index + 50]
#    matchObj = re.match( r'.* fps, (.*?) kb/s', line, re.M|re.I)
#  #  print(matchObj.group(0))
#  #  print(matchObj.group(1))
#    if (matchObj) :
#        return float(matchObj.group(1))
    

def getResult(output) :
    result = {}
    index = output.rfind('encoded ')
    line = output[index:]
    matchObj = re.match( r'.*, (.*?) fps, (.*?) kb/s$', line, re.M|re.I)
  #  print(matchObj.group(0))
  #  print(matchObj.group(1))
    if (matchObj) :
        match_num = matchObj.group(1)
        result['fps'] = float(match_num)
        match_num = matchObj.group(2)
        result['bitrate'] = float(match_num)

    result['psnr'] = getPsnr(output)
    return result 

def encode(h264_file_name, yuv_file_name, file_prop, enc_param) :
    x264_param = '--input-res ' + str(file_prop['width']) + 'x' + str(file_prop['height']) \
        + ' --fps ' + file_prop['framerate']
    if enc_param['profile'] : 
        x264_param  +=   ' --profile ' + enc_param['profile']
    if enc_param['preset'] : 
        x264_param  +=   ' --preset ' + enc_param['preset']
    if enc_param['bitrate'] : 
        x264_param  +=   ' --bitrate ' + str(enc_param['bitrate'])
    if enc_param['ref'] : 
        x264_param  +=   ' --ref ' + str(enc_param['ref'])
    if enc_param['bframes'] : 
        x264_param  +=   ' --bframes ' + str(enc_param['bframes'])
    if enc_param['cmd'] : 
        x264_param  +=   ' ' + str(enc_param['cmd'])

    command =  'x264 --psnr ' + x264_param + ' -o ' + h264_file_name + \
              ' ' + yuv_file_name
    print(command)

    output_buf = Popen(command, stdout=PIPE, stderr=PIPE, shell=False).communicate() 
    result = output_buf[len(output_buf) - 1]
    output = result.decode('utf-8')
    print(output)

    enc_result = getResult(output)

    return enc_result

