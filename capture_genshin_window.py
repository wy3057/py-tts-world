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
        target_windows = [win for win in gw.getWindowsWithTitle(window_title) if win.visible]
        if not target_windows:
            print(f"未找到窗口: {window_title}")
            return None

        target_window = target_windows[0]  # 选择第一个匹配的窗口
        x, y, width, height = target_window.left, target_window.top, target_window.width, target_window.height
        print(f"已找到窗口: {window_title}, 坐标: ({x}, {y}), 尺寸: ({width}, {height})")
    except Exception as e:
        print(f"获取窗口信息时发生错误: {e}")
        return None

    print("准备开始截图，请按鼠标左键以截图，按 'q' 键退出监听。")
    picture = None

    while True:
        # 检测退出条件
        if keyboard.is_pressed('q'):
            print("退出监听。")
            break

        # 检查当前活动窗口是否为指定窗口
        try:
            active_window = win32gui.GetForegroundWindow()
            active_window_title = win32gui.GetWindowText(active_window)
        except Exception as e:
            print(f"获取活动窗口信息时发生错误: {e}")
            continue

        if active_window_title == window_title:
            # 检测鼠标左键按下
            if keyboard.is_pressed('left'):
                print("检测到鼠标左键按下，正在截图...")
                try:
                    screenshot = pyautogui.screenshot(region=(x, y, width, height))
                    picture = screenshot
                    print("截图完成！")
                    break
                except Exception as e:
                    print(f"截图失败: {e}")
        else:
            print("当前活动窗口不是指定窗口，请将焦点放在指定窗口上。")

    return picture
