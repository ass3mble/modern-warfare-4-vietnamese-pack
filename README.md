# Call of Duty: Modern Warfare 4 | Vietnamese Localization

**Bản Việt hóa cộng đồng dành cho Call of Duty: Modern Warfare 4 (2026), gồm 40.085 chuỗi văn bản và bộ cài đặt kiểm tra tính tương thích trước khi thay tệp.**

Dự án tập trung vào lời thoại chiến dịch, phụ đề, mục tiêu nhiệm vụ, giao diện và thuật ngữ trong trò chơi. Mục tiêu là giúp nội dung tiếng Việt dễ hiểu, đúng ngữ cảnh và giữ được nhịp kể chuyện của một trò chơi bắn súng góc nhìn thứ nhất.

Đây là dự án độc lập, miễn phí, không liên kết hoặc được bảo trợ bởi Activision, Infinity Ward hay nhà phát hành trò chơi.

> **Phiên bản công khai trong kho:** V6.157, ngày 24/10/2026. Đây là phiên bản của gói được đăng trong kho này, không phải lời khẳng định rằng nó tương thích với mọi bản cập nhật trò chơi. Gói đã được đối chiếu cấu trúc dữ liệu và kiểm tra cài đặt ngoại tuyến, nhưng chưa kiểm chứng trực tiếp toàn bộ 16 nhiệm vụ chiến dịch.

## Tải bản Việt hóa

**[Tải trọn bộ bản Việt hóa và trình cài đặt](https://github.com/ass3mble/modern-warfare-4-vietnamese-pack/archive/refs/heads/main.zip)**

Trên GitHub, bạn cũng có thể chọn `Code` rồi `Download ZIP`. Sau khi tải, **giải nén toàn bộ** trước khi chạy tệp cài đặt.

## Bản này gồm những gì?

| Thành phần | Nội dung |
| --- | --- |
| Bản dịch | 40.085 chuỗi tiếng Việt trong gói V6.157 |
| Chiến dịch | Lời thoại, phụ đề, mô tả và mục tiêu nhiệm vụ có trong bộ dữ liệu |
| Giao diện | Văn bản và thuật ngữ tương ứng trong bộ dữ liệu |
| Trình cài | Tạo tệp Việt hóa từ dữ liệu gốc phù hợp trên máy người dùng |
| Kiểm tra | Xác minh cấu trúc, dấu vân tay dữ liệu, bản sao lưu và kết quả ghi |
| Khôi phục | Có thể trở về tệp trước khi cài bằng bản sao lưu |

**Giới hạn quan trọng:** Gói không đi kèm bộ nạp Việt hóa, phông chữ thương mại hay các tệp thực thi của trò chơi. Muốn thấy tiếng Việt trong trò chơi, bạn phải có bộ nạp tương thích với `sp26/trdata2.bin`. Trình cài không tự bổ sung bộ nạp.

## Cách cài trên Windows

1. **Thoát trò chơi hoàn toàn.**
2. Đảm bảo bạn có bản trò chơi phù hợp được cài hợp pháp và đã có bộ nạp Việt hóa tương thích.
3. Cài [Python 3](https://www.python.org/downloads/windows/) nếu máy chưa có. Khi cài, có thể bật tùy chọn thêm Python vào đường dẫn hệ thống.
4. Tải và giải nén toàn bộ kho mã nguồn.
5. Nhấp đúp `INSTALL_VIET_HOA.bat`.
6. Chọn **thư mục gốc của trò chơi**, tức thư mục chứa `sp26`. Ví dụ: `F:\Call of Duty - MW 4 (2026)`.
7. Đọc thông báo của trình cài trước khi mở trò chơi để kiểm tra.

Bạn có thể kéo thả thư mục gốc trò chơi vào `INSTALL_VIET_HOA.bat` thay cho việc chọn thư mục bằng hộp thoại.

### Hiểu thông báo của trình cài

- `SUCCESS`: dữ liệu Việt hóa đã được ghi và kiểm tra. Tệp cũ được sao lưu.
- `ALREADY INSTALLED`: tệp hiện tại đã có dấu vân tay SHA-256 trùng với bản phát hành này.
- Nếu dữ liệu nguồn không khớp: trình cài sẽ từ chối ghi để tránh áp một bộ dịch không tương thích.

Đừng cố bỏ qua bước xác minh phiên bản nếu trình cài từ chối. Việc ghép bản dịch sai cấu trúc có thể làm hỏng tệp ngôn ngữ.

## Cách khôi phục bản cũ

1. Thoát trò chơi.
2. Vào thư mục `sp26`.
3. Tìm tệp `trdata2.bin.BACKUP-...` được tạo khi cài.
4. Giữ lại một bản sao an toàn, sau đó khôi phục tệp đã sao lưu về tên `trdata2.bin`.
5. Mở lại trò chơi và kiểm tra.

Không xóa bản sao lưu khi chưa xác nhận trò chơi hoạt động bình thường.

## Tính tương thích và an toàn tệp

Trước khi ghi, trình cài xác minh thứ tự và cấu trúc **40.085 khóa nguồn tiếng Anh**, cùng dấu vân tay SHA-256. Dữ liệu đích được dựng từ tệp gốc có sẵn trên máy người dùng.

Trình cài chỉ cần thay `sp26/trdata2.bin`. Nó không sửa tệp thực thi, thư viện, dữ liệu trò chơi khác hoặc hệ thống chống gian lận. Việc thay tệp được thực hiện sau khi tạo bản sao lưu và kiểm tra dữ liệu ứng viên.

**Dấu vân tay SHA-256 của tệp đã cài V6.157:**

```text
f7279a141946e6f26140386ca2e5bcf46d5f6802585de199938f7790db321ce5
```

**Dấu vân tay SHA-256 của bộ nguồn tiếng Anh tương thích:**

```text
4e67f94799574f55f3398c3223811072741f9b19d75993d7471243ba4333049f
```

Chỉ kiểm tra, không thay tệp:

```powershell
python INSTALL_VIET_HOA.py --game-dir "F:\Call of Duty - MW 4 (2026)" --verify-only
```

Việc thử nghiệm trình cài được thực hiện ngoại tuyến trên bộ dữ liệu khớp cấu trúc. Kết quả đối chiếu tệp và bản sao lưu không thay thế cho việc kiểm thử hiển thị phông chữ, phụ đề và toàn bộ quá trình chơi.

## Các tệp trong kho

| Đường dẫn | Công dụng |
| --- | --- |
| `pack/manifest.json` | Phiên bản, dấu vân tay dữ liệu và danh sách các phần gói |
| `pack/v6157.part00.b64` đến `pack/v6157.part08.b64` | Chín phần dữ liệu văn bản tiếng Việt đã nén |
| `INSTALL_VIET_HOA.bat` | Mở trình cài trên Windows |
| `INSTALL_VIET_HOA.py` | Kiểm tra, dựng tệp, sao lưu, ghi và hậu kiểm |
| `tools/trdata.py` | Công cụ đọc cấu trúc dữ liệu và kiểm tra thay đổi |
| `tests/test_trdata.py` | Kiểm thử trên dữ liệu mô phỏng, không cần tệp trò chơi thương mại |

Kho chỉ phát hành dữ liệu đích bằng tiếng Việt và mã nguồn công cụ do dự án tạo ra. Không phân phối nguyên văn kịch bản tiếng Anh có bản quyền, bộ từ điển gốc, phông chữ độc quyền, thư viện nạp hoặc tệp thực thi của trò chơi.

## Dành cho người muốn đóng góp

Kiểm tra công cụ với dữ liệu mô phỏng:

```powershell
python -m unittest discover -s tests -v
```

Khi góp ý bản dịch, hãy cung cấp mã chuỗi, bản tiếng Việt hiện tại, tình huống trong trò chơi và câu đề xuất. Ưu tiên lỗi làm sai người nói, phủ định, diễn biến câu chuyện và mục tiêu nhiệm vụ.

Xem thêm [hướng dẫn đóng góp](CONTRIBUTING.md), [thông tin an toàn](SECURITY.md) và [giấy phép](LICENSE). Giấy phép MIT chỉ áp dụng cho phần mã nguồn và công cụ gốc của dự án, không áp dụng cho tài sản thuộc bên thứ ba.
