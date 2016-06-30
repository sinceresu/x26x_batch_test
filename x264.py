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
    
def getRealBitrate(output) :
    index = output.rfind('encoded ')
    line = output[index:index + 50]
    matchObj = re.match( r'.* fps, (.*?) kb/s', line, re.M|re.I)
  #  print(matchObj.group(0))
  #  print(matchObj.group(1))
    if (matchObj) :
        return float(matchObj.group(1))
    


def encode(h264_file_name, yuv_file_name, file_prop, enc_param, enc_result) :
    x264_param = '--input-res ' + str(file_prop['width']) + 'x' + str(file_prop['height']) \
        + ' --fps ' + file_prop['framerate']
    if enc_param['profile'] : 
        x264_param  +=   ' --profile ' + enc_param['profile']
    if enc_param['bitrate'] : 
        x264_param  +=   ' --bitrate ' + str(enc_param['bitrate'])
    if enc_param['ref'] : 
        x264_param  +=   ' --ref ' + str(enc_param['ref'])
    if enc_param['bframes'] : 
        x264_param  +=   ' --ref ' + str(enc_param['ref'])
    if enc_param['cmd'] : 
        x264_param  +=   ' ' + str(enc_param['cmd'])

    command =  'x264 --psnr ' + x264_param + ' -o ' + h264_file_name + \
              ' ' + yuv_file_name
#    print(command)
    output_reader = Popen(command, stdout=PIPE, stderr=PIPE)
    output_reader.wait()
    
    result = output_reader.returncode
  #  print("result: %d" % result)
    if (result !=0) :   
        return -1
    
    raw_output = output_reader.stderr.read()
    output = raw_output.decode('utf-8')
    print(output)

    psnr = getPsnr(output)
    
    if (not psnr) :
        return -1
    
    enc_result['psnr'] = psnr
    enc_result['real_bitrate'] = getRealBitrate(output)
    return 0

