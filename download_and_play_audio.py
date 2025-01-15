import pygame
import tempfile
import os
import requests

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
