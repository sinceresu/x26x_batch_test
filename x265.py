#!/usr/bin/python3
import os
import re 
import sys,subprocess
from subprocess import Popen,PIPE

#def getPsnr(output) :
#    index = output.rfind('PSNR:')
#    line = output[index:index + 20]
#    matchObj = re.match( r'PSNR: (.*?)$', line, re.M|re.I)
#    if (matchObj) :
#        match_num = matchObj.group(1)
#        return float(match_num)
    
#def getRealBitrate(output) :
#    index = output.rfind('encoded ')
#    line = output[index:index + 60]
#    matchObj = re.match( r'.*, (.*?) kb/s', line, re.M|re.I)
#  #  print(matchObj.group(0))
#  #  print(matchObj.group(1))
#    if (matchObj) :
#        match_num = matchObj.group(1)
#        return float(match_num)

#def getFPS(output) :
#    index = output.rfind('encoded ')
#    line = output[index:index + 60]
#    matchObj = re.match( r'.*, \((.*?) fps', line, re.M|re.I)
#  #  print(matchObj.group(0))
#  #  print(matchObj.group(1))
#    if (matchObj) :
#        match_num = matchObj.group(1)
#        return float(match_num)

def getResult(output) :
    result = {}
    index = output.rfind('encoded ')
    line = output[index:]
    matchObj = re.match( r'.* \((.*?) fps.*, (.*?) kb/s, .* PSNR: (.*?)$', line, re.M|re.I)
  #  print(matchObj.group(0))
  #  print(matchObj.group(1))
    if (matchObj) :
        match_num = matchObj.group(1)
        result['fps'] = float(match_num)
        match_num = matchObj.group(2)
        result['bitrate'] = float(match_num)
        match_num = matchObj.group(3)
        result['psnr'] = float(match_num)
        return result 


def encode(output_file, yuv_file, file_prop, enc_param) :
    x265_param = '--input-res ' + str(file_prop['width']) + 'x' + str(file_prop['height']) \
        + ' --fps ' + file_prop['framerate']
    if enc_param['profile'] : 
        x265_param  +=   ' --profile ' + enc_param['profile']
    if enc_param['preset'] : 
        x265_param  +=   ' --preset ' + enc_param['preset']
    if enc_param['bitrate'] : 
        x265_param  +=   ' --bitrate ' + str(enc_param['bitrate'])
    if enc_param['ref'] : 
        x265_param  +=   ' --ref ' + str(enc_param['ref'])
    if enc_param['bframes'] : 
        x265_param  +=   ' --ref ' + str(enc_param['ref'])
    if enc_param['cmd'] : 
        x265_param  +=   ' ' + str(enc_param['cmd'])

    command =  'x265 --psnr ' + x265_param + ' -o ' + output_file + \
              ' ' + yuv_file
    print(command)

    output_buf = Popen(command, stdout=PIPE, stderr=PIPE, shell=False).communicate() 
    result = output_buf[len(output_buf) - 1]
    output = result.decode('utf-8')
    print(output)

    #psnr = getPsnr(output)
    #if (not psnr) :
    #    return -1
    
    enc_result = getResult(output)
    return enc_result
    #enc_result['psnr'] = psnr
    #enc_result['real_bitrate'] = getRealBitrate(output)

