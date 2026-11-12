# AutoValue India — Dự đoán giá ô tô cũ bằng AI

Ứng dụng Streamlit bằng tiếng Việt: nhập thông tin ô tô, nhận giá tham khảo bằng **INR (₹)**, khoảng dự đoán và tệp CSV. Mô hình đã huấn luyện sẵn; khách truy cập không cần tài khoản Kaggle, tải CSV hoặc huấn luyện khi mở web.

**Phạm vi:** thị trường xe cũ Ấn Độ, dữ liệu lịch sử CarDekho có năm sản xuất đến **2020**, không có ngày quan sát từng tin. Kết quả không đại diện giá rao bán hiện tại. Không dùng Excel của người dùng hoặc dữ liệu xe máy.

- Kho mã: https://github.com/danghydzvaio-tech/giaxecu
- Website: https://dudoangiaxecu-danghuy.streamlit.app/
- [Nguồn dữ liệu và giấy phép](DATA_SOURCE.md) · [Ghi công ảnh](docs/IMAGE_CREDITS.md) · [Thiết kế](docs/DESIGN.md)

## Chạy ứng dụng

Dùng **Python 3.12** và giữ nguyên phiên bản trong `requirements.txt`:

```bash
git clone https://github.com/danghydzvaio-tech/giaxecu.git
cd giaxecu
python -m venv .venv
```

Kích hoạt bằng `.venv\Scripts\Activate.ps1` trên Windows PowerShell hoặc `source .venv/bin/activate` trên macOS/Linux, rồi chạy:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Để deploy, mở https://share.streamlit.io/, chọn kho `danghydzvaio-tech/giaxecu`, nhánh `main`, **Main file path: `app.py`**, Python **3.12**, rồi bấm Deploy. Cấu hình theme nằm tại **`.streamlit/config.toml` ở gốc kho**. Giữ đủ `artifacts/`, `assets/`, `static/cars/` và các tệp giao diện. Không cần API key/Secrets để khởi chạy; ứng dụng cần Python nên không triển khai bằng GitHub Pages.

## Luồng sử dụng và giao diện

1. Hero dùng ảnh Renault Kwid WebP có ghi công; dưới hero là phạm vi dữ liệu lịch sử và form nhập xe.
2. Chọn hãng, phiên bản, nhiên liệu/hộp số có trong tập huấn luyện. Kiểm tra năm, km, chủ sở hữu, người bán và thông số gợi ý.
3. Bấm **Dự đoán giá xe** để xem giá trung tâm, khoảng dự đoán có mục tiêu phủ 80%, cảnh báo và tải CSV.
4. Dải giá lịch sử cùng cấu hình ưu tiên năm trong khoảng ±2; dưới 5 mẫu thì dùng toàn bộ mẫu cùng cấu hình và ghi rõ. Vạch sáng đánh dấu giá dự đoán.
5. Bộ sưu tập **Những chiếc xe trong dữ liệu** mặc định đóng; sáu ảnh gallery chỉ được tạo và nhúng khi mở. Dữ liệu tham chiếu và giới thiệu nằm phía dưới.

Theme nâu **#5B4632**, nâu tối **#3A2C1F**, vàng kem **#F4D9A0**, cam đất **#C8792C**; tiêu đề serif, card kính mờ, viền sáng, thanh tiến trình và hiệu ứng hiện dần. Navbar pill trên desktop chuyển thành dock trên mobile. CSS/JavaScript thuần, không có build tool hoặc thư viện chuyển động. `prefers-reduced-motion` tắt chuyển động; nội dung và biểu mẫu vẫn dùng được khi hiệu ứng không chạy.

JavaScript lấy từ tệp tin cậy trong kho. Một HTML component cao 0 chỉ bootstrap hai bộ điều khiển vào cửa sổ Streamlit cùng origin; script khởi tạo tự gỡ và bộ điều khiển có phiên bản để tái sử dụng observer khi rerun. Vẫn có thao tác với `window.parent` ở bước bootstrap vì `st.html()` lọc script trong ứng dụng thực tế; không tuyên bố đã loại bỏ hoàn toàn việc này. Không có con trỏ tùy chỉnh, màn hình loading giả hoặc mã giao diện do người dùng nhập.

Ảnh lưu cục bộ và nhúng bằng data URL để tránh lỗi đường dẫn static qua khung Cloud. Nguồn, tác giả, giấy phép và ánh xạ dòng xe giữ tại `static/cars/catalog.json` và [IMAGE_CREDITS.md](docs/IMAGE_CREDITS.md). Ảnh minh họa cùng dòng/thế hệ, không xác nhận chính chiếc xe hoặc mọi phiên bản trong bản ghi giá.

## Quy ước hiển thị giá

`price_format.py` dùng chung cho kết quả, mẫu lịch sử, bảng và biểu đồ:

| INR gốc | Hiển thị đầy đủ | Đơn vị gọn |
|---:|---|---|
| 450000 | ₹4,50,000 | ₹4,50 lakh |
| 9999999 | ₹99,99,999 | ₹99,99 lakh |
| 10000000 | ₹1,00,00,000 | ₹1,00 crore |
| 12500000 | ₹1,25,00,000 | ₹1,25 crore |

**1 lakh = ₹1,00,000; 1 crore = 100 lakh.** Dạng gọn dùng dấu phẩy thập phân theo giao diện tiếng Việt. Chuyển sang crore theo giá thật, không theo số làm tròn. CSV giữ giá dạng số INR; trục năm dùng số nguyên như `2011`, không phân nhóm hàng nghìn.

## Dữ liệu và chọn mô hình

Nguồn duy nhất: **Nehal Birla — Vehicle dataset**, Kaggle **version 4**, tệp **Car details v3.csv**:

https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho

| Bước | Số dòng |
|---|---:|
| CSV ban đầu | 8.128 |
| Ngoài phạm vi ô tô con hoặc tên chưa xác minh, đã loại | 23 |
| Trùng hoàn toàn, đã loại | 1.201 |
| Sau làm sạch | **6.904** |
| Huấn luyện/chọn mô hình | **4.423** |
| Validation dành riêng cho hiệu chỉnh khoảng | **1.101** |
| Test giữ riêng | **1.380** |

Nhóm theo `name`, `year`, `km_driven`, `fuel`, `transmission` không trùng giữa ba phần. Trong 5.524 dòng phát triển không thuộc test, **chỉ 4.423 dòng fit** tham gia GroupKFold 5 lần; 1.101 dòng hiệu chỉnh được giữ riêng. Ba mô hình dùng cùng fold; tiền xử lý và chuẩn hóa chỉ học từ phần huấn luyện của từng fold. Chọn theo **MAE trung bình CV thấp nhất**, không theo test.

Với MLP, số epoch được chọn bằng validation nhóm nội bộ bên trong phần đang huấn luyện, sau đó refit toàn bộ phần đó. Tập hiệu chỉnh không chọn mô hình, tham số hoặc epoch. MLP cuối dùng **12 epoch**, lớp ẩn **128 → 64**, ReLU, Adam, alpha 0,01 và mục tiêu `log1p(INR)` chuẩn hóa. Đây là ANN của scikit-learn, không dùng TensorFlow/Keras.

### Cross-validation: trung bình ± độ lệch chuẩn

Độ lệch chuẩn mẫu qua 5 fold (`ddof=1`), MAE bằng INR:

| Mô hình | MAE (₹) | MAPE | R² |
|---|---:|---:|---:|
| **MLP — được chọn** | **80.689,67 ± 2.729,16** | **17,49% ± 1,66%** | **0,8953 ± 0,0163** |
| Random Forest | 83.807,52 ± 3.965,39 | 17,80% ± 0,88% | 0,8614 ± 0,0409 |
| HistGradientBoosting | 83.299,67 ± 5.625,04 | 17,30% ± 0,97% | 0,8617 ± 0,0591 |

### Khoảng dự đoán và test cuối

Split conformal dùng phần dư tuyệt đối trên thang `log1p(INR)` của 1.101 dòng hiệu chỉnh. Mục tiêu phủ 80%; lấy phần tử thứ `ceil((1101+1)×0,8)=882` trong dãy phần dư đã sắp xếp, bán kính log **0,2428267926**. Đổi cận về INR bằng `expm1`; khoảng thường không đối xứng quanh giá trung tâm.

Sau khi chọn mô hình và hiệu chỉnh, test được dùng một lần cho báo cáo cuối của quy trình này:

| Chỉ số trên 1.380 dòng test | Kết quả |
|---|---:|
| MAE | ₹79,468.32 |
| RMSE | ₹1,50,432.18 |
| MAPE | 16,2850% |
| Sai số % tuyệt đối trung vị | 12,0560% |
| R² | 0,9084 |
| Độ phủ khoảng thực đo | **78,9855%** |

MAE/MAPE tăng nhẹ so với bản trước (₹79,131.21 và 16,2168%); R² tăng từ 0,9047. Không khẳng định chính xác hơn ở mọi tiêu chí và không tinh chỉnh tiếp theo kết quả test.

| Phân khúc giá thật | Số mẫu test | MAPE | Độ phủ |
|---|---:|---:|---:|
| Dưới 3 lakh | 438 | 20,23% | **70,78%** |
| 3–6 lakh | 519 | 15,10% | 81,50% |
| 6–10 lakh | 327 | 12,47% | 86,24% |
| Trên 10 lakh | 96 | 17,69% | 78,13% |

80% là **mục tiêu phủ tổng thể**, không bảo đảm riêng từng xe/hãng/phân khúc. Conformal cần giả định dữ liệu tương lai tương đồng và có tính hoán đổi; chia nhóm, bản đăng lại chưa nhận diện và thay đổi thị trường có thể ảnh hưởng độ phủ. Phân khúc dưới 3 lakh chỉ phủ khoảng 70,8%. R² không phải phần trăm chính xác. App cảnh báo **độ tin cậy thấp** nếu hãng có dưới 10 mẫu huấn luyện hoặc giá dự đoán trên 10 lakh.

## Huấn luyện lại và tính toàn vẹn

```bash
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python train.py
python build_manifest.py
python -m unittest discover -s tests -v
```

Trên Windows có thể chạy `python train.py`; script cũng giới hạn thread tính toán. Script tải ZIP Kaggle công khai version 4, đọc toàn bộ phản hồi, kiểm tra độ dài nếu có `Content-Length` và báo rõ ZIP lỗi/cắt cụt. Chỉ đọc `Car details v3.csv`, xác minh SHA-256 trước khi huấn luyện:

```text
1b2a30b2f36fd246366773fe5375399692f1a113890ad2a6d464b8c8deaadadb
```

Nếu đã tải đúng CSV từ Kaggle:

```bash
python train.py --source-csv "/path/to/Car details v3.csv"
python build_manifest.py
```

`train.py` sinh toàn bộ tài nguyên trong `artifacts/`, cập nhật giá kỳ vọng cho các đầu vào cố định trong `tests/prediction_examples.json`, rồi ghi manifest. Lệnh `build_manifest.py` ghi lại cùng bảng hash một cách tường minh. **Không sửa thủ công artifact hoặc đổi hash để che lỗi mô hình.** Thay mô hình phải chạy lại quy trình, kiểm thử và commit trọn bộ tài nguyên. `service.load_assets()` xác minh SHA-256 của bảy tệp trước khi nạp; manifest đổi cũng làm mới cache mô hình trong app.

Không đọc Excel, tạo dữ liệu giả hoặc đưa xe đời 2021 trở đi vào huấn luyện. Nguồn/hash sai thì dừng, không thay bằng dữ liệu mẫu. Bộ dữ liệu gốc không đưa vào kho. Phát triển tiếp cần dùng CV để chọn và dành một test độc lập mới, tránh tối ưu lặp lại trên test đã công bố.

## Cấu trúc mã đang dùng

```text
app.py                         # Layout Streamlit, form, kết quả, biểu đồ
assets/theme.css               # CSS nền, hero, widget và responsive
ui_effects.css / ui_effects.js  # Kính mờ, viền sáng, reveal, tiến trình, parallax
navbar.html / .css / .js        # Navbar pill/dock, icon, scroll-spy
price_format.py                # INR kiểu Ấn Độ, lakh/crore, nhãn biểu đồ
service.py                     # Hash, đầu vào, dự đoán, đối chiếu
car_model.py                   # Làm sạch, tiền xử lý, inference, conformal
train.py                       # Kiểm tra nguồn, CV, huấn luyện, báo cáo
build_manifest.py              # SHA-256 cho bộ tài nguyên
photo_catalog.py               # Ghép ảnh xác minh với dữ liệu tham chiếu
requirements.txt               # Phiên bản thư viện triển khai
.streamlit/config.toml         # Theme nâu/cam local và Cloud
artifacts/
  ann_bundle.joblib            # Mô hình + preprocessing/scaler/conformal
  manifest.json                # Hash của 7 tệp còn lại
  evaluation.json              # CV, test, độ phủ, sai số theo phân khúc
  reference.csv                # Chỉ 4.423 dòng huấn luyện
  training_history.csv         # Epoch nội bộ/refit, thời gian fit
  holdout_predictions.csv      # Giá thật, giá giữa, hai cận và sai số test
  split_indices.npz            # Chỉ số ba phần, hash nhóm, fold CV
  verification.json           # Biên bản xác minh quy trình
static/cars/
  catalog.json                 # Ánh xạ dòng xe, nguồn, tác giả, giấy phép
  *.webp                       # 6 ảnh cục bộ; hero dùng lại kwid.webp
tests/                         # Unit test, AppTest, ví dụ dự đoán cố định
.github/workflows/checks.yml   # Python 3.12, kiểm tra JS, test khi push/PR
docs/DESIGN.md                 # Thiết kế và tiêu chí kiểm chứng
docs/IMAGE_CREDITS.md           # Nguồn và giấy phép từng ảnh
DATA_SOURCE.md                 # ODbL/Database Contents License và ghi công
```

Không còn frontend tĩnh riêng; CSS dài đã tách khỏi Python. Tệp giao diện không sử dụng và bước kiểm tra JavaScript cũ đã bỏ.

## Kiểm tra và đo trước/sau

```bash
node --check ui_effects.js
node --check navbar.js
python -m unittest discover -s tests -v
```

Bộ kiểm tra hiện có **27 test**: hash, hồi quy mô hình, nhóm/CV, conformal, cảnh báo, định dạng giá, ảnh, giao diện và tải ZIP trên 10 MiB/thiếu byte. GitHub Actions chạy khi push `main`, có pull request hoặc chạy thủ công. Test local đạt không thay thế việc xem CI của đúng commit triển khai.

| Chỉ tiêu | Trước | Sau |
|---|---:|---:|
| HTML nội dung ban đầu, desktop 1440px | 6.338.772 byte | 481.139 byte |
| HTML nội dung ban đầu, mobile 390px | 6.331.586 byte | 474.045 byte |
| Byte ảnh ô tô nhúng duy nhất lúc đầu | 4.635.983 byte | 252.066 byte |
| MAE test (INR) | 79.131,21 | 79.468,32 |
| MAPE test | 16,2168% | 16,2850% |
| Độ phủ khoảng test | Chưa có | 78,9855% |

HTML là UTF-8 chưa nén của `stMainBlockContainer.outerHTML` sau khởi tạo, trước dự đoán/gallery; không phải phản hồi HTTP tĩnh hoặc byte mạng nén. Byte ảnh là tổng byte ảnh cục bộ duy nhất nhúng trong trạng thái ban đầu. Form bắt đầu tại khoảng 672px trên desktop/674px trên mobile; không có cuộn ngang trong lần đo. Chưa đo Lighthouse hoặc mạng 4G trong cùng điều kiện nên không công bố điểm/tốc độ.

## Xử lý lỗi và giới hạn

- **Web chưa đổi:** kiểm tra đúng repo/nhánh/main file và commit GitHub; xem log ở Manage app rồi **Reboot app** nếu phiên cũ chưa nạp mã mới. Xóa cache trình duyệt không sửa lỗi backend.
- **Hash không khớp/thiếu mô hình:** khôi phục cả `artifacts/` từ cùng commit, không chỉ tải một tệp Python.
- **Lỗi thư viện:** dùng Python 3.12 và giữ `requirements.txt`, nhất là scikit-learn đi cùng mô hình.
- **Ảnh không hiện:** giữ đủ WebP và catalog; app dùng ảnh cục bộ, không phụ thuộc hotlink mạng xã hội.
- **Giới hạn nghiệp vụ:** phân loại ô tô theo tên/ghế, chưa xác thực VIN; thiếu tai nạn/ngập nước/bảo dưỡng/địa phương và giá giao dịch kiểm chứng. Người dùng cần kiểm tra thông số gợi ý.

Tác giả dữ liệu: **Nehal Birla**. Giữ nguyên ghi nguồn/giấy phép trong [DATA_SOURCE.md](DATA_SOURCE.md), [IMAGE_CREDITS.md](docs/IMAGE_CREDITS.md) và catalog. Không công khai PDF tham khảo, ảnh hội thoại hoặc Excel của người dùng trong kho.
