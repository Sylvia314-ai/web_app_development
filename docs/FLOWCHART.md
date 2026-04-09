# 系統流程圖設計文件 (FLOWCHART.md)

本文件依據 [PRD.md](PRD.md) 的需求與 [ARCHITECTURE.md](ARCHITECTURE.md) 的架構設計，將「線上算命系統」的互動與資料流視覺化。提供開發人員在著手開發前，確認使用者的操作行為邊界與系統響應模式。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者從進入網站開始的操作路徑，包含主功能的使用與權限判斷。

```mermaid
flowchart LR
    A([進入網站首頁]) --> B{是否有登入?}
    
    B -->|否| C[瀏覽每日運勢 / 基本介紹]
    C --> B1[切換至登入/註冊頁面]
    B1 -->|註冊/登入成功| D[返回與個人化首頁]
    
    B -->|是| D
    
    D --> E{選擇功能模組}
    
    E -->|算命與抽籤| F[進入抽籤/占卜頁面]
    F --> F1[點擊求籤/抽牌]
    F1 --> F2[系統顯示算命結果]
    F2 --> F3[自動儲存至歷史紀錄]
    F2 --> F4[點擊分享至社群平台]
    
    E -->|歷史紀錄| G[進入會員儀表板]
    G --> G1[瀏覽過往算命與抽籤結果]
    
    E -->|捐香油錢| H[進入捐獻頁面]
    H --> H1[選擇捐款金額並結帳]
    H1 --> H2[系統顯示感謝祈福畫面]
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖具體描述使用者進行「線上抽籤並儲存紀錄」操作時，系統各元件間的資料傳遞。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Flask as Flask Controller (routes/divination.py)
    participant Model as SQLAlchemy Model (divination.py)
    participant DB as SQLite 資料庫

    User->>Browser: 在抽籤頁面點擊「立刻求籤」
    Browser->>Flask: POST /divination/draw <br/> (帶表單資料及 CSRF Token)
    Flask->>Flask: 檢查使用者登入狀態與驗證 Token
    Flask->>Model: 呼叫產生籤詩商業邏輯 (隨機抽取)
    Model->>DB: INSERT INTO divination_records <br/> (儲存使用者 ID 與籤詩 ID/結果)
    DB-->>Model: 成功寫入
    Model-->>Flask: 回傳算命紀錄物件 (包含解籤內容與流水號 ID)
    Flask-->>Browser: HTTP 302 重導向至 /divination/result/{id}
    Browser->>Flask: GET /divination/result/{id}
    Flask->>Browser: 透過 Jinja2 渲染 result.html 並回傳
    Browser-->>User: 顯示詳細的算命結果與解籤內容
```

## 3. 功能清單與路由對照表

本表列出系統所有的核心功能與其對應的 URL 路徑 (Endpoint) 及 HTTP 方法，供後續實作路由時參考：

| 功能模組 | 操作描述 | HTTP 方法 | URL 路徑 |
| --- | --- | --- | --- |
| **首頁與運勢** | 瀏覽首頁與每日運勢 | `GET` | `/` |
| **帳號管理** | 顯示註冊頁面 / 送出註冊資料 | `GET` / `POST` | `/auth/register` |
| **帳號管理** | 顯示登入頁面 / 送出登入資訊 | `GET` / `POST` | `/auth/login` |
| **帳號管理** | 使用者登出 (清除 Session) | `GET` | `/auth/logout` |
| **算命與抽籤** | 顯示可選擇的算命/抽籤項目清單 | `GET` | `/divination` |
| **算命與抽籤** | 執行抽籤/占卜並儲存結果 (寫入 DB) | `POST` | `/divination/draw` |
| **算命與抽籤** | 查看單一算命/抽籤的詳細結果與分享 | `GET` | `/divination/result/<id>` |
| **歷史紀錄** | 瀏覽該使用者的所有過往算命紀錄 | `GET` | `/divination/history` |
| **線上捐獻** | 顯示捐款表單與選擇方案 | `GET` | `/donation` |
| **線上捐獻** | 送出捐款請求/模擬建立訂單 | `POST` | `/donation/donate` |
| **線上捐獻** | 捐款成功感謝與祈福畫面 | `GET` | `/donation/success` |
