import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QRadioButton, QPushButton, QMessageBox, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal, QObject

class TTSConfigSignal(QObject):
    tts_address_signal = pyqtSignal(str)

tts_config_signal = TTSConfigSignal()

def start_local_tts_server():
    try:
        # 启动本地tts_server.py
        subprocess.Popen(['python', 'tts-server.py'])
        print("本地TTS服务器已启动")
        return "http://127.0.0.1:8000/v1/audio/speech"
    except Exception as e:
        print(f"启动本地TTS服务器时发生错误: {e}")
        return None

class TTSServerConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TTS Server Control")

        # 创建布局
        layout = QVBoxLayout()

        # 创建单选框
        self.radio_start = QRadioButton("启动TTS服务器")
        self.radio_skip = QRadioButton("跳过启动")
        self.radio_start.setChecked(True)  # 默认选中启动

        # 添加单选框到布局
        layout.addWidget(self.radio_start)
        layout.addWidget(self.radio_skip)

        # 创建文本框
        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("输入TTS服务器地址")  # 设置占位符文本

        # 添加文本框到布局
        layout.addWidget(self.text_box)

        # 创建按钮盒
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.on_confirm)
        button_box.rejected.connect(self.reject)

        # 添加按钮盒到布局
        layout.addWidget(button_box)

        # 设置布局到对话框
        self.setLayout(layout)

    def on_confirm(self):
        if self.radio_start.isChecked():
            tts_server_address = start_local_tts_server()
        else:
            tts_server_address = self.text_box.text()  # 获取文本框内容
            print(f"TTS Server Address: {tts_server_address}")  # 输出TTS服务器地址
            QMessageBox.information(None, "Info", f"TTS Server Address set to: {tts_server_address}")

        if tts_server_address:
            self.tts_server_address = tts_server_address
            tts_config_signal.tts_address_signal.emit(tts_server_address)
            self.accept()
        else:
            self.reject()

def run_tts_server_config():
    app = QApplication([])
    dialog = TTSServerConfigDialog()
    result = dialog.exec_()
    if result == QDialog.Accepted:
        return dialog.tts_server_address
    return None
