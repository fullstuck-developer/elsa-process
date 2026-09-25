# Elsa Auto-Freeze Shield

Một tiện ích hệ thống (chạy ngầm dưới system tray) giúp tự động phát hiện và đóng băng (suspend) các tiến trình mục tiêu như `mb_monitor`. 

## 🌟 Tính Năng
- **Quét Tự Động**: Liên tục quét hệ thống mỗi 2 giây để tìm và tự động đóng băng các tiến trình trong danh sách mục tiêu.
- **Biểu Tượng Hệ Thống (System Tray)**: Giao diện tối giản chạy ngầm.
  - 🟢 **Chấm Xanh**: Lá chắn đang BẬT (Băng giá - Đóng băng mục tiêu).
  - 🔴 **Chấm Đỏ**: Lá chắn đang TẮT (Bình thường).
- **Phím Tắt Nhanh**: Dễ dàng bật/tắt (Đóng Băng/Rã Đông) bằng tổ hợp phím `Ctrl + Alt + X` từ bất cứ đâu.
- **Trạng Thái Thông Minh**: Menu hiển thị trạng thái `👀` (Nếu mục tiêu đang chạy ngầm) hoặc `👻` (Nếu không có bóng dáng mục tiêu).

## 🎯 Danh Sách Mục Tiêu (Mặc Định)
- `mb_monitor.exe`
- `mb monitor agent.exe`
- `mb_monitor`

## ⚙️ Cài Đặt

### 1. Yêu cầu môi trường
- Python 3.x
- Quyền Administrator (đôi khi cần thiết để can thiệp vào các process của hệ thống).

### 2. Cài đặt thư viện
Cài đặt các gói phụ thuộc thông qua `pip`:
```bash
pip install psutil keyboard pystray Pillow
```

## 🚀 Hướng Dẫn Sử Dụng
1. Chạy mã nguồn Python:
   ```bash
   python main.py
   ```
2. Ứng dụng sẽ xuất hiện một biểu tượng hình bông tuyết (hoặc hình vuông xám nếu thiếu file ảnh `ice_emoji.png`) dưới khay hệ thống (System Tray góc phải màn hình).
3. Nhấp chuột phải vào biểu tượng để xem menu:
   - **ĐÓNG BĂNG / RÃ ĐÔNG**: Chuyển đổi trạng thái bằng tay.
   - **Thoát**: Tắt hoàn toàn ứng dụng.
4. **Sử dụng phím tắt**: Nhấn `Ctrl + Alt + X` bất kỳ lúc nào để chuyển trạng thái một cách nhanh chóng.

## 📦 Hướng Dẫn Đóng Gói (Build .exe)
Nếu muốn đóng gói ứng dụng này thành file thực thi `.exe` độc lập trên Windows (không cần cài Python):
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=ice_emoji.png --add-data "ice_emoji.png;." main.py
```
*(Lưu ý: Bạn cần có sẵn một file ảnh `ice_emoji.png` cùng thư mục với mã nguồn để ứng dụng hiển thị biểu tượng đẹp nhất)*
