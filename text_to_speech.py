import requests
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