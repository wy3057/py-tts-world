import pyautogui
import keyboard
import win32gui
import pygetwindow as gw
from PIL import Image

def capture_specific_window(window_title):
    """
    当鼠标左键按下时，对指定窗口截图，并将截图保存为变量 picture。

    Args:
        window_title (str): 窗口的标题名称。

    Returns:
        PIL.Image.Image: 截图图片。
    """
    # 获取窗口信息
    try:
        target_window = next(win for win in gw.getWindowsWithTitle(window_title) if win.visible)
        x, y, width, height = target_window.left, target_window.top, target_window.width, target_window.height
        print(f"已找到窗口: {window_title}, 坐标: ({x}, {y}), 尺寸: ({width}, {height})")
    except StopIteration:
        print(f"未找到窗口: {window_title}")
        return None

    print("准备开始截图，请按鼠标左键以截图，按 'q' 键退出监听。")
    picture = None

    while True:
        # 检测退出条件
        if keyboard.is_pressed('q'):
            print("退出监听。")
            break

        # 检测鼠标左键按下
        if keyboard.is_pressed('o'):
            print("检测到o键按下，正在截图...")
            # 截图指定窗口区域
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            picture = screenshot
            print("截图完成！")
            # 退出循环
            break

    return picture

# 调用函数
window_title = "原神"  # 指定窗口标题
picture = capture_specific_window(window_title)

#if picture:
  #  picture.show()  # 显示截图
