# 🚗 AutoValue India — Dự đoán giá ô tô cũ bằng ANN

**Nhập thông tin ô tô → bấm “Dự đoán giá xe” → nhận giá bằng ₹ và lakh.**

Ứng dụng Streamlit, giao diện tiếng Việt, dùng ANN đã huấn luyện sẵn trên dữ liệu ô tô tại Ấn Độ tải trực tiếp từ Kaggle. Người dùng không cần tải CSV, tài khoản Kaggle hoặc huấn luyện khi mở web. Không sử dụng file Excel 200 dòng và không đưa xe máy vào bộ huấn luyện.

Kho dự án: https://github.com/danghydzvaio-tech/giaxecu

## Đưa lên Streamlit để có đường dẫn website

1. Đăng nhập https://share.streamlit.io/ bằng tài khoản đã kết nối GitHub.
2. Chọn **Create app / New app → Deploy a public app from GitHub**.
3. Điền chính xác:

   | Mục | Giá trị |
   |---|---|
   | Repository | `danghydzvaio-tech/giaxecu` |
   | Branch | `main` |
   | Main file path | `app.py` |
   | Python, trong Advanced settings | **3.12** |

4. Bấm **Deploy** và đợi cài các thư viện trong `requirements.txt`.
5. Mở đường dẫn Streamlit cấp, nhập thông tin xe và bấm **Dự đoán giá xe**.

**Không chọn GitHub Pages:** ứng dụng cần Python chạy trên Streamlit. Kho có sẵn mô hình và dữ liệu tham chiếu, nên không cần API key hoặc Secrets để khởi chạy. Không xóa thư mục `artifacts/` khi đưa mã lên GitHub.

## Chạy trên máy tính

Cài Python **3.12**, tải hoặc clone kho, rồi mở terminal tại thư mục có `app.py`:

```bash
git clone https://github.com/danghydzvaio-tech/giaxecu.git
cd giaxecu
python -m venv .venv
```

Kích hoạt môi trường:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

Cài và chạy:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Chức năng đã có

- Chọn hãng, phiên bản xe và tổ hợp nhiên liệu/hộp số có trong dữ liệu.
- Nhập năm, số km, lịch sử sở hữu, người bán, dung tích động cơ, công suất và số ghế.
- Tự điền gợi ý thông số theo trung vị mẫu cùng cấu hình; người dùng có thể chỉnh lại.
- Dự đoán bằng ANN đã lưu, đổi kết quả về INR và lakh; lưu kết quả CSV.
- Cảnh báo cấu hình ít mẫu hoặc thông số nằm ngoài phạm vi mẫu tham chiếu.
- Bảng xe lịch sử tương tự nằm trong mục mở rộng, giao diện thích ứng điện thoại.
- Kiểm tra hash của các tệp mô hình trước khi nạp; không nhận pickle/joblib từ người dùng.
- Kiểm tra tự động bằng unittest, Streamlit AppTest và GitHub Actions.

Website giữ luồng nhập liệu → kết quả. Công thức, bảng huấn luyện và biểu đồ loss không đưa vào luồng sử dụng chính.

## Cấu trúc kho

```text
app.py                         # Giao diện Streamlit; chọn tệp này khi deploy
index.html                     # Template hero/header/footer, không thay app.py
style.css                      # Hệ thống thiết kế và responsive
script.js                      # GSAP/ScrollTrigger/Lenis và tương tác
service.py                     # Nạp tài nguyên, kiểm tra đầu vào, gọi ANN
car_model.py                   # Làm sạch dữ liệu và preprocessing/inference
train.py                       # Tải Kaggle v4 và huấn luyện lại
build_manifest.py              # Ghi hash các tài nguyên sau huấn luyện
requirements.txt               # Phiên bản thư viện triển khai
.streamlit/config.toml         # Màu sắc và cấu hình giao diện
artifacts/
  ann_bundle.joblib            # ANN + preprocessing + target scaler + metadata
  manifest.json                # SHA-256 của gói mô hình
  evaluation.json              # Nguồn, cấu hình, chia tập và kết quả kiểm tra
  reference.csv                # Chỉ tập train, dùng cho lựa chọn/gợi ý/đối chiếu
  training_history.csv         # Loss qua từng epoch
  holdout_predictions.csv      # Giá thật và dự đoán của tập kiểm tra
  split_indices.npz            # Chỉ số train/validation/test sau làm sạch
  verification.json           # Biên bản kiểm tra kỹ thuật ban đầu
tests/
  test_app.py                  # Kiểm tra mô hình, đầu vào, giao diện
  prediction_examples.json    # Ví dụ hồi quy để đối chiếu mô hình đã lưu
.github/workflows/checks.yml   # Kiểm tra khi push/PR
docs/
  DESIGN.md                    # Thiết kế theo 5 bước đã thống nhất
DATA_SOURCE.md                 # Nguồn và giấy phép dữ liệu
```

## Dữ liệu và kết quả thực tế

Nguồn: **Nehal Birla — Vehicle dataset**, Kaggle, phiên bản bộ dữ liệu **4**, tệp **Car details v3.csv**.

https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho

| Xử lý | Số dòng |
|---|---:|
| Ban đầu | 8.128 |
| Ngoài phạm vi ô tô con hoặc tên hãng chưa xác minh | 23 |
| Bản ghi trùng hoàn toàn đã loại | 1.201 |
| Còn lại | **6.904** |
| Train | 4.423 |
| Validation | 1.101 |
| Test | 1.380 |

Chỉ dùng hãng ô tô đã nhận diện; loại xe tải/pick-up/Winger và cấu hình ngoài 4–9 ghế khi có số ghế. Giữ 208 dòng thiếu ghế khi thuộc hãng đã nhận diện. Phân loại dựa vào tên/số ghế, không có VIN để kiểm chứng từng phương tiện. Danh sách tên đã loại nằm trong báo cáo.

| Mô hình, cùng tập test | MAE (₹) | RMSE (₹) | R² |
|---|---:|---:|---:|
| **ANN — dùng trên web** | **79.131** | **153.497** | **0,9047** |
| Random Forest — đối chứng | 82.004 | 170.583 | 0,8823 |
| Giá trung vị train — baseline | 278.026 | 512.531 | −0,0629 |

Đây là một lần chia theo nhóm, seed 42. **R² không phải phần trăm chính xác. MAE không phải biên sai số bảo đảm cho từng xe.** Không có khoảng dự đoán được hiệu chỉnh. Các nhóm có cùng tên, năm, km, nhiên liệu và hộp số được giữ riêng giữa train/validation/test. Thiếu mã tin/VIN nên vẫn có thể còn bản đăng lại khác thông số.

## Mô hình ANN

- Mạng truyền thẳng `MLPRegressor` của scikit-learn, lớp ẩn **128 → 64**, ReLU, đầu ra tuyến tính.
- Adam, learning rate 0,001, batch size 64, L2 alpha 0,01.
- Đầu vào số: năm sản xuất, log(1 + km), dung tích cc, công suất bhp, số ghế.
- Phân loại: hãng, tên xe/phiên bản, nhiên liệu, hộp số, lịch sử sở hữu, loại người bán.
- Điền thiếu và chuẩn hóa số; one-hot encoding chỉ học từ train.
- Mục tiêu là log(1 + giá) đã chuẩn hóa; khi dự đoán sẽ đổi ngược về INR.
- Validation chọn thời điểm dừng. Lần huấn luyện đã chạy 34 epoch, lưu trạng thái tốt nhất ở epoch 4. Không dùng test để chọn epoch hoặc tự refit sau đánh giá.
- Dùng ANN của scikit-learn, không phải TensorFlow/Keras; vẫn có các lớp nơ-ron, lan truyền ngược và tối ưu Adam.

## Huấn luyện lại

```bash
python train.py
```

Script tự tải nguồn Kaggle công khai với `datasetVersionNumber=4`, đọc duy nhất `Car details v3.csv`, rồi tạo lại các tệp trong `artifacts/` và `manifest.json`. Bộ dữ liệu gốc không được đưa lên kho. Không đọc file Excel của người dùng. Nguồn không truy cập được thì script báo lỗi, không tự thay bằng dữ liệu giả.

Sau khi đổi mô hình, cần cập nhật `tests/prediction_examples.json` từ các ví dụ kiểm chứng tương ứng, chạy kiểm tra và commit trọn bộ mã/tài nguyên. Nếu chỉnh một tệp tài nguyên có chủ đích, chạy `python build_manifest.py` để tạo lại hash; việc này chỉ cập nhật tính toàn vẹn, không thay cho đánh giá mô hình. Không tiếp tục tối ưu theo cùng tập test; dùng validation/cross-validation trong tập phát triển và một test cuối độc lập.

```bash
python -m unittest discover -s tests -v
```

## Giới hạn và đơn vị giá

- `selling_price` của **v3** được xử lý theo INR. Ví dụ 450000 → ₹450.000 → 4,5 lakh. Không nhân thêm 100.000 như thang giá của tệp `car data.csv` khác.
- Metadata Kaggle tổng quát không định nghĩa đơn vị từng cột; quy ước xử lý v3 được công khai trong báo cáo và `DATA_SOURCE.md`.
- Xe sản xuất **1983–2020**. Website chỉ cho nhập trong phạm vi này. Bộ dữ liệu cập nhật 14/01/2023 không có ngày khảo sát từng tin, vì vậy không đại diện giá thị trường hiện tại.
- Chưa biết tình trạng tai nạn/ngập nước, bảo dưỡng, địa phương hoặc giá giao dịch đã xác thực. Giá nguồn có thể là giá rao bán.
- Thông số gợi ý có thể không đúng xe thực tế; người dùng cần chỉnh trước khi dự đoán.

## Sửa lỗi triển khai thường gặp

- **Không tìm thấy app.py:** chọn `main`, đường dẫn `app.py` ngay tại gốc kho.
- **Không tìm thấy mô hình/hash không khớp:** tải lại đủ `artifacts/` theo cùng commit; không chỉ upload tệp Python.
- **Lỗi thư viện:** dùng Python 3.12 và giữ nguyên `requirements.txt`. Không đổi riêng phiên bản scikit-learn khi dùng mô hình cũ.
- **Web không cập nhật sau push:** mở Manage app trên Streamlit và reboot ứng dụng; xem log để xác định lỗi cụ thể.

## Nguồn và giấy phép

Tác giả dữ liệu: Nehal Birla. Các CSV tham chiếu/kiểm tra là trích xuất và biến đổi từ nguồn Kaggle. Xem `DATA_SOURCE.md` cho ghi công, ODbL và Database Contents License. Không đưa PDF tham khảo, ảnh chụp hội thoại hoặc file Excel của người dùng vào kho công khai.


## Giao diện và chuyển động

Giữ ứng dụng Streamlit và toàn bộ biểu mẫu/kết quả hiện có. Ba tệp `index.html`, `style.css`, `script.js` ở gốc được `app.py` nạp làm lớp giao diện. **Không chọn index.html làm main file trên Streamlit.** Mở riêng HTML chỉ xem được phần khung; chức năng dự đoán vẫn cần chạy `streamlit run app.py`.

- Header cố định có nền kính mờ, ẩn/hiện theo hướng cuộn; menu điện thoại hỗ trợ Escape và giữ focus.
- Hero có ảnh ô tô thật có nguồn/giấy phép, chữ xuất hiện theo dòng, parallax và nút magnetic trên chuột desktop.
- GSAP 3.12.5, ScrollTrigger và Lenis 1.3.4 nạp qua jsDelivr; Google Fonts có font fallback.
- Có thanh tiến trình cuộn, loader ngắn, nút về đầu, hiệu ứng thẻ giá, floating labels và trạng thái gửi form.
- `prefers-reduced-motion` tắt Lenis, loader và các animation; CDN lỗi thì biểu mẫu và dự đoán vẫn chạy.
- Python/ANN, dữ liệu, số liệu đánh giá, tải CSV và bảng đối chiếu được giữ nguyên. Không thêm liên hệ hoặc đối tác không có dữ liệu.
- JavaScript chỉ là mã giao diện tin cậy trong kho. Bootstrap dùng HTML component cùng origin của Streamlit để nạp mã, vì một số frontend Streamlit lọc script trong `st.html`.

Đã kiểm tra luồng dự đoán, giá trị đầu ra và CSV trên trình duyệt ở desktop, tablet, điện thoại, chế độ giảm chuyển động và khi CDN bị chặn. Không công bố điểm Lighthouse vì chưa đo Lighthouse trước/sau trong cùng điều kiện.


## Creative motion — bản nâng cấp

Giữ Streamlit và ANN hiện có. Không có ảnh hoặc tài nguyên sao chép từ template tham khảo.

1. Hero nền studio sáng, chữ Cormorant Garamond serif. `Intl.Segmenter` tách grapheme tiếng Việt; glyph thẳng/italic chồng nhau và chuyển opacity trong khung có chiều rộng cố định. H1 giữ aria-label đầy đủ. Menu pill kính mờ có nền active di chuyển.
2. Tám sprite SVG tự vẽ nở theo quãng đường con trỏ quanh xe, thu sau khi rời vùng 2 giây; gió dừng khi ngoài viewport hoặc tab ẩn. Thiết bị cảm ứng kích hoạt theo cuộn; reduced motion hiển thị tĩnh.
3. ScrollTrigger pin riêng hero HTML do ứng dụng sở hữu, nền teal bo góc 32px của phần tiếp theo phủ lên khi cuộn. Không pin/reparent biểu mẫu hoặc DOM do React của Streamlit quản lý.
4. Sáu dòng xe được lấy trực tiếp từ tập train: giá nguồn lịch sử, không phải giá ANN hay tin đang bán. Nền chuyển bằng lớp màu opacity; ảnh minh họa đổi bằng overflow-hidden + translate thay clip-path. Trên điện thoại hoặc bàn phím, chọn dòng để mở ảnh/mô tả.

Hai số liệu hero là số mẫu sau làm sạch và số mẫu test từ metadata mô hình, không phải khách hàng hoặc mức hài lòng. Ảnh ô tô thật được lưu tại `static/cars/`; 8 sprite trang trí vẫn là SVG tự vẽ trong `index.html`. Nguồn, tác giả, giấy phép và phép ghép ảnh với dữ liệu có trong `static/cars/catalog.json` và `docs/IMAGE_CREDITS.md`.

Các bộ mã hoàn chỉnh nằm ở `index.html`, `style.css`, `script.js`; `app.py` nạp chúng vào Streamlit và xử lý dữ liệu/dự đoán. Mở riêng index.html chỉ xem khung hero/footer, không thay cho `streamlit run app.py`.


Full code giao diện theo thứ tự index.html → style.css → script.js: [docs/FRONTEND_FULL_CODE.md](docs/FRONTEND_FULL_CODE.md).


## Bảng màu và ảnh thật

Giao diện dùng đúng bảng màu mẫu: **#171717** (đen), **#88F9C0** (mint), **#A31C1B** (đỏ rượu vang). Chữ nhỏ ưu tiên trắng/mint để giữ tương phản; đỏ dùng cho CTA/điểm nhấn.

- Hero: Renault Kwid RXT(O) ảnh thật; 6 dòng tham chiếu có ảnh riêng của Swift Dzire, Honda City, Hyundai Eon, Toyota Etios sedan, Ford Figo và Renault Kwid.
- Ảnh được đối chiếu tên dòng/thế hệ với caption tác giả, lưu cục bộ và có ghi công. Không khẳng định ảnh chính là chiếc xe trong bản ghi giá, hoặc đúng mọi trim/động cơ theo từng thị trường.
- Đã tham khảo Pixabay/Pexels/Unsplash người dùng gửi. Ảnh Etios có nguồn gốc Pixabay CC0; các ảnh còn lại chọn metadata rõ từ Commons. Unsplash trả HTTP401 khi tìm kiếm trong phiên.
- `photo_catalog.py` ghép ảnh với tên xe/năm/bản ghi train; không gán ngẫu nhiên ảnh cho mẫu xe chưa xác minh. Khi có ảnh phù hợp, mục đối chiếu kết quả cũng hiển thị ảnh đó.
- `static/cars/catalog.json`: tên ảnh, mẫu/năm tham chiếu, giá nguồn thực tế, SHA-256, tác giả và license.
- `static/cars/*.webp`: sáu ảnh tối ưu kích thước. Giữ chúng trong kho, không hotlink từ site ngoài.
- `.streamlit/config.toml` có `server.enableStaticServing = true`; URL ảnh là `/app/static/cars/...`. Cần **Reboot app** sau khi cập nhật cấu hình theme/static serving.
- Xem [nguồn và giấy phép ảnh](docs/IMAGE_CREDITS.md). Bộ mô hình ANN và artifact đánh giá không thay đổi.
