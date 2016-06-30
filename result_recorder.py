
class Recorder:
     def __init__(self, file_name):
        self.file = open(file_name, "w")
        if not self.file :
            return

        self.file.write("input file, output file, width, height, framerate, profile, preset, bitrate(kb/s), speed(fps), psnr(db), avg(kb/s)\n")

     def record(self, h264_file_name, yuv_file_name, file_prop, enc_param, enc_result) :
        if not enc_result:
            return
        if not self.file :
            return
        self.file.write("%s, %s, " % (yuv_file_name, h264_file_name))
        self.file.write("%s, %s, %s, " % (file_prop['width'], file_prop['height'], file_prop['framerate']))
        self.file.write("%s, %s, %s, " % (enc_param['profile'], enc_param['preset'], enc_param['bitrate']))
        self.file.write("%s, %s, %s" % (enc_result['fps'], enc_result['psnr'], enc_result['bitrate']))
        self.file.write("\n")

     def __del__(self):
       self.file.close()
