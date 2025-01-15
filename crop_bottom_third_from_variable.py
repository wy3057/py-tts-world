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
