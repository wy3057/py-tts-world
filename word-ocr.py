import sys
from PIL import Image
import pytesseract
import re
import argparse

def load_image(image_path):
    """
    加载图像文件
    :param image_path: 图像文件路径
    :return: Image对象
    """
    try:
        return Image.open(image_path)
    except IOError as e:
        print(f"无法打开图像文件: {e}")
        sys.exit(1)

def validate_ocr_result(text):
    """
    验证OCR识别结果是否有效
    :param text: OCR识别出的文本
    :return: 布尔值，表示识别结果是否有效
    """
    if not text or text.isspace():
        print("OCR 识别结果为空或无效")
        return False
    return True

def find_target_words(text, target_words):
    """
    在OCR识别结果中查找目标词语
    :param text: OCR识别出的文本
    :param target_words: 目标词语列表
    :return: 找到的目标词语列表
    """
    found_words = []
    for word in target_words:
        if re.search(r'\b' + re.escape(word) + r'\b', text):
            found_words.append(word)
    return found_words

def main(image_path, target_words):
    """
    主函数，执行OCR识别并查找目标词语
    :param image_path: 图像文件路径
    :param target_words: 目标词语列表
    """
    img = load_image(image_path)
    
    # 使用pytesseract进行OCR识别
    text = pytesseract.image_to_string(img, lang='chi_sim')
    
    if not validate_ocr_result(text):
        sys.exit(1)
    
    # 检查识别出的文字中是否包含目标词语
    found_words = find_target_words(text, target_words)
    
    print("识别出的目标词语:", found_words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从图像中识别指定的目标词语")
    parser.add_argument("image_path", help="图像文件路径")
    parser.add_argument("--words", nargs='+', default=['词语1', '词语2', '词语3'], help="目标词语列表")
    
    args = parser.parse_args()
    main(args.image_path, args.words)
