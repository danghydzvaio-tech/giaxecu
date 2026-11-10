# Thiết kế AutoValue India theo 5 bước

## 1. Lên kế hoạch nội dung

Sản phẩm là công cụ định giá ô tô cũ tại Ấn Độ. Giao diện tiếng Việt, kết quả bằng INR/lakh. Người dùng nhập thông tin, bấm dự đoán và nhận giá; không phải học về ANN hoặc chạy huấn luyện.

Thứ tự: giới thiệu ngắn → chọn hãng/phiên bản/cấu hình → nhập năm, km, chủ sở hữu và thông số → nút dự đoán → giá và lưu CSV. Mẫu xe đối chiếu và nguồn dữ liệu nằm trong phần mở rộng. Không có tài khoản, thanh toán, chatbot, trang huấn luyện hoặc dữ liệu xe máy.

## 2. Hệ thống màu

- Navy #15324F: tiêu đề và phần giới thiệu.
- Teal #0F766E: nút hành động chính.
- Nền #F8FAFC, nền phụ #E2E8F0, chữ #0F172A.
- Cảnh báo có nhãn chữ; không chỉ dùng màu để truyền thông tin.

## 3. Chữ và hình ảnh

Dùng Plus Jakarta Sans cho nội dung và Space Grotesk cho tiêu đề qua Google Fonts; luôn có font sans-serif fallback khi mạng chậm hoặc bị chặn. Giá lớn, đơn vị rõ ràng. Hero dùng minh họa SVG tự tạo; không lấy ảnh xe chưa có quyền sử dụng, không để hình trang trí chiếm diện tích biểu mẫu. Bố cục hai/ba cột trên máy tính, xếp dọc trên điện thoại.

## 4. Công nghệ

Python 3.12, Streamlit, pandas, NumPy, scikit-learn MLPRegressor và joblib. Chọn ANN đã huấn luyện sẵn vì phù hợp mục tiêu người dùng nhập thông tin là có kết quả. GitHub quản lý mã và tài nguyên; Streamlit Community Cloud chạy Python. Không cần backend/database riêng trong phạm vi bản đầu.

Mô hình, preprocessing và target scaler được lưu cùng nhau để tránh dùng khác quy trình lúc huấn luyện. SHA-256 phát hiện tài nguyên bị thiếu hoặc sai phiên bản. Không tải dữ liệu hay gọi Kaggle lúc khách truy cập.

## 5. Tiêu chí triển khai hoàn chỉnh

- Repo có app.py, requirements.txt, cấu hình Streamlit và toàn bộ artifacts.
- Đầu vào được kiểm tra; chỉ chọn cấu hình có trong dữ liệu, giới hạn năm của bộ huấn luyện.
- Dự đoán từ ANN thật, không dùng giá giả hay công thức thay thế mô hình.
- Ghi rõ dữ liệu lịch sử; không gọi R² là phần trăm chính xác hoặc MAE là khoảng tin cậy.
- Lưu kết quả CSV, hiển thị tốt trên điện thoại, có hướng dẫn deploy cụ thể.
- Kiểm tra mô hình đã lưu, chỉ số báo cáo và luồng giao diện; tự chạy kiểm tra khi push.

Tài liệu PDF về ANN/GPA được tham khảo để hiểu thuật toán. Không dùng dữ liệu GPA, trọng số hoặc bảng loss trong PDF cho mô hình giá xe. Không yêu cầu người dùng xem các công thức trên web.


## Creative studio

Bản mới bổ sung nền studio ivory, serif Cormorant Garamond và vùng dữ liệu teal đậm. Nội dung ban đầu, bộ mô hình, thông số, liên kết và luồng nhập xe → kết quả → CSV được giữ. Các hiệu ứng không tạo số liệu marketing: hai góc hero dùng số mẫu train-clean/test thật; danh sách dùng giá nguồn lịch sử có ghi chú minh họa SVG.

Các hiệu ứng dùng transform/opacity/filter; nền gallery là các lớp màu tĩnh crossfade opacity. Pin chỉ áp dụng hero do HTML sở hữu. Reduced motion bỏ pin, Lenis và các vòng lặp sway; CDN bị chặn vẫn dùng được biểu mẫu và mở dòng xe.
