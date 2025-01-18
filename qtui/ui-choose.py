import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QRadioButton, QLabel

class ChooseSpeakerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("选择发言人")
        self.setGeometry(100, 100, 300, 200)

        # 创建一个中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 创建标签
        label = QLabel("请选择发言人：")
        layout.addWidget(label)

        # 创建单选框
        self.radio_button1 = QRadioButton("发言人1")
        self.radio_button2 = QRadioButton("发言人2")
        self.radio_button3 = QRadioButton("发言人3")

        # 将单选框添加到布局中
        layout.addWidget(self.radio_button1)
        layout.addWidget(self.radio_button2)
        layout.addWidget(self.radio_button3)

        # 连接单选框的点击信号到槽函数
        self.radio_button1.clicked.connect(self.on_radio_button_clicked)
        self.radio_button2.clicked.connect(self.on_radio_button_clicked)
        self.radio_button3.clicked.connect(self.on_radio_button_clicked)

        # 设置中心部件的布局
        central_widget.setLayout(layout)

    def on_radio_button_clicked(self):
        if self.radio_button1.isChecked():
            print("选择了发言人1")
        elif self.radio_button2.isChecked():
            print("选择了发言人2")
        elif self.radio_button3.isChecked():
            print("选择了发言人3")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChooseSpeakerWindow()
    window.show()
    sys.exit(app.exec_())
