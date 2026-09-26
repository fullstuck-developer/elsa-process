import os
import sys
import psutil
import keyboard
import threading
import time
import pystray
from PIL import Image, ImageDraw

# Trạng thái Lá chắn tự động
auto_freeze_enabled = False
frozen_pids = set()
icon = None
TARGET_NAMES = ["mb_monitor.exe", "mb monitor agent.exe", "mb_monitor"]

def get_resource_path(relative_path):
    """ Tương thích đường dẫn ảnh khi đóng gói thành .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def create_image(is_safe: bool):
    width = 64
    height = 64
    icon_path = get_resource_path("ice_emoji.png")
    
    if os.path.exists(icon_path):
        try:
            base_image = Image.open(icon_path).convert("RGBA")
            image = base_image.resize((width, height), Image.Resampling.LANCZOS)
        except Exception:
            image = Image.new('RGBA', (width, height), color=(40, 40, 40, 255))
    else:
        image = Image.new('RGBA', (width, height), color=(40, 40, 40, 255))
        
    dc = ImageDraw.Draw(image)
    
    # Chấm trạng thái: Safe = Bật lá chắn (Xanh lá), Danger = Tắt lá chắn (Đỏ)
    dot_color = (0, 255, 0, 255) if is_safe else (255, 0, 0, 255)
    
    # Vẽ chấm to, góc phải
    dc.ellipse([36, 4, 60, 28], fill=dot_color, outline=(255, 255, 255, 255), width=2)
    return image

def auto_monitor_loop():
    """Luồng quét và đóng băng tự động mỗi 2 giây"""
    global auto_freeze_enabled, frozen_pids
    
    while True:
        if auto_freeze_enabled:
            current_pids = set()
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = str(proc.info.get('name', '')).lower()
                    if proc_name in TARGET_NAMES:
                        pid = proc.info['pid']
                        current_pids.add(pid)
                        
                        # Nếu PID này chưa bị đóng băng, tiến hành tóm cổ
                        if pid not in frozen_pids:
                            try:
                                proc.suspend()
                                frozen_pids.add(pid)
                                print(f"[{time.strftime('%X')}] Đã ĐÓNG BĂNG thành công: {proc_name} (PID: {pid})")
                            except psutil.AccessDenied:
                                print(f"[{time.strftime('%X')}] LỖI: Không đủ quyền (Access Denied) để đóng băng {proc_name} (PID: {pid}). Hãy chạy bằng quyền Administrator!")
                            except Exception as e:
                                print(f"[{time.strftime('%X')}] LỖI đóng băng {proc_name} (PID: {pid}): {e}")
                except (psutil.NoSuchProcess, AttributeError):
                    pass
                    
            # Dọn dẹp bộ nhớ: xóa các PID không còn tồn tại
            dead_pids = frozen_pids - current_pids
            for d_pid in dead_pids:
                print(f"[{time.strftime('%X')}] Đối tượng (PID: {d_pid}) đã biến mất. Ngừng tracking.")
            frozen_pids.intersection_update(current_pids)
        time.sleep(2)

def toggle_target(item=None):
    """Công tắc Tắt/Bật toàn bộ Lá chắn Tự động"""
    global auto_freeze_enabled, frozen_pids, icon
    auto_freeze_enabled = not auto_freeze_enabled
    
    if auto_freeze_enabled:
        print(f"\n[{time.strftime('%X')}] >>> LÁ CHẮN AUTO-FREEZE ĐÃ BẬT <<<")
    else:
        print(f"\n[{time.strftime('%X')}] >>> LÁ CHẮN AUTO-FREEZE ĐÃ TẮT <<<")
    
    # Tương tác ngay lập tức với các tiến trình đang có
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = str(proc.info.get('name', '')).lower()
            if proc_name in TARGET_NAMES:
                pid = proc.info['pid']
                if auto_freeze_enabled:
                    if pid not in frozen_pids:
                        try:
                            proc.suspend()
                            frozen_pids.add(pid)
                            print(f"[{time.strftime('%X')}] (Thủ công) Đã ĐÓNG BĂNG: {proc_name} (PID: {pid})")
                        except psutil.AccessDenied:
                            print(f"[{time.strftime('%X')}] LỖI: Access Denied khi đóng băng {proc_name} (PID: {pid}). Chạy lại bằng Administrator!")
                        except Exception as e:
                            print(f"[{time.strftime('%X')}] LỖI đóng băng {proc_name} (PID: {pid}): {e}")
                else:
                    try:
                        # Gọi resume nhiều lần để đảm bảo xoá sạch Suspend Count (nếu > 1)
                        for _ in range(3):
                            proc.resume()
                        
                        frozen_pids.discard(pid)
                        print(f"[{time.strftime('%X')}] (Thủ công) Đã RÃ ĐÔNG: {proc_name} (PID: {pid})")
                    except psutil.AccessDenied:
                        print(f"[{time.strftime('%X')}] LỖI: Access Denied khi rã đông {proc_name} (PID: {pid}). Chạy lại bằng Administrator!")
                    except Exception as e:
                        print(f"[{time.strftime('%X')}] LỖI rã đông {proc_name} (PID: {pid}): {e}")
        except (psutil.NoSuchProcess, AttributeError):
            pass
            
    # Cập nhật Icon
    if icon is not None:
        icon.icon = create_image(is_safe=auto_freeze_enabled)

def check_target_exists():
    for proc in psutil.process_iter(['name']):
        try:
            proc_name = str(proc.info.get('name', '')).lower()
            if proc_name in TARGET_NAMES:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            pass
    return False

def get_status_text(item):
    if check_target_exists():
        return "👀"
    else:
        return "👻"


def get_shield_text(item):
    return "ĐÓNG BĂNG (Ctrl + Alt + X)" if auto_freeze_enabled else "RÃ ĐÔNG (Ctrl + Alt + X)"

def do_nothing(icon, item):
    pass

def keyboard_listener():
    keyboard.add_hotkey('ctrl+alt+x', toggle_target)
    keyboard.wait()

def quit_app(icon, item):
    # Rã đông tất cả trước khi thoát
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            if pid in frozen_pids:
                for _ in range(3):
                    proc.resume()
                print(f"[{time.strftime('%X')}] Đã rã đông PID: {pid} trước khi thoát.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            pass
    
    icon.stop()
    os._exit(0)

def main():
    global icon
    print("Elsa Auto-Freeze Shield is starting...")
    
    # Khởi chạy các luồng ngầm
    threading.Thread(target=keyboard_listener, daemon=True).start()
    threading.Thread(target=auto_monitor_loop, daemon=True).start()
    
    # Mặc định tắt lá chắn (Chấm đỏ)
    icon_image = create_image(is_safe=False)
    
    menu = pystray.Menu(
        pystray.MenuItem(get_status_text, do_nothing),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(get_shield_text, toggle_target, default=True),
        pystray.MenuItem("Thoát", quit_app)
    )
    
    icon = pystray.Icon("Elsa", icon_image, "Elsa Auto-Freeze Shield", menu)
    icon.run()

if __name__ == "__main__":
    main()
