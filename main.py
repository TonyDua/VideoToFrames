import cv2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
# from ttk import Progressbar
import subprocess
import threading


class VideoToFrames:
    def __init__(self, master):
        self.master = master
        master.title("视频转序列帧 beta v0.4")
        master.geometry("600x400")
        self.file_label = tk.Label(master, text="选择视频文件:")
        self.file_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=5)

        self.file_button = tk.Button(master, text="选择文件", command=self.select_file)
        self.file_button.grid(row=0, column=2, sticky='e', padx=10, pady=5)

        self.output_label = tk.Label(master, text="选择输出文件夹:")
        self.output_label.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5)

        self.output_button = tk.Button(master, text="选择输出文件夹", command=self.select_output_dir)
        self.output_button.grid(row=1, column=2, sticky='e', padx=10, pady=5)

        self.output_name_label = tk.Label(master, text="输出文件名(英文):")
        self.output_name_label.grid(row=2, column=0, sticky='w', padx=10, pady=5)

        self.output_name_input = tk.Entry(master)
        self.output_name_input.grid(row=2, column=1, padx=10, pady=5)
        self.output_name_input.bind("<Return>", self.write_output_name)

        self.output_file_type_combo = ttk.Combobox(master, values=["png", "jpg", "bmp"])
        self.output_file_type_combo.set("png")
        self.output_file_type_combo.grid(row=2, column=2, padx=10, pady=5)

        self.output_path_label = tk.Label(master, text="输出路径和文件名:")
        self.output_path_label.grid(row=3, column=0, columnspan=2, sticky='w', padx=10, pady=3)

        self.fps_label = tk.Label(master, text="帧速率:")
        self.fps_label.grid(row=4, column=0, columnspan=2, sticky='w', padx=10, pady=3)

        self.size_label = tk.Label(master, text="文件大小:")
        self.size_label.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=3)

        self.frames_label = tk.Label(master, text="预计序列帧数量:")
        self.frames_label.grid(row=6, column=0, columnspan=2, sticky='w', padx=10, pady=3)

        self.start_button = tk.Button(master, text="开始转换", command=self.start_conversion)
        self.start_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.progress_label = tk.Label(master, text="")
        self.progress_label.grid(row=8, column=0, padx=10, pady=10)

        self.process = None
        self.outputdir = ""

    def write_output_name(self, event):
        output_name = self.output_name_input.get()
        output_file_type = self.output_file_type_combo.get()
        outputfilename = self.outputdir + '/' + output_name + '_%d.' + output_file_type
        print(outputfilename)
        self.output_path_label.config(text="输出路径和文件名:" + outputfilename)

    def select_output_dir(self):
        # 选择文件夹并判断是否为空
        self.outputdir = filedialog.askdirectory(title="选择文件夹", parent=root)
        if self.outputdir:
            if os.listdir(self.outputdir):
                tk.messagebox.showwarning("警告", "文件夹内有其他文件，请重新选择空文件夹")
            else:
                self.output_label.config(text="选择的输出文件夹：" + self.outputdir)
        # 输出选择的文件夹路径
        print(self.outputdir)

    def select_file(self):
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="选择文件",
                                                   filetypes=(("MOV files", "*.mov"), ("MP4 files", "*.mp4"), ("AVI files", "*.avi")))
        self.file_label.config(text="选择的视频文件: " + self.filename)

        # 获取视频信息
        cap = cv2.VideoCapture(self.filename)
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = os.path.getsize(self.filename)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        self.fps_label.config(text="帧速率: " + str(fps))
        self.size_label.config(text="文件大小: " + str(size))
        self.frames_label.config(text="预计序列帧数量: " + str(frames))

    def start_conversion(self):
        if not hasattr(self, 'filename'):
            self.file_label.config(text="请先选择视频文件")
            return

        # output_dir = os.path.dirname(self.filename)
        output_dir = self.outputdir
        # output_name = os.path.splitext(os.path.basename(self.filename))[0]
        output_name = self.output_name_input.get()
        output_file_type = self.output_file_type_combo.get()
        output_path = os.path.join(output_dir, output_name + '_%d.' + output_file_type)

        # Check if FFmpeg is installed
        try:
            # 使用ffmpeg将视频转换为序列帧
            command = 'ffmpeg' + ' -i ' + self.filename + ' -qscale:v ' + '2 ' + output_path
            command2 = 'ffmpeg' + ' -i ' + self.filename + ' -qscale:v ' + '2 ' + output_path
            print(command)

            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #t = threading.Thread(target=self.process.communicate)
            (stdout, stderr) = self.process.communicate()
            #t.start()
            total_frames = int(self.frames_label.cget("text").split(": ")[1])
            current_frame = 0

            # 显示进度条
            progress_window = tk.Toplevel(self.master)
            progress_window.title("转换进度")
            progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
            progress_bar.pack()
            progress_label = tk.Label(progress_window, text="0/" + str(total_frames))
            progress_label.pack()

            # 读取ffmpeg输出并更新进度条
            while self.process.poll() is None:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    output_str = output.decode('utf-8').strip()
                    if output_str.startswith('frame='):
                        current_frame += 1
                        progress_bar['value'] = current_frame / total_frames * 100
                        progress_label.config(text=str(current_frame) + "/" + str(total_frames))
                        self.progress_label.config(text=str(current_frame) + "/" + str(total_frames) +
                                                        "   输出完成百分比: " + str(
                            round(current_frame / total_frames * 100, 2)) + "%")

            # 关闭进度条窗口
            progress_window.destroy()

            # 显示完成对话框
            done_window = tk.Toplevel(self.master)
            done_window.title("完成")
            done_label = tk.Label(done_window, text="序列帧输出完成!")
            done_label.pack()
            done_button = tk.Button(done_window, text="Done", command=done_window.destroy)
            done_button.pack()
        except FileNotFoundError:
            # FFmpeg is not installed, download and install it
            tk.messagebox.showwarning("警告", "FFmpeg没有安装，请安装后，将FFmpeg添加到系统变量后重试！！")


root = tk.Tk()
video_to_frames = VideoToFrames(root)
root.mainloop()
