# coding: utf-8
import time
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QProcess, QThread
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from UI_ConvertInterface import Ui_CorvertInterfaceMainWindow
from VideoToFrames_Function import VideoToFrames


class WorkThread(QThread):
    signal = pyqtSignal(str)
    finishsignal = pyqtSignal(str)

    def __init__(self, parent=None):
        # 初始化函数
        super(WorkThread, self).__init__(parent)
        self.convert_video_setting = None
        self.convert_video_function_inst = None

    def run(self):
        # 覆盖父类中原有的 run()函数
        print("开启子线程!")
        try:

            # for i in range(11):
            #     print(self.convert_video_setting)
            #     # self.signal.emit(convert_video_setting)
            #     # self.signal.emit("Hello, this is %dth world!" % i)
            #     time.sleep(1)
            self.convert_video_function_inst.video_convert_info = self.convert_video_setting
            self.convert_video_function_inst.start_convert()
            self.finishsignal.emit("the task is end!")
        except Exception as err:
            print(err)


class ConvertInterface(Ui_CorvertInterfaceMainWindow, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        # 初始化UI
        self.init_ui()
        # 调用信号槽
        self.connect_ui()
        # 启动新的线程
        self.task = None  # 初始化线程
        self.VideoToFrames_Inst = None

        # 快速生成字典
        self.seq = ('videofile',
                    'outputdir',
                    'outputname',
                    'autocreateseqdir',
                    'seqframesnum',
                    'splitframe',
                    'splitframenum',
                    )

        self.videocornvertinfo = dict.fromkeys(self.seq)

    def init_ui(self):
        # 调整面板尺寸
        self.MainCard.setGeometry(QtCore.QRect(0, 45, 740, 900))
        # 设置主卡片的圆角
        self.MainCard.setBorderRadius(200)

        # 隐藏转换状态横幅
        self.ConvernState.setVisible(False)

        # 隐藏任务预览模块
        # self.JobViewLable.setVisible(False)
        # self.HeaderCardWidget.setVisible(False)
        # 设置 处理文件 输出目录 输出文件名控件初始状态
        self.VideoPathText.clearButton.setVisible(True)
        self.VideoPathText.setAcceptDrops(True)

        # 添加输出文件类型的选项
        self.OutputFileTypeComboBox.clear()
        self.OutputFileTypeComboBox.addItem("PNG")
        self.OutputFileTypeComboBox.addItem("JPG")
        self.OutputFileTypeComboBox.addItem("BMP")
        self.OutputFileTypeComboBox.addItem("TIFF")

    def connect_ui(self):
        # self.StartConvertBTN.clicked.connect(self.startconvertbtn_clicked)
        self.SelectVideoBTN.clicked.connect(self.SelectVideoBTN_clicked)
        self.SelectDirBTN.clicked.connect(self.SelectDirBTN_Clicked)
        self.FlashViewBTN.clicked.connect(self.FlashViewBTN_Clicked)
        self.StartConvertBTN.clicked.connect(self.StartConvertBTN_Clicked)

    def SelectVideoBTN_clicked(self):
        videofile = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择视频文件",  # 标题
            r"c:\\",  # 起始目录
            "视频类 (*.mp4 *.mov *.avi)"  # 选择类型过滤项
        )
        self.VideoPathText.setText(videofile[0])
        print(videofile[0])

    def SelectDirBTN_Clicked(self):
        outputfolder = QFileDialog.getExistingDirectory(
            self,  # 父窗口对象
            "选择输出目录",  # 标题
            r"c:\\"  # 起始目录
        )
        print(outputfolder)
        print(type(outputfolder))
        self.OutputPathText.setText(outputfolder)

    def checker_VideoToFrame_Inst(self):
        if self.VideoToFrames_Inst is None:
            self.VideoToFrames_Inst = VideoToFrames()
            print('VideoToFrames实例创建成功')
            return self.VideoToFrames_Inst
        else:
            print('VideoToFrames实例已创建过了')
            return self.VideoToFrames_Inst

    def FlashViewBTN_Clicked(self):
        try:
            videofile = self.VideoPathText.text()
            if videofile != "":
                self.checker_VideoToFrame_Inst()
                videoinfo = self.VideoToFrames_Inst.videoinfo(videofile)
                # 设置任务预览面板数据

                # self.JobViewLable.setVisible(True)
                # self.HeaderCardWidget.setVisible(True)

                # 设置图片
                self.ViewImage.setImage(videoinfo["viewimgpath"])
                self.ViewImage.scaledToWidth(225)
                # self.ViewImage.setBorderRadius(8, 8, 8, 8)

                # 设置label参数
                # videoinfo = ('videofiledir',
                #             'videofilename',
                #             'videofiletype',
                #             'viewimgpath',
                #             'fps',
                #             'size',
                #             'frames',
                #             'fourcc',
                #             'format',
                #             'resolution')
                self.VideoPathClickText.setText(videoinfo['videofilename'] + videoinfo['videofiletype'])
                self.VideoSizeText.setText(videoinfo['size'])
                self.VideoCodeText.setText(videoinfo['fourcc'])
                self.VideoFramesText.setText(str(videoinfo['frames']))
                self.VideoFPSText.setText(str(videoinfo['fps']))
                self.VideoRelText.setText(videoinfo['resolution'])
                if self.SplitframeCheckbox and self.SpliteFramNumSpinBox.value() == 0:
                    self.OutputSeqFrameNumText.setText(str(videoinfo['frames']))
                else:
                    # 显示抽帧之后的视频帧数 未完成
                    # self.SpliteFramNumSpinBox.value()
                    pass
            else:
                print("未选择视频文件")
                pass

        except Exception as err:
            print(err)

    def StartConvertBTN_Clicked(self):

        self.videocornvertinfo['videofile'] = self.VideoPathText.text()
        self.videocornvertinfo['outputdir'] = self.OutputPathText.text()
        self.videocornvertinfo['outputname'] = self.OutputDirNameText.text()
        self.videocornvertinfo['outputfiletype'] = self.OutputFileTypeComboBox.currentText()
        self.videocornvertinfo['autocreateseqdir'] = self.AutoCreateDirCheckBox.isChecked()
        self.videocornvertinfo['seqframesnum'] = self.SeqNumSpinBox.value()
        self.videocornvertinfo['splitframe'] = self.SplitframeCheckbox.isChecked()
        self.videocornvertinfo['splitframenum'] = self.SpliteFramNumSpinBox.value()

        print(self.videocornvertinfo)

        self.task = WorkThread()
        self.task.signal.connect(self.process_Started)

        self.task.convert_video_setting = self.videocornvertinfo
        self.task.convert_video_function_inst = self.checker_VideoToFrame_Inst()
        self.task.start()
        self.task.finishsignal.connect(self.process_finished)

    def process_Started(self, msg):
        self.ConvernState.show()
        '''
        处理QThread的started信号
        '''
        print(msg)

        # start_msg_box = QMessageBox.information(self,
        #                                         'info',
        #                                         '已成功子进程' + msg,
        #                                         QMessageBox.StandardButton.Yes,
        #                                         QMessageBox.StandardButton.Yes)

    #
    def process_finished(self, msg):
        '''
        处理QThread的finished信号
        '''
        print(msg)
        # finished_msg_box = QMessageBox.information(self,
        #                                            'info',
        #                                            f'子进程已关闭,' + msg,
        #                                            QMessageBox.StandardButton.Yes,
        #                                            QMessageBox.StandardButton.Yes)

    # def process_readStdout(self):
    #     if self.process is not None:
    #         data = self.process.readAllStandardOutput()
    #         stdout = bytes(data).decode("utf8")  # 字符串形式的输出信息
    #         # self.textEdit_2.setText(stdout)
    #         print(stdout)
    #
    # def process_readStderr(self):
    #     if self.process is not None:
    #         data = self.process.readAllStandardError()
    #         stderr = bytes(data).decode("utf8")  # 字符串格式的报错信息
    #         # self.textEdit_2.setText(stderr)
    #         print(stderr)
