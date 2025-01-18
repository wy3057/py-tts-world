import pygetwindow as gw
import time

def monitor_window_position(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        print(f"Monitoring window: {window_title}")
        while True:
            position = window.topleft
            size = window.size
            print(f"Position: {position}, Size: {size}")
            time.sleep(1)  # 每秒监测一次
    except IndexError:
        print(f"Window with title '{window_title}' not found.")
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    window_title = "原神"  # 替换为你要监测的窗口标题
    monitor_window_position(window_title)