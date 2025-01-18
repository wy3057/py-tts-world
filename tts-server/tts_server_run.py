import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QMessageBox, QLineEdit

def start_local_tts_server():
    # 启动本地tts_server.py
    subprocess.Popen(['python', 'tts-server.py'])

def on_confirm():
    if radio_start.isChecked():
        start_local_tts_server()
    else:
        global tts_server_address  # 声明全局变量
        tts_server_address = text_box.text()  # 获取文本框内容
        print(f"TTS Server Address: {tts_server_address}")  # 输出TTS服务器地址
        QMessageBox.information(None, "Info", f"TTS Server Address set to: {tts_server_address}")
    app.quit()

# 创建主窗口
app = QApplication([])
root = QWidget()
root.setWindowTitle("TTS Server Control")

# 创建布局
layout = QVBoxLayout()

# 创建单选框
radio_start = QRadioButton("启动TTS服务器")
radio_skip = QRadioButton("跳过启动")
radio_start.setChecked(True)  # 默认选中启动

# 添加单选框到布局
layout.addWidget(radio_start)
layout.addWidget(radio_skip)

# 创建文本框
text_box = QLineEdit()
text_box.setPlaceholderText("输入TTS服务器地址")  # 设置占位符文本

# 添加文本框到布局
layout.addWidget(text_box)

# 创建确认按钮
confirm_button = QPushButton("确认")
confirm_button.clicked.connect(on_confirm)

# 添加按钮到布局
layout.addWidget(confirm_button)

# 设置布局到主窗口
root.setLayout(layout)

# 运行主循环
root.show()
app.exec_()