import download_and_play_audio
from cnocr import CnOcr
import capture_genshin_window
import crop_bottom_third_from_variable
import crop_bottom__from_variable
import text_to_speech

def main():
    """
    主函数，用于处理文本转语音，并播放生成的音频。
    """
    # 示例使用
    text = final_text
    audio_url = text_to_speech.text_to_speech(text)

    if audio_url:
        print(f"生成的音频URL: {audio_url}")
        download_and_play_audio.download_and_play_audio(audio_url)
    else:
        print("音频生成失败")

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
final_text = ''.join(filtered_text)
name_text = ''.join(name_text)

# 打印最终的文本和名称
print(final_text)
print(name_text)

# 显示处理过的图像
cuttedimage.show()
persoimage.show()

# 调用主函数
main()
