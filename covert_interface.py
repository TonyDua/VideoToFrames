# coding: utf-8
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QProcess
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from UI_ConvertInterface import Ui_CorvertInterfaceMainWindow
from VideoToFrames_Function import VideoToFrames


class ConvertInterface(Ui_CorvertInterfaceMainWindow, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        # 初始化UI
        self.init_ui()
        # 调用信号槽
        self.connect_ui()
        # 启动新的线程
        self.process = None
        self.VideoToFrames_Inst = None

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
        self.process = QProcess()
        if self.process is not None:
            # 线程绑定
            self.process.started.connect(self.process_Started)
            self.checker_VideoToFrame_Inst()
            # self.process.start('notepad.exe')
            try:
                videofile = self.VideoPathText.text()
                outputdir = self.OutputPathText.text()
                outputname = self.OutputDirNameText.text()
                outputfiletype = self.OutputFileTypeComboBox.currentText()
                autocreateseqdir = self.AutoCreateDirCheckBox.checkState()
                seqframesnum = self.SeqNumSpinBox.value()
                splitframe = self.SplitframeCheckbox.checkState()
                splitframenum = self.SpliteFramNumSpinBox.value()

                self.process.started(self.VideoToFrames_Inst.start_convert(videofile,
                                                                         outputdir,
                                                                         outputname,
                                                                         outputfiletype,
                                                                         autocreateseqdir,
                                                                         seqframesnum,
                                                                         splitframe,
                                                                         splitframenum
                                                                         ))
            except Exception as err:
                print(err)
            self.process.readyReadStandardOutput.connect(self.process_readStdout)
            self.process.readyReadStandardError.connect(self.process_readStderr)
            self.process.finished.connect(self.process_finished)

    def process_Started(self):
        self.ConvernState.show()
        '''
        处理QProcess的started信号
        '''
        start_msg_box = QMessageBox.information(self,
                                                'info',
                                                '已成功子进程',
                                                QMessageBox.StandardButton.Yes,
                                                QMessageBox.StandardButton.Yes)

    def process_finished(self, exitCode, exitStatus):
        '''
        处理QProcess的finished信号，获取退出状态
        '''

        finished_msg_box = QMessageBox.information(self,
                                                   'info',
                                                   f'子进程已关闭, exitcode={exitCode}, exitStatus:{exitStatus}',
                                                   QMessageBox.StandardButton.Yes,
                                                   QMessageBox.StandardButton.Yes)

    def process_readStdout(self):
        if self.process is not None:
            data = self.process.readAllStandardOutput()
            stdout = bytes(data).decode("utf8")  # 字符串形式的输出信息
            # self.textEdit_2.setText(stdout)
            print(stdout)

    def process_readStderr(self):
        if self.process is not None:
            data = self.process.readAllStandardError()
            stderr = bytes(data).decode("utf8")  # 字符串格式的报错信息
            # self.textEdit_2.setText(stderr)
            print(stderr)
