# AutoValue Premium UI — DEMO

Nhánh `premium-ui-demo-v2` là bản demo giao diện độc lập. Mọi mức giá dùng công thức giả lập; app không nạp mô hình ANN và không cung cấp báo giá thị trường. Nhánh main vẫn giữ ứng dụng ANN thật.

## Chạy cục bộ

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Mở trình duyệt và kiểm tra nhãn `PREMIUM-DEMO-2.0`. Trong năm 2026, thông số mặc định cho kết quả giả lập ₹417,000. CSV có cột demo_only=True.

## Deploy demo lên Community Cloud

1. Chọn repo danghydzvaio-tech/giaxecu, branch premium-ui-demo-v2, Main file path app.py; dùng Python 3.12. File .streamlit/config.toml nằm ngay thư mục gốc repo.
2. Sau khi deploy hoặc thay đổi cấu hình, mở Manage app → menu → Reboot app và xem logs.
3. Mở tab mới/Ctrl+F5; kiểm tra nhãn PREMIUM-DEMO-2.0. Nếu chưa có nhãn, kiểm tra lại branch, Main file path và log. Xóa cache dữ liệu không khắc phục việc chọn sai entrypoint.

Để giữ link ANN thật hiện tại, tạo một deployment demo riêng. Chỉ chuyển deployment hiện tại sang nhánh này nếu chủ động muốn chạy công thức giả lập.

## Giao diện

CSS/HTML được chèn trực tiếp trong app.py, dùng selectors data-testid/ARIA và !important. Không cần React/Tailwind hoặc thư viện UI bổ sung. Font Google có fallback; hình ô tô là SVG nhúng. Giao diện hỗ trợ mobile, bàn phím và prefers-reduced-motion.

Ẩn header/menu/footer bên trong ứng dụng; huy hiệu hosted của nền tảng Cloud nằm ngoài khung ứng dụng.
