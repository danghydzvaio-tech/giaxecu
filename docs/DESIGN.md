# Thiết kế AutoValue India

## 1. Mục tiêu và nội dung

Công cụ ước tính giá ô tô cũ **Ấn Độ**, giao diện tiếng Việt, đơn vị **INR (₹)**. Luồng: nhập xe → dự đoán → xem giá/khoảng → tải CSV. Dữ liệu lịch sử CarDekho có năm sản xuất tối đa 2020 và không có ngày quan sát từng tin; kết quả không đại diện giá rao bán hiện tại.

Thứ tự thực tế: navbar → hero → phạm vi → form → kết quả khi có → gallery mặc định đóng → dữ liệu tham chiếu → giới thiệu → ghi công người sáng lập. Form ở ngay dưới hero để đến bước nhập liệu sau một lần cuộn ngắn trên điện thoại. Không thêm tài khoản, thanh toán, huấn luyện trên web hoặc số liệu marketing giả.

Dòng phạm vi: “Giá tham khảo thị trường xe cũ Ấn Độ (INR), dựa trên dữ liệu lịch sử CarDekho đến năm 2020, không phải giá rao bán hiện tại.”

## 2. Màu sắc, chữ và bề mặt

| Vai trò | Giá trị |
|---|---|
| Nâu chính | `#5B4632` |
| Nâu tối | `#3A2C1F` |
| Vàng kem | `#F4D9A0` |
| Cam đất | `#C8792C` |

Nền gradient nâu có vùng sáng cam bên phải. Hero dùng serif Cormorant Garamond/Georgia; nội dung Inter và tiêu đề phụ Sora có fallback. Chỉ nhãn ngắn/kicker/badge viết hoa; mô tả dài và footer giữ cách viết câu, cỡ tối thiểu 12px. Giá lớn có INR đầy đủ và tương đương lakh/crore.

Card/khung kính mờ, nền nâu trong suốt, viền vàng kem mảnh, bo góc 16–20px và bóng mềm. Giữ widget Streamlit để có bàn phím, label, trợ giúp và kiểm tra đầu vào. Focus rõ; cảnh báo có chữ, không chỉ dựa vào màu.

`assets/theme.css` quản lý nền/bố cục/hero/widget/bảng/responsive; `ui_effects.css` quản lý kính/viền/reveal; `navbar.css` quản lý điều hướng. Python đọc CSS từ tệp. `.streamlit/config.toml` đặt cùng palette để widget và các vùng mặc định thống nhất.

## 3. Ảnh và hiệu năng ban đầu

Hero dùng **`static/cars/kwid.webp` (252.066 byte)** có sẵn trong catalog, thay PNG lớn. Nhúng data URL từ byte cục bộ đã cache, tránh hotlink và lỗi đường dẫn qua khung Cloud `/~/+/`.

Gallery sau kết quả trong `st.expander` mặc định đóng. Chỉ sinh sáu ảnh khi mở; `loading="lazy"` trì hoãn giải mã ảnh ngoài vùng nhìn. Lúc đầu chỉ nhúng hero, dưới mục tiêu 500 KB. Mỗi ảnh có tên xe, giá nguồn lịch sử, nguồn, tác giả và giấy phép. Ảnh cùng dòng/thế hệ, không xác nhận chính phương tiện hoặc mọi phiên bản động cơ của bản ghi.

Nguồn/giấy phép giữ tại `static/cars/catalog.json` và [IMAGE_CREDITS.md](IMAGE_CREDITS.md). Không sửa metadata nguồn để hợp thức hóa ảnh chưa xác minh.

| Chỉ tiêu render ban đầu | Trước | Sau |
|---|---:|---:|
| HTML desktop 1440px | 6.338.772 byte | 481.139 byte |
| HTML mobile 390px | 6.331.586 byte | 474.045 byte |
| Byte ảnh ô tô nhúng duy nhất | 4.635.983 byte | 252.066 byte |

HTML là UTF-8 chưa nén của `stMainBlockContainer.outerHTML` sau khởi tạo, trước dự đoán/gallery; không phải HTTP shell hoặc byte mạng nén. Form bắt đầu khoảng 672px desktop/674px mobile, không có cuộn ngang trong lần đo. Chưa có đo Lighthouse/4G đủ điều kiện so sánh.

## 4. Điều hướng và chuyển động

`navbar.html` có ba mục **Định giá**, **Dữ liệu tham chiếu**, **Giới thiệu**, icon SVG, nhãn truy cập, `aria-current` và focus rõ. Desktop dùng pill nổi; dưới 768px chuyển thành dock đáy tôn trọng safe-area. Cloud chừa thêm khoảng cho điều khiển nền tảng.

`navbar.js` quản lý scroll-spy, indicator và cuộn tới section; navbar thu nhỏ theo hướng cuộn. `ui_effects.js` quản lý tiến trình, parallax nhẹ vùng sáng và reveal bằng IntersectionObserver. MutationObserver xử lý DOM mới khi Streamlit rerun; bộ điều khiển có phiên bản và hàm dọn listener/observer để tránh nhân đôi.

Một HTML component cao 0 bootstrap hai bộ điều khiển vào cửa sổ Streamlit cùng origin; script khởi tạo tự gỡ. Bước này vẫn dùng `window.parent` vì `st.html()` lọc script trong ứng dụng thực tế. Hạn chế còn một bootstrap, chỉ nạp mã cục bộ tin cậy và tái sử dụng bộ điều khiển; không tuyên bố đã bỏ mọi thao tác với cửa sổ cha.

CSS dùng conic-gradient/`@property` cho viền sáng, transform/opacity cho reveal và hover. Mobile giảm blur lồng nhau. `prefers-reduced-motion` tắt animation/chuyển cảnh/parallax. Không có con trỏ tùy chỉnh, loading giả, thư viện chuyển động ngoài hoặc JavaScript do người dùng cung cấp. JavaScript không tính giá hoặc quyết định nghiệp vụ.

## 5. Kết quả và cách đối chiếu

Hàm chung `price_format.py`: `450000 → ₹4,50,000`, `9999999 → ₹99,99,999`, từ `10000000 → ₹1,00 crore`. Chú giải **1 lakh = ₹1,00,000; 1 crore = 100 lakh**. Trục năm dùng số nguyên (`2011`); giá trên trục/tooltip/bảng nhóm kiểu Ấn Độ. CSV giữ số INR để xử lý tiếp.

Kết quả có một giá trung tâm lớn, bỏ metric “Giá dự đoán” lặp lại. Dưới giá là hai cận mục tiêu phủ 80%, độ phủ thực đo, sai số phần trăm và đơn vị gọn. Cảnh báo “độ tin cậy thấp” khi hãng có dưới 10 mẫu huấn luyện hoặc giá dự đoán trên 10 lakh; giữ cảnh báo cấu hình ít mẫu/thông số ngoài phạm vi.

Dải lịch sử cùng cấu hình ưu tiên năm ±2. Dưới 5 mẫu thì dùng toàn bộ mẫu cùng cấu hình và nói rõ. Miền thanh bao gồm giá dự đoán để marker không bị cắt. Dải lịch sử khác khoảng conformal, có chú thích phân biệt. CSV gồm giá giữa, cận dưới/cận trên và mức phủ mục tiêu.

## 6. Mô hình và tính đúng đắn

Python 3.12, Streamlit, pandas, NumPy, scikit-learn và joblib; giữ phiên bản `requirements.txt`. Khi mở app chỉ nạp mô hình sẵn, không gọi Kaggle hoặc huấn luyện. `service.py` xác minh hash, kiểm tra đầu vào và phục vụ dự đoán; `car_model.py` giữ tiền xử lý/inference/conformal.

6.904 dòng sau làm sạch chia theo nhóm tên/năm/km/nhiên liệu/hộp số: **4.423 fit, 1.101 hiệu chỉnh, 1.380 test**. GroupKFold 5 lần so sánh MLP, Random Forest và HistGradientBoosting trên **4.423 dòng fit**; hiệu chỉnh không chọn mô hình hoặc epoch. MLP có validation nhóm nội bộ, rồi refit toàn bộ phần đang huấn luyện. MLP được chọn bằng MAE trung bình CV thấp nhất, không bằng test.

Conformal dùng phần dư tuyệt đối `log1p(INR)` trên 1.101 dòng hiệu chỉnh, thứ hạng `ceil((n+1)×0,8)=882`, bán kính log 0,2428267926. Sau khi cố định mô hình/khoảng, test báo MAE **₹79,468.32**, MAPE **16,2850%**, sai số % trung vị **12,0560%**, R² **0,9084**, độ phủ **78,9855%**. MAE/MAPE tăng nhẹ so với trước; không mô tả là cải thiện toàn diện độ chính xác.

80% là mục tiêu phủ tổng thể dưới giả định dữ liệu tương đồng, không bảo đảm từng xe/hãng/phân khúc. Dưới 3 lakh thực đo chỉ phủ **70,78%**. Thiếu VIN/ngày tin/tình trạng; bản đăng lại và thay đổi thị trường có thể ảnh hưởng sai số/độ phủ. R² không phải “phần trăm chính xác”.

`train.py` kiểm tra nguồn Kaggle version 4/SHA-256, chạy CV/huấn luyện/hiệu chỉnh/báo cáo và sinh toàn bộ artifact; `build_manifest.py` ghi hash bảy tệp. Không sửa thủ công artifact. Tải ZIP không cắt ở 10 MiB; phản hồi thiếu độ dài hoặc ZIP hỏng được báo rõ khi phát hiện.

## 7. Tiêu chí kiểm chứng

- 27 kiểm tra unit/AppTest: hash, hồi quy mô hình, nhóm/CV, conformal, cảnh báo, INR/lakh/crore, ảnh, form và tải ZIP đầy đủ/cắt cụt.
- CI kiểm tra cú pháp hai tệp JS đang dùng và test Python 3.12; xem kết quả đúng commit trước khi kết luận deploy thành công.
- Desktop/tablet/mobile: form ngay dưới hero, không cuộn ngang; gallery đóng không sinh ảnh, mở/đóng không mất kết quả; mọi ảnh giải mã được.
- Giá, khoảng, CSV, marker lịch sử, biểu đồ giữ đúng dữ liệu; năm không phân nhóm hàng nghìn.
- Hiệu ứng/navbar có một bộ điều khiển sau rerun; reduced motion vẫn hiện đủ nội dung; không cản bàn phím hoặc điện thoại.
- Giữ nguyên `DATA_SOURCE.md`, `docs/IMAGE_CREDITS.md`, `static/cars/catalog.json`, phiên bản thư viện và các ghi công/giấy phép.

PDF ANN người dùng gửi chỉ tham khảo thuật toán; không dùng dữ liệu GPA, trọng số hoặc bảng loss trong tài liệu cho mô hình giá xe.
