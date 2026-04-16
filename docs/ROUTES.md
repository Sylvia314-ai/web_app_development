# 路由設計文件 (ROUTES.md)

本文件根據 PRD、系統架構與資料庫設計，規劃「線上算命系統」的 Flask 路由，並提供前後端分工作業的參考。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 | GET | `/` | `templates/index.html` | 顯示首頁內容或每日運勢 |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示會員註冊表單 |
| 註冊處理 | POST | `/auth/register` | — | 接收註冊資料，存入 DB 後重導向 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示會員登入表單 |
| 登入處理 | POST | `/auth/login` | — | 驗證密碼並建立登入狀態，重導向 |
| 登出 | GET | `/auth/logout` | — | 清除登入狀態，重導向 |
| 算命主頁 | GET | `/divination/` | `templates/divination/index.html` | 顯示可選的抽籤與算命項目 |
| 執行抽籤 | POST | `/divination/draw` | — | 亂數產生籤詩，存入 DB，重導向 |
| 抽籤結果 | GET | `/divination/result/<int:id>` | `templates/divination/result.html`| 顯示單一算命紀錄結果與解籤內容 |
| 歷史紀錄 | GET | `/divination/history` | `templates/divination/history.html` | 顯示使用者的算命歷史紀錄列表 |
| 捐獻頁面 | GET | `/donation/` | `templates/donation/donate.html` | 顯示油香捐款金額選擇頁面 |
| 建立訂單 | POST | `/donation/donate` | — | 記錄捐款至 DB，重導向至成功頁 |
| 捐獻成功 | GET | `/donation/success` | `templates/donation/success.html` | 顯示感謝祈福畫面 |

## 2. 每個路由的詳細說明

### 2.1 主基礎路由 (`routes/main.py`)
- **GET `/`**：
  - 輸入：無
  - 邏輯：從 session 檢查登入狀態。可配合外部 API 解析當日運勢（Placeholder）。
  - 輸出：渲染 `index.html`。
  - 錯誤：無。

### 2.2 帳號認證路由 (`routes/auth.py`)
- **GET, POST `/auth/register`**：
  - 輸入：POST 帶有 `username`, `email`, `password`，GET 無。
  - 邏輯：若為 POST，檢查是否有重複註冊，將密碼 Hash 後呼叫 `User.create` 寫入。
  - 輸出：註冊成功重導向至 `/auth/login`。
- **GET, POST `/auth/login`**：
  - 輸入：POST 帶有 `username` 或 `email`，及密碼。
  - 邏輯：比對帳號與密碼 Hash，通過後將 user_id 寫入 session。
  - 輸出：登入成功重導至 `/`。若失敗則顯示錯誤 Flash message。
- **GET `/auth/logout`**：
  - 邏輯：`session.clear()`。
  - 輸出：重導至 `/`。

### 2.3 抽籤算命路由 (`routes/divination.py`)
- **GET `/divination/`**：
  - 邏輯：驗證是否登入（可選），列出可供抽籤的項目（如：六十甲子籤）。
  - 輸出：渲染 `divination/index.html`。
- **POST `/divination/draw`**：
  - 輸入：表單欄位 `divination_type`。
  - 邏輯：需登入。隨機取出一支籤（利用陣列或額外字典），呼叫 `DivinationRecord.create()` 儲存，取得 ID。
  - 輸出：重導至 `/divination/result/<id>`。
- **GET `/divination/result/<id>`**：
  - 輸入：URL 參數 `id`。
  - 邏輯：需登入。呼叫 `DivinationRecord.get_by_id(id)`，驗證此記錄是否屬於當前使用者。
  - 輸出：渲染 `divination/result.html`。
  - 錯誤：404 找不到檔案，或 403 權限不足。
- **GET `/divination/history`**：
  - 邏輯：需登入。呼叫 `DivinationRecord.get_by_user_id(session['user_id'])` 取得列表。
  - 輸出：渲染 `divination/history.html`。

### 2.4 捐獻路由 (`routes/donation.py`)
- **GET `/donation/`**：
  - 邏輯：顯示捐獻選項頁面。
  - 輸出：渲染 `donation/donate.html`。
- **POST `/donation/donate`**：
  - 輸入：表單裡的 `amount`。
  - 邏輯：需登入。呼叫 `Donation.create()` 建立金流紀錄，狀態先壓 `pending`（模擬後隨即轉為 `completed` 或第三方回呼）。
  - 輸出：重導向至 `/donation/success`。
- **GET `/donation/success`**：
  - 邏輯：宣告捐獻成功。
  - 輸出：渲染 `donation/success.html`。

## 3. Jinja2 模板清單

所有模板皆繼承自 `templates/base.html`，以保持風格一致。

### 核心基礎
- `templates/base.html`：包含 HTML5 骨架、CSS/JS 引入、Navbar、Flash Message 區塊與 Footer，為所有頁面共用。
- `templates/index.html`：首頁。

### 認證 (Auth)
- `templates/auth/login.html`：登入表單頁面。
- `templates/auth/register.html`：註冊表單頁面。

### 算命與抽籤 (Divination)
- `templates/divination/index.html`：算命項目列表/點擊抽籤頁面。
- `templates/divination/result.html`：單次抽籤的結果詳情與解籤頁面。
- `templates/divination/history.html`：過往算命紀錄列表頁面。

### 捐款 (Donation)
- `templates/donation/donate.html`：選擇捐獻金額、輸入祈福語的表單。
- `templates/donation/success.html`：感謝頁面。
