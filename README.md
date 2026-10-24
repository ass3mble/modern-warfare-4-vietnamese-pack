# Modern Warfare 4 — Vietnamese Localization Toolkit

> Unofficial community localization project. Not affiliated with or endorsed by Activision, Infinity Ward, or the game's publishers.

**Repository:** public, source-only toolkit for auditing and preparing Vietnamese localization corrections for *Call of Duty: Modern Warfare 4 (2026)*.

## What is published?

- A read-only parser and validation tools for a UTF-8, length-prefixed translation dictionary.
- A guarded builder for **detached candidates** generated from human-reviewed EN/VI corrections.
- Offline synthetic tests, contribution guidelines, and release-integrity documentation.

**This is not a redistribution of the game or a ready-to-play translation download.** No original game executable, fastfile, DLL, font, complete localization dictionary, paid content, extracted third-party pack, authentication token, or unauthorized game asset belongs in this repository. Review every contribution for redistribution rights.

## Status

| Area | Status |
| --- | --- |
| Public source toolkit | In development |
| Local campaign dialogue review | Ongoing |
| Static validation of local candidates | Separate from this public repository |
| In-game rendering and all 16 campaign missions | **Not fully verified** |
| Redistributable Vietnamese translation package | **Not published** |

The scripts here are intended for users working with **their own legitimately obtained local files**. They never need to start the game.

## Quick start

Requires **Python 3.10+**; no third-party Python packages.

Inspect a locally owned dictionary:

```bash
python tools/trdata.py inspect "path/to/trdata2.bin" --expect-count 40085
```

Prepare a CSV with these exact columns:

```csv
id,EN_exact,installed_VI_exact,candidate_VI_exact
```

The CSV should contain only corrections you are authorized to share or use. Build a **new** output file, never the original:

```bash
python tools/trdata.py build "path/to/trdata2.bin" review.csv \
  --base-sha YOUR_VERIFIED_SHA256 \
  --out "separate-staging/candidate.bin" \
  --expect-count 40085
```

Verify the result independently:

```bash
python tools/trdata.py verify "path/to/trdata2.bin" \
  "separate-staging/candidate.bin" --review review.csv
```

Test without any game data:

```bash
python -m unittest discover -s tests -v
```

The example count reflects one locally examined dictionary format; it is **not** a guarantee of compatibility with every version.

## Safety guarantees

The builder rejects a mismatched base SHA-256, missing or duplicate review IDs, source drift, control-token/newline changes, the source path as the output, and existing output files. It writes **only** an independently named candidate; installation into a running game is intentionally out of scope. Validate and back up separately before using any generated file.

See [CONTRIBUTING.md](CONTRIBUTING.md) for copyright and review requirements and [SECURITY.md](SECURITY.md) for handling of suspicious files.

## Tiếng Việt

Repo công khai **công cụ và quy trình kiểm toán Việt hóa**, không chứa dữ liệu game gốc. Công cụ đọc tệp dịch cục bộ, kiểm tra cặp câu Anh–Việt, giữ nguyên placeholder/ngắt dòng và chỉ xuất ứng viên sang **đường dẫn mới**, không tự ghi đè bản LIVE.

**Chưa xác nhận đã kiểm thử hoàn chỉnh trong game hoặc cả 16 nhiệm vụ campaign.** Các sửa đổi mới phải được rà ngữ cảnh, kiểm thử riêng và phát hành theo quy trình có sao lưu.

## License

[MIT](LICENSE) applies **only to original source code and documentation authored for this repository**. It does not grant permission to redistribute any game, third-party translations, assets, trademarks, or fonts.
