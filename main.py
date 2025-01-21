import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
import threading
import download_and_play_audio
from cnocr import CnOcr
import capture_genshin_window
import crop_bottom_third_from_variable
import crop_bottom__from_variable
import text_to_speech
from tts_server_run import run_tts_server_config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("tts大世界合成")
        self.setGeometry(100, 100, 600, 400)

        # 创建日志窗口
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.WidgetWidth)

        # 启动程序按钮
        self.start_button = QPushButton("启动程序", self)
        self.start_button.clicked.connect(self.start_program)

        # 关闭程序按钮
        self.close_button = QPushButton("关闭程序", self)
        self.close_button.clicked.connect(self.close)

        # 配置TTS服务器按钮
        self.config_tts_button = QPushButton("配置TTS服务器", self)
        self.config_tts_button.clicked.connect(self.config_tts_server)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.log_text)
        layout.addWidget(self.start_button)
        layout.addWidget(self.close_button)
        layout.addWidget(self.config_tts_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # TTS服务器地址
        self.tts_server_address = "https://tts.bgi.sh/v1/audio/speech"

    def config_tts_server(self):
        tts_server_address = run_tts_server_config()
        if tts_server_address:
            self.tts_server_address = tts_server_address
            self.log_text.append(f"TTS Server Address set to: {self.tts_server_address}")

    def start_program(self):
        self.process_and_play_audio()

    def process_and_play_audio(self):
        # 捕获特定窗口的截图
        windowtitle = "原神"
        picture = capture_genshin_window.capture_specific_window(windowtitle)

        # 对截图进行裁剪，获取底部三分之一的图像
        cuttedimage = crop_bottom_third_from_variable.crop_bottom_third_from_variable(picture)

        # 对截图进行裁剪，获取底部的图像，可能是个性签名部分
        persoimage = crop_bottom__from_variable.crop_bottom__from_variable(picture)

        # 使用CnOcr进行光学字符识别
        img_fp = cuttedimage
        ocr = CnOcr()
        out = ocr.ocr(img_fp)

        # 重新初始化OCR，虽然已经初始化过，但这里可能是为了清晰性而重复
        ocr = CnOcr()
        ou = ocr.ocr(persoimage)

        # 打印识别的字符
        print("Predicted Chars:", out)
        print("name", ou)

        # 提取识别的字符和名称
        predicted_chars = out
        name = ou

        # 设置置信度阈值
        confidence_threshold = 0.1

        # 过滤掉低置信度和无关信息
        filtered_text = []
        for item in predicted_chars:
            if item['score'] >= confidence_threshold and not item['text'].startswith('UID'):
                filtered_text.append(item['text'])

        name_text = []
        for item in name:
            if item['score'] >= confidence_threshold and not item['text'].startswith('UID'):
                name_text.append(item['text'])

        # 拼接文本片段
        self.final_text = ''.join(filtered_text)
        name_text = ''.join(name_text)

        # 打印最终的文本和名称
        print(self.final_text)
        print(name_text)

        # 显示处理过的图像
        cuttedimage.show()
        persoimage.show()

        # 主函数，用于处理文本转语音，并播放生成的音频。
        text = self.final_text
        audio_url = text_to_speech.text_to_speech(text, url=self.tts_server_address)

        if audio_url:
            self.log_text.append(f"生成的音频URL: {audio_url}")
            download_and_play_audio.download_and_play_audio(audio_url)
        else:
            self.log_text.append("音频生成失败")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
