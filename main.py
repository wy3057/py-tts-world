import time
import pytesseract
import pygetwindow as gw
import pyautogui
from PIL import Image
import pyttsx3
import threading


# 根据你的安装路径设置 Tesseract 的路径
# pytesseract.pytesseract.tesseract_cmd = r'<你的Tesseract安装路径>'

def extract_text_from_image(image):
    """从图片中提取文本"""
    text = pytesseract.image_to_string(image, lang='chi_sim')  # 支持中文
    return text.strip()


def list_voices(engine):
    """列出所有可用的语音模型"""
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name} - {voice.languages}")


def speak_text(text, voice_id):
    """合成并播放文本"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()


def capture_and_recognize(window_title):
    """每200ms截图并识别文本"""
    while True:
        # 获取指定窗口
        try:
            window = gw.getWindowsWithTitle('原神')[0]
        except IndexError:
            print(f"未找到标题为 '{'原神'}' 的窗口。")
            return

        # 截图窗口区域
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))

        # 将截图转为灰度图像以提高 OCR 效果
        screenshot_gray = screenshot.convert('L')

        # 获取图像的尺寸
        width, height = screenshot_gray.size

        # 计算中部四分之一的区域
        box = (width // 4, height // 4, width * 3 // 4, height * 3 // 4)
        box1 = (width // 4, height // 4, width * 3 // 4, height * 3 // 4)
        cropped_image = screenshot_gray.crop(box)#发音文本
        person_image = screenshot_gray.crop(box1)

        # 提取文本
        text = extract_text_from_image(cropped_image)
        text1 = extract_text_from_image(person_image)#获取角色文本
        if text:
            #print("识别到的文本:", text)

            # 每次识别后允许用户选择语音模型
            #engine = pyttsx3.init()
            #print("可用的语音模型:")
            #list_voices(engine)

            # 用户选择语音模型
            voice_id = int(get_number_representation(text1))

            # 合成并播放识别到的文本
            speak_text(text, voice_id)

        time.sleep(0.2)  # 每200ms截图一次

text_number_dict = {
    "Hello": "72 101 108 108 111",
    "World": "87 111 114 108 100",
    "Python": "80 121 116 104 111 110",
    "OpenAI": "79 112 101 110 65 73",
}

def get_number_representation(text):
    # 返回对应文字的数字表示
    return text_number_dict.get(text, "Not found")

if __name__ == "__main__":
    # 用户输入窗口标题
    window_title = input("请输入要截图的窗口标题: ")

    # 启动截图和识别线程
    capture_thread = threading.Thread(target=capture_and_recognize, args=(window_title,))
    capture_thread.start()