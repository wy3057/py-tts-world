import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QPlainTextEdit
import download_and_play_audio
from cnocr import CnOcr
import capture_genshin_window
import crop_bottom_third_from_variable
import crop_bottom__from_variable
import text_to_speech

class TTSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个标签
        self.label = QLabel('欢迎使用 TTS 应用', self)

        # 创建一个按钮
        self.button = QPushButton('处理文本', self)
        self.button.clicked.connect(self.process_text)  # 连接按钮点击事件到槽函数

        # 创建一个文本编辑框用于显示最终文本
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # 创建一个纯文本编辑框用于显示日志
        self.log_edit = QPlainTextEdit(self)
        self.log_edit.setReadOnly(True)

        # 使用垂直布局管理器
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.log_edit)

        # 设置窗口的布局
        self.setLayout(layout)

        # 设置窗口标题和大小
        self.setWindowTitle('TTS 应用')
        self.setGeometry(300, 300, 400, 500)

    def process_text(self):
        # 清空日志编辑框
        self.log_edit.clear()

        # 捕获特定窗口的截图
        windowtitle = "原神"
        picture = capture_genshin_window.capture_specific_window(windowtitle)
        self.log_edit.appendPlainText(f"捕获窗口: {windowtitle}")

        # 对截图进行裁剪，获取底部三分之一的图像
        cuttedimage = crop_bottom_third_from_variable.crop_bottom_third_from_variable(picture)
        self.log_edit.appendPlainText("裁剪底部三分之一的图像")

        # 对截图进行裁剪，获取底部的图像，可能是个性签名部分
        persoimage = crop_bottom__from_variable.crop_bottom__from_variable(picture)
        self.log_edit.appendPlainText("裁剪底部的图像")

        # 使用CnOcr进行光学字符识别
        img_fp = cuttedimage
        ocr = CnOcr()
        out = ocr.ocr(img_fp)
        self.log_edit.appendPlainText("OCR识别底部三分之一的图像")

        # 重新初始化OCR，虽然已经初始化过，但这里可能是为了清晰性而重复
        ocr = CnOcr()
        ou = ocr.ocr(persoimage)
        self.log_edit.appendPlainText("OCR识别底部的图像")

        # 打印识别的字符
        print("Predicted Chars:", out)
        print("name", ou)
        self.log_edit.appendPlainText(f"识别的字符: {out}")
        self.log_edit.appendPlainText(f"识别的名称: {ou}")

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
        final_text = ''.join(filtered_text)
        name_text = ''.join(name_text)

        # 打印最终的文本和名称
        print(final_text)
        print(name_text)
        self.log_edit.appendPlainText(f"最终文本: {final_text}")
        self.log_edit.appendPlainText(f"名称: {name_text}")

        # 显示处理过的图像
        cuttedimage.show()
        persoimage.show()

        # 调用主函数
        audio_url = text_to_speech.text_to_speech(final_text)
        self.log_edit.appendPlainText(f"生成的音频URL: {audio_url}")

        if audio_url:
            print(f"生成的音频URL: {audio_url}")
            download_and_play_audio.download_and_play_audio(audio_url)
        else:
            print("音频生成失败")
            self.log_edit.appendPlainText("音频生成失败")

        # 在文本编辑框中显示最终文本
        self.text_edit.setText(final_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TTSApp()
    ex.show()
    sys.exit(app.exec_())
