# 路由與頁面設計文件 (ROUTES) - 讀書計畫管理系統

這份文件定義了本系統所有的 Flask 路由 (URL Path)、HTTP 方法以及與 Jinja2 模板之間的對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (任務列表) | GET | `/` | `index.html` | 顯示所有任務與行事曆檢視 |
| 新增任務 | POST | `/tasks/add` | — | 接收表單資料存入 DB，完成後重導向至首頁 |
| 切換完成狀態 | POST | `/tasks/<int:id>/toggle` | — | 接收前端狀態切換請求，更新 DB 後回傳成功狀態 |
| 刪除任務 | POST | `/tasks/<int:id>/delete` | — | 刪除單筆任務，完成後重導向至首頁 |
| 進度統計 | GET | `/stats` | `stats.html` | 顯示完成率等統計圖表 |

> **說明**：由於我們採用了「以單一視圖為主的工作區」架構（詳見 ARCHITECTURE.md），所以任務的新增表單直接放在首頁 (`index.html`) 中，不需要額外建立 `/tasks/new` 的頁面。

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **輸入**：無
- **處理邏輯**：呼叫 `Task.get_all()` 取得目前所有任務。
- **輸出**：將任務清單傳給 `index.html` 進行渲染。
- **錯誤處理**：若資料庫連線失敗，回傳 500 錯誤。

### `POST /tasks/add` (新增任務)
- **輸入**：表單欄位 `subject` (科目), `title` (內容), `due_date` (預定日期)
- **處理邏輯**：驗證欄位是否空白，若無誤則呼叫 `Task.create(subject, title, due_date)`。
- **輸出**：透過 `redirect('/')` 重導向回首頁。
- **錯誤處理**：如果資料驗證失敗（例如未填寫必填欄位），可用 `flash` 顯示錯誤訊息，並重新渲染首頁。

### `POST /tasks/<int:id>/toggle` (切換完成狀態)
- **輸入**：URL 參數 `id`
- **處理邏輯**：確認任務存在後，呼叫 `Task.toggle_status(id)`。
- **輸出**：此為配合 AJAX 呼叫的 API，回傳 JSON `{ "success": true }`；若是傳統表單則可重導向回首頁。
- **錯誤處理**：若找不到該 id 的任務，回傳 404 Not Found。

### `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `Task.delete(id)` 刪除該筆資料。
- **輸出**：透過 `redirect('/')` 重導向回首頁。
- **錯誤處理**：若任務不存在，可忽略或提示錯誤。

### `GET /stats` (進度統計)
- **輸入**：無
- **處理邏輯**：呼叫 `Task.get_all()`，並於後端計算完成率 (已完成任務數 / 總任務數)。
- **輸出**：將統計數據傳給 `stats.html` 進行渲染。

## 3. Jinja2 模板清單

所有模板皆存放在 `app/templates/` 目錄下：

1. `base.html`
   - **說明**：共用版面佈局（包含 HTML 的 `<head>`、全局導覽列、頁尾與共用的 CSS/JS 引入）。其他頁面都會繼承此檔案。
2. `index.html`
   - **說明**：首頁模板。繼承自 `base.html`。包含「新增任務表單」與「任務列表」兩個主要區塊。
3. `stats.html`
   - **說明**：統計頁面模板。繼承自 `base.html`。負責以圖表或進度條顯示學習進度。

## 4. 路由骨架程式碼

請參考以下檔案：
- `app/routes/__init__.py`
- `app/routes/task_routes.py`
