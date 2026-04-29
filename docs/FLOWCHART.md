# 流程圖與流程設計 (FLOWCHART) - 讀書計畫管理系統

這份文件視覺化了使用者操作路徑以及系統內的資料流，幫助開發團隊確認每個功能的前後步驟。

## 1. 使用者流程圖（User Flow）

以下流程圖展示了使用者進入「讀書計畫管理系統」後，如何進行各項操作（如新增任務、標記完成、查看進度等）。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 任務列表與行事曆]
    Home --> Action{要執行什麼操作？}
    
    Action -->|新增| Form[填寫新增任務表單]
    Form -->|送出| ProcessAdd[系統處理新增]
    ProcessAdd --> Home
    
    Action -->|標記狀態| Toggle[點擊任務的完成 Checkbox]
    Toggle --> ProcessToggle[系統非同步更新狀態]
    ProcessToggle --> Home
    
    Action -->|查看統計| Stats[點擊進入進度統計頁]
    Stats --> Home
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖以「使用者新增一筆讀書任務」為例，展示從前端送出表單到後端資料庫存取的完整資料流。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask 路由
    participant DB as SQLite 資料庫

    User->>Browser: 在首頁填寫任務內容並送出表單
    Browser->>Flask: POST /tasks/add (表單資料)
    Flask->>Flask: 驗證資料格式
    Flask->>DB: INSERT INTO tasks (title, subject, due_date)
    DB-->>Flask: 寫入成功
    Flask-->>Browser: HTTP 302 重導向回首頁 (GET /)
    Browser->>Flask: 重新載入首頁
    Flask->>DB: SELECT * FROM tasks 取得最新任務列表
    DB-->>Flask: 回傳任務清單
    Flask-->>Browser: 回傳渲染後的首頁 HTML (包含新任務)
    Browser-->>User: 看到新增的任務
```

## 3. 功能清單對照表

根據 PRD 定義的核心功能，我們規劃了以下的路由結構：

| 功能名稱 | 網址路徑 (URL) | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **任務列表** | `/` | GET | 顯示首頁，包含所有任務與行事曆檢視 |
| **任務新增** | `/tasks/add` | POST | 接收表單資料並建立新的讀書任務 |
| **完成標記** | `/tasks/<id>/toggle` | POST | 切換特定任務的「已完成/未完成」狀態 |
| **進度統計** | `/stats` | GET | 顯示任務完成比例與整體學習進度統計圖表 |
