import cv2
import os


class VideoToFrames:
    def __init__(self):
        # 快速生成字典
        self.seq1 = ('videofiledir',
                    'videofilename',
                    'videofiletype',
                    'viewimgpath',
                    'fps',
                    'size',
                    'frames',
                    'fourcc',
                    'format',
                    'resolution')

        self.videofileinfo = dict.fromkeys(self.seq1)

        # 快速生成字典
        self.seq2 = ('videofile',
                    'outputdir',
                    'outputname',
                    'autocreateseqdir',
                    'seqframesnum',
                    'splitframe',
                    'splitframenum',
                    )

        self.video_convert_info = dict.fromkeys(self.seq2)
        #self.video_convert_setting = self.video_convert_info
    def getfilesize(self, videofile):

        fsize = os.path.getsize(videofile)
        # print(fsize)
        if fsize <= 1000000:
            fsize = fsize / float(1024 * 1)
            fsize = round(fsize, 2)
            fsize = str(fsize) + ' KB'
            return fsize
        elif 1000000 <= fsize <= 1000000000:
            fsize = fsize / float(1024 * 1024)
            fsize = round(fsize, 2)
            fsize = str(fsize) + ' MB'
            return fsize
        elif fsize >= 1000000000:
            fsize = fsize / float(1024 * 1024 * 1024)
            fsize = round(fsize, 2)
            fsize = str(fsize) + ' GB'
            return fsize

        return fsize

    def get_video_png(self, videofile, frame_num=1):
        """
        获取视频封面
        :param video_path: 视频文件路径
        :param output_png_path: 截取图片存储路径
        :param frame_num: 指定截取视频第几帧
        :return:
        """
        vidcap = cv2.VideoCapture(videofile)
        # 获取帧数
        frame_count = vidcap.get(7)

        if frame_num > frame_count:
            frame_num = 1
        # print(f"frame_count = {frame_count} | last frame_num = {frame_num}")

        # 指定帧
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

        success, image = vidcap.read()
        # n = 1
        # while n < 30:
        #     success, image = vidcap.read()
        #     n += 1
        dirStr, ext = os.path.splitext(videofile)
        videofilename = dirStr.split("/")[-1]
        videofiledir = os.path.split(dirStr)[0]
        videofiletype = ext
        output_png_path = f'./data/user_data/temp/{videofilename}_{frame_num}.png'
        try:
            imag = cv2.imwrite(output_png_path, image)
        except Exception as err:
            print(err)

        vidcap.release()
        return imag, videofiledir, videofilename, videofiletype, output_png_path

    def videoinfo(self, videofile):
        # print(type(videofile))
        # print("收到的videoFile是" + videofile)
        cap = cv2.VideoCapture(videofile)
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = self.getfilesize(videofile)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        codec = int(cap.get(cv2.CAP_PROP_FOURCC))
        fformat = cap.get(cv2.CAP_PROP_FORMAT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = str(width) + "*" + str(height)

        # 解析CV2 FOURCC  https://www.cnblogs.com/laosan007/p/12778407.html
        fourcc = chr(codec & 0xFF) + chr((codec >> 8) & 0xFF) + chr((codec >> 16) & 0xFF) + chr((codec >> 24) & 0xFF)
        # while (cap.isOpened()):
        #     ret, frame = cap.read(100)
        #     if ret:
        #         cv2.imshow('frame', frame)
        #         c = cv2.waitKey(1)
        #         if c == 27:
        #             break
        view_img_values = self.get_video_png(videofile)
        # print(view_img_values)
        if view_img_values[0]:
            self.videofileinfo["videofiledir"] = view_img_values[1]
            self.videofileinfo["videofilename"] = view_img_values[2]
            self.videofileinfo["videofiletype"] = view_img_values[3]
            self.videofileinfo["viewimgpath"] = view_img_values[4]

        cap.release()

        self.videofileinfo["fps"] = fps
        self.videofileinfo["size"] = size
        self.videofileinfo["frames"] = frames
        self.videofileinfo["fourcc"] = fourcc
        self.videofileinfo["format"] = fformat
        self.videofileinfo["resolution"] = resolution

        print(self.videofileinfo)
        return self.videofileinfo

    def proess_test(self, videofile):
        print(videofile)

    def start_convert(self):
        try:
            # 使用ffmpeg将视频转换为序列帧
            print('VideoToFrames_Function收到的设置是：' + self.video_convert_info)
            # output_path = output_dir + "/" + outputname + outputfiletype
            # command = 'ffmpeg' + ' -i ' + videofile + ' -qscale:v ' + '2 ' + output_path
            # print(command)

            # self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # (stdout, stderr) = self.process.communicate()

            # total_frames = int(self.frames_label.cget("text").split(": ")[1])
            current_frame = 0

            # # 显示进度条
            # progress_window = tk.Toplevel(self.master)
            # progress_window.title("转换进度")
            # progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
            # progress_bar.pack()
            # progress_label = tk.Label(progress_window, text="0/" + str(total_frames))
            # progress_label.pack()

            # 读取ffmpeg输出并更新进度条
            # while self.process.poll() is None:
            #     output = self.process.stdout.readline()
            #     if output == '' and self.process.poll() is not None:
            #         break
            #     if output:
            #         output_str = output.decode('utf-8').strip()
            #         if output_str.startswith('frame='):
            #             current_frame += 1
            #             progress_bar['value'] = current_frame / total_frames * 100
            #             progress_label.config(text=str(current_frame) + "/" + str(total_frames))
            #             self.progress_label.config(text=str(current_frame) + "/" + str(total_frames) +
            #                                             "   输出完成百分比: " + str(
            #                 round(current_frame / total_frames * 100, 2)) + "%")

        except FileNotFoundError:
            # FFmpeg is not installed, download and install it
            # tk.messagebox.showwarning("警告", "FFmpeg没有安装，请安装后，将FFmpeg添加到系统变量后重试！！")
            pass
