# Modern Warfare 4 — Vietnamese Localization V6.157

**Full Vietnamese localization content — 40,085 strings.** Free community project; unofficial and not affiliated with Activision, Infinity Ward, or the game's publishers.

The current public package contains the **complete Vietnamese target-text snapshot** of the locally validated V6.157 translation (24 October 2026), distributed as a compressed, source-only overlay. It does **not** contain copyrighted English game scripts, the original paired dictionary, commercial font data, executables, DLLs, fastfiles or other proprietary game assets.

## 📥 Download / Tải bản Việt hóa

**[Download toàn bộ gói Việt hóa và trình cài (.zip)](https://github.com/ass3mble/modern-warfare-4-vietnamese-pack/archive/refs/heads/main.zip)**

GitHub: click **Code → Download ZIP**, then extract the ZIP fully. **Do not run the installer inside an unopened ZIP.**

## Cách cài cho Windows

1. **Tắt game hoàn toàn.** Bạn cần bản game phù hợp, được cài hợp pháp và đã có **bộ nạp Việt hóa tương thích** có khả năng đọc `sp26/trdata2.bin`. Gói công khai này không kèm hoặc cài đặt hook/DLL.
2. Cài **[Python 3](https://www.python.org/downloads/windows/)** nếu máy chưa có. Khi cài Python trên Windows, có thể chọn *Add Python to PATH*.
3. Giải nén toàn bộ `modern-warfare-4-vietnamese-pack-main.zip`.
4. Nhấp đúp **`INSTALL_VIET_HOA.bat`**.
5. Chọn thư mục **gốc của game** (thư mục chứa `sp26`), ví dụ `F:\Call of Duty - MW 4 (2026)`. Không chọn riêng thư mục `sp26`.
6. Nếu thông báo **SUCCESS**, bản Việt hóa đã được ghi vào `sp26\trdata2.bin`; tệp cũ được sao lưu với hậu tố `.BACKUP-...`. Mở game theo cách thông thường để kiểm tra.

Có thể kéo-thả thư mục game vào `INSTALL_VIET_HOA.bat` thay vì chọn từ hộp thoại. Trường hợp `ALREADY INSTALLED` nghĩa là dữ liệu đang dùng đã trùng SHA-256 với bản phát hành này.

### Cần biết trước khi cài

- Trình cài xác minh cấu trúc **40.085 khóa tiếng Anh** và dấu vân tay nguồn SHA-256 **trước khi ghi**. Nếu dữ liệu game khác phiên bản tương thích, nó **từ chối cài** để tránh hỏng game.
- Tệp đích được dựng lại từ dữ liệu nguồn **trên chính máy người dùng**, nên không cần tải nội dung gốc của game từ GitHub.
- Luôn sao lưu bản cũ với SHA-256 được xác thực. Không chạm vào EXE, DLL, FF, anti-cheat, bộ font hoặc các tệp ngoài `sp26/trdata2.bin`.
- Gói chỉ cung cấp **dữ liệu Việt hóa**; người cài vẫn cần bộ nạp hỗ trợ định dạng này. Không có bảo đảm bản game nguyên gốc chưa có loader sẽ tự hiển thị tiếng Việt.
- Đây là bản **đã kiểm tra tĩnh trên bộ dữ liệu**, chưa được xác nhận kiểm thử toàn bộ 16 nhiệm vụ campaign và mọi màn hình thực tế.

### Khôi phục / Restore

Nếu cần quay lại bản cũ, hãy **thoát game** và vào thư mục `sp26`. Tìm tệp `trdata2.bin.BACKUP-...` do trình cài tạo. Giữ một bản sao an toàn của tệp này, đổi tên nó về `trdata2.bin` để thay tệp vừa cài. Không xóa bản backup cho đến khi game hoạt động bình thường.

## Release contents

| Item | Contents |
| --- | --- |
| `pack/manifest.json` | Version, source fingerprint, segment list and exact integrity SHA-256 |
| `pack/v6157.part00.b64` through `v6157.part08.b64` | All 40,085 Vietnamese target strings in nine compressed text segments; no English game text |
| `INSTALL_VIET_HOA.bat` | Windows double-click launcher |
| `INSTALL_VIET_HOA.py` | Offline installer: validate → build candidate → backup → atomic replacement → verify |
| `tools/trdata.py` | Advanced low-level parser and reviewed correction validator |
| `tests/test_trdata.py` | Synthetic-only parser tests, independent of commercial game files |

**Release V6.157:** expected installed `sp26/trdata2.bin` SHA-256:

```text
f7279a141946e6f26140386ca2e5bcf46d5f6802585de199938f7790db321ce5
```

Expected English source fingerprint:

```text
4e67f94799574f55f3398c3223811072741f9b19d75993d7471243ba4333049f
```

Verify a matching local game without modifying anything:

```bash
python INSTALL_VIET_HOA.py --game-dir "F:\Call of Duty - MW 4 (2026)" --verify-only
```

Installer integration was tested offline with a private synthetic/English-only translation target derived from the matching local key corpus; it generated a **byte-for-byte identical** `trdata2.bin` and verified a SHA-matched backup. That does **not** establish runtime font/gameplay compatibility.

## Developers / Dành cho người đóng góp

Run synthetic parser tests:

```bash
python -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [LICENSE](LICENSE). MIT covers repository original installer/toolkit source, not third-party game assets. Do not commit private game files, proprietary fonts, loader DLLs or copyrighted English dictionaries.
