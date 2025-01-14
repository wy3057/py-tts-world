def crop_bottom_third_from_variable(image):
    """
    裁剪图片的下三分之一，并返回裁剪后的图片。

    Args:
        image (PIL.Image.Image): 输入的图片对象。

    Returns:
        PIL.Image.Image: 裁剪后的图片对象。
    """
    # 获取图像尺寸
    width, height = image.size

    # 计算裁剪区域
    upper = height * 5 // 6
    # 上边界为图像高度的 2/3

    rect = (0, upper, width, height)  # 裁剪区域 (x1, y1, x2, y2)

    # 裁剪图像
    cropped_image = image.crop(rect)

    return cropped_image


def crop_bottom__from_variable(image):
    """
    裁剪图片的下三分之一，并返回裁剪后的图片。

    Args:
        image (PIL.Image.Image): 输入的图片对象。

    Returns:
        PIL.Image.Image: 裁剪后的图片对象。
    """
    # 获取图像尺寸
    width, height = image.size

    # 计算裁剪区域
    upper = height * 3 // 4
    down = height * 5 // 6
    # 上边界为图像高度的 2/3

    rect = (0, upper, width, down)  # 裁剪区域 (x1, y1, x2, y2)

    # 裁剪图像
    personimage = image.crop(rect)

    return personimage


import capture_genshin_window

windowtitle = "原神"
picture = capture_genshin_window.capture_specific_window(windowtitle)
cuttedimage = crop_bottom_third_from_variable(picture)
persoimage = crop_bottom__from_variable(picture)
from cnocr import CnOcr

img_fp = cuttedimage
ocr = CnOcr()
out = ocr.ocr(img_fp)

ocr = CnOcr()
ou = ocr.ocr(persoimage)
print("Predicted Chars:", out)
print("name", ou)
predicted_chars = out
name = ou
# 设置置信度阈值
confidence_threshold = 0.1

# 过滤掉低置信度和无关信息


# 拼接文本片段
filtered_text = []
for item in predicted_chars:
    if item['score'] >= confidence_threshold and not item['text'].startswith('UID'):
        filtered_text.append(item['text'])

name_text = []
for item in name:
    if item['score'] >= confidence_threshold and not item['text'].startswith('UID'):
        name_text.append(item['text'])
import requests
import pygame
import tempfile
import os


def text_to_speech(text, voice='派蒙', speed=0.2, pitch=0.6, pause=0.8, style=1):
    """
    调用TTS API将文本转换为语音

    参数:
        text (str): 要转换的文本
        voice (str): 语音角色
        speed (float): 语速
        pitch (float): 音调
        pause (float): 停顿
        style (int): 风格
    """
    # API配置
    if voice is None:
        voice = ou
    url = "https://tts.bgi.sh/v1/audio/speech"
    headers = {
        "Authorization": "Bearer sk-bgi",
        "Content-Type": "application/json"
    }

    # 请求数据
    payload = {
        "prompt": text,
        "voice": voice,
        "speed": speed,
        "pitch": pitch,
        "pause": pause,
        "style": style
    }

    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 检查响应状态

        # 解析响应
        result = response.json()
        if result["status"] == "success":
            return result["audio_url"]
        else:
            raise Exception("API调用失败")

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None


def download_and_play_audio(audio_url):
    """
    下载并播放音频文件

    参数:
        audio_url (str): 音频文件URL
    """
    try:
        # 下载音频文件
        response = requests.get(audio_url)
        response.raise_for_status()

        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name

        # 初始化pygame混音器
        pygame.mixer.init()

        # 加载并播放音频
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # 等待播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # 清理临时文件
        pygame.mixer.quit()
        os.unlink(temp_path)

    except Exception as e:
        print(f"播放音频时发生错误: {e}")


def main():
    # 示例使用
    text = final_text
    audio_url = text_to_speech(text)

    if audio_url:
        print(f"生成的音频URL: {audio_url}")
        download_and_play_audio(audio_url)
    else:
        print("音频生成失败")


final_text = ''.join(filtered_text)
name_text = ''.join(name_text)
print(final_text)
print(name_text)
cuttedimage.show()
persoimage.show()
main()
"""

# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   合成小语种需要传输小语种文本、使用小语种发音人vcn、tte=unicode以及修改文本编码方式
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
from websocket import WebSocketApp

import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(message)
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:

            with open('./demo.pcm', 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        d = {"common": wsParam.CommonArgs,
             "business": wsParam.BusinessArgs,
             "data": wsParam.Data,
             }
        d = json.dumps(d)
        print("------>开始发送文本数据")
        ws.send(d)
        if os.path.exists('./demo.pcm'):
            os.remove('./demo.pcm')

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # 测试时候在此处正确填写相关信息即可运行
    wsParam = Ws_Param(APPID='628045d2', APISecret='ZWNiOTBkNjQyMTkxMDQxMGI0NGJiNGJi',
                       APIKey='6445f4c33fd07566ca17b90ca5535b14',
                       Text=final_text)
    websocket.enableTrace(True)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
"""
