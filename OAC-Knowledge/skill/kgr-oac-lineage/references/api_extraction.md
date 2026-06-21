# API extraction — re-extract kho từ OAC

Cookbook đầy đủ (endpoint, auth, CSRF, bẫy, pipeline) ở:
**`C:\Project\KGR-OAC-Agents\OAC-Knowledge\external\oac_rest_api_notes.md`** — đọc file đó.

Tóm tắt pipeline rebuild:
1. MCP `chrome-dashboard` → login OAC (minhndn@bizin.vn). KHÔNG kill Chrome toàn cục; gỡ kẹt theo profile `profile-dashboard`.
2. Fetch 4 workbook (`projects/json`) + enumerate (`homepage`) + 40 dataflow def (`dataflows?dataFlowID=`) + 63 dataset (`dataset/datasets?datasetID=all`). Lưu raw vào `C:\Project\KGR-OAC-Agents\Dashboard-builder\_oac_extract\`.
3. `PYTHONUTF8=1 python C:\Project\KGR-OAC-Agents\Dashboard-builder\_oac_extract\build_catalogs.py` → sinh 5 YAML vào `C:\Project\KGR-OAC-Agents\OAC-Knowledge\`.
4. `PYTHONUTF8=1 python ..\scripts\validate_kb.py` → phải PASS (0 ERROR).
5. Copy raw mới sang `C:\Project\KGR-OAC-Agents\OAC-Knowledge\raw\`.

Builder + raw đều giữ trong `_oac_extract\` (provenance) — có thể re-distill không cần fetch lại.
