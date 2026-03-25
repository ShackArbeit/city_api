# Europe Travel API — FastAPI + MongoDB Atlas + Swagger

這是一個 **一天內可完成、適合面試展示的 FastAPI RESTful API 專案規格**。  
主題以 **歐洲城市與旅遊景點** 為背景，目標是同時展示：

- FastAPI 建立 RESTful API 的能力
- MongoDB Atlas 雲端資料庫串接
- Swagger / OpenAPI 文件
- 免費部署
- GitHub + CI/CD 基本流程

---

## 1. 專案定位

這個專案不是要做成正式商業產品，而是要做成：

**一個可以在面試中 5～10 分鐘內講清楚技術亮點的後端作品。**

所以請遵守以下原則：

1. **一天內完成優先**
2. **只做最能展示 RESTful 概念的 API**
3. **先完成 CRUD、文件、部署，再考慮加值功能**
4. **資料主題要直觀，讓面試官一看就懂**

---

## 2. 一天內完成版功能範圍

### 必做功能

- FastAPI 專案初始化
- MongoDB Atlas 連線
- `cities` collection CRUD
- `attractions` collection CRUD
- Query string 篩選功能
- Swagger 自動文件 (`/docs`)
- 免費平台部署
- README 說明

### 不建議一天內加入的功能

以下先不要做，避免超時：

- JWT 登入驗證
- RBAC 權限管理
- Docker Compose 多服務編排
- 圖片上傳
- 太複雜的 aggregation pipeline
- 排程任務
- Redis
- 單元測試全覆蓋

---

## 3. 專案主題

### 主題名稱

**Europe Travel API**

### 情境說明

這是一個提供歐洲旅遊城市與景點資訊的 RESTful API，讓使用者可以：

- 查看城市資訊
- 查看特定城市的景點
- 新增景點
- 修改景點資訊
- 刪除景點
- 依城市、分類、是否免費等條件篩選資料

這個主題的好處是：

- 資料直觀
- CRUD 很好展示
- 很適合 MongoDB 文件型資料結構
- 面試時容易講清楚 resource design

---

## 4. 建議技術棧

- **Backend**: FastAPI
- **Database**: MongoDB Atlas
- **ODM/Driver**: PyMongo（一天版較簡單）
- **Validation**: Pydantic
- **Docs**: FastAPI OpenAPI / Swagger UI
- **Deploy**: Render
- **CI/CD**: GitHub + Render Auto Deploy 或 GitHub Actions

---

## 5. 建議資料夾結構

```bash
project-root/
├─ app/
│  ├─ main.py
│  ├─ core/
│  │  └─ config.py
│  ├─ db/
│  │  └─ mongodb.py
│  ├─ models/
│  │  ├─ city_model.py
│  │  └─ attraction_model.py
│  ├─ schemas/
│  │  ├─ city_schema.py
│  │  └─ attraction_schema.py
│  ├─ routers/
│  │  ├─ cities.py
│  │  └─ attractions.py
│  └─ utils/
│     └─ helpers.py
├─ mock_data/
│  ├─ cities.json
│  └─ attractions.json
├─ requirements.txt
├─ .env.example
├─ .gitignore
└─ README.md
```

---

## 6. MongoDB Collections 設計

本專案只做兩個 collection：

---

### 6.1 `cities`

城市資料。

#### 欄位設計

| 欄位 | 型別 | 說明 |
|---|---|---|
| `_id` | ObjectId | MongoDB 主鍵 |
| `name` | string | 城市名稱 |
| `country` | string | 國家 |
| `region` | string | 區域，例如 Western Europe |
| `language` | array[string] | 常用語言 |
| `currency` | string | 幣別 |
| `best_season` | string | 最佳旅遊季節 |
| `description` | string | 城市簡介 |
| `created_at` | datetime | 建立時間 |
| `updated_at` | datetime | 更新時間 |

---

### 6.2 `attractions`

景點資料。

#### 欄位設計

| 欄位 | 型別 | 說明 |
|---|---|---|
| `_id` | ObjectId | MongoDB 主鍵 |
| `city_name` | string | 所屬城市名稱（一天版先不用 join） |
| `name` | string | 景點名稱 |
| `category` | string | 類型，例如 landmark / museum / palace / park |
| `address` | string | 地址 |
| `rating` | float | 評分 |
| `ticket_price_eur` | float | 門票價格（歐元） |
| `is_free` | boolean | 是否免費 |
| `recommended_visit_hours` | number | 建議停留時數 |
| `tags` | array[string] | 標籤 |
| `description` | string | 景點簡介 |
| `created_at` | datetime | 建立時間 |
| `updated_at` | datetime | 更新時間 |

> 為了控制一天內完成，這裡先用 `city_name` 而不是 `city_id`，讓你先完成功能與展示。第二版再改成真正關聯。

---

## 7. RESTful API 設計

---

### 7.1 Cities API

| Method | Path | 用途 |
|---|---|---|
| GET | `/api/v1/cities` | 取得城市列表 |
| GET | `/api/v1/cities/{city_id}` | 取得單一城市 |
| POST | `/api/v1/cities` | 新增城市 |
| PATCH | `/api/v1/cities/{city_id}` | 部分更新城市 |
| DELETE | `/api/v1/cities/{city_id}` | 刪除城市 |

---

### 7.2 Attractions API

| Method | Path | 用途 |
|---|---|---|
| GET | `/api/v1/attractions` | 取得景點列表 |
| GET | `/api/v1/attractions/{attraction_id}` | 取得單一景點 |
| POST | `/api/v1/attractions` | 新增景點 |
| PATCH | `/api/v1/attractions/{attraction_id}` | 部分更新景點 |
| DELETE | `/api/v1/attractions/{attraction_id}` | 刪除景點 |

---

### 7.3 Query Parameters（加分展示）

`GET /api/v1/attractions` 支援：

- `city_name=Paris`
- `category=museum`
- `is_free=true`
- `min_rating=4.5`

範例：

```http
GET /api/v1/attractions?city_name=Paris&is_free=false&min_rating=4.5
```

這一段在面試時很好講，因為可以展示：

- RESTful resource 設計
- query parameter filtering
- API 的可讀性與擴展性

---

## 8. Swagger / OpenAPI 文件

FastAPI 會自動提供：

- Swagger UI: `/docs`
- ReDoc: `/redoc`

建議你在 `main.py` 中設定：

- 專案標題
- 版本號
- description
- tags

例如：

- title: `Europe Travel API`
- version: `1.0.0`
- description: `A demo RESTful API for European travel cities and attractions.`

---

## 9. 部署建議

### 首選：Render

原因：

- 可直接部署 FastAPI
- 可連接 GitHub
- push 後可自動重新部署
- 適合 side project / 面試展示

### Render 部署重點

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- Python version 請和本機一致
- 環境變數放到 Render 的 Environment Variables

---

## 10. CI/CD 最小可行方案

### 最簡單版本

直接使用 Render 連 GitHub：

- push 到 `main`
- Render 自動 deploy

### 想再多展示一點

可以補一個 GitHub Actions：

- 安裝依賴
- 執行基本檢查
- 若通過就由 Render 自動吃新版本

一天版的重點是：

**CI/CD 有概念、有流程、有畫面即可，不要過度工程化。**

---

## 11. 建議開發順序（一天版）

### 第 1 階段：先完成能跑

1. 初始化 FastAPI 專案
2. 安裝 requirements
3. 建立 `main.py`
4. 測試 `/docs`

### 第 2 階段：接資料庫

5. 建立 MongoDB Atlas cluster
6. 建立資料庫與 collections
7. 在 `.env` 放 `MONGODB_URL`
8. 完成 FastAPI 連線

### 第 3 階段：做 API

9. 完成 `cities` CRUD
10. 完成 `attractions` CRUD
11. 加入 query filters
12. 加入錯誤處理

### 第 4 階段：部署

13. push 到 GitHub
14. 部署到 Render
15. 驗證 `/docs`
16. 補 README

---

## 12. 給 Codex 的分段 Prompt

以下 prompt 可以分段貼給 Codex，不要一次丟太大包，成功率會比較高。

---

### Prompt 1：初始化專案骨架

```text
請幫我建立一個 FastAPI 專案骨架，專案名稱為 Europe Travel API。

需求：
1. 使用 FastAPI
2. 專案資料夾結構如下：app/core, app/db, app/models, app/schemas, app/routers, app/utils
3. 建立 app/main.py
4. 設定 API title = Europe Travel API
5. version = 1.0.0
6. description = A demo RESTful API for European travel cities and attractions.
7. 加入 /health route 回傳 {"status": "ok"}
8. 請一併產生 requirements.txt

請先只完成骨架，不要先寫 CRUD。
```

---

### Prompt 2：MongoDB Atlas 連線

```text
請幫我在 FastAPI 專案中加入 MongoDB Atlas 連線功能。

需求：
1. 使用 PyMongo
2. 建立 app/core/config.py 讀取 .env 中的 MONGODB_URL 與 DB_NAME
3. 建立 app/db/mongodb.py 管理 MongoClient
4. 提供可重複使用的資料庫連線方法
5. 程式需保持簡潔，適合一天內完成的專案
6. 不要做過度抽象
7. 同時提供 .env.example

請輸出完整程式碼。
```

---

### Prompt 3：建立 Pydantic Schemas

```text
請幫我為 Europe Travel API 建立 Pydantic schemas。

需求：
1. 建立 city_schema.py 與 attraction_schema.py
2. cities 欄位：name, country, region, language, currency, best_season, description
3. attractions 欄位：city_name, name, category, address, rating, ticket_price_eur, is_free, recommended_visit_hours, tags, description
4. 請區分 Create schema、Update schema、Response schema
5. PATCH 更新請使用 optional fields
6. 回傳格式需適合 MongoDB ObjectId 轉字串

請輸出完整程式碼。
```

---

### Prompt 4：實作 Cities CRUD Router

```text
請幫我在 FastAPI 專案中實作 cities router。

需求：
1. 檔案位置：app/routers/cities.py
2. API 前綴：/api/v1/cities
3. 實作以下 API：
   - GET /api/v1/cities
   - GET /api/v1/cities/{city_id}
   - POST /api/v1/cities
   - PATCH /api/v1/cities/{city_id}
   - DELETE /api/v1/cities/{city_id}
4. 使用 MongoDB Atlas
5. 回傳內容請做 ObjectId 轉字串
6. 找不到資料時回傳 404
7. 成功新增回傳 201
8. 程式碼請保持面試展示友善、結構清楚

請輸出完整程式碼。
```

---

### Prompt 5：實作 Attractions CRUD + Filter

```text
請幫我在 FastAPI 專案中實作 attractions router。

需求：
1. 檔案位置：app/routers/attractions.py
2. API 前綴：/api/v1/attractions
3. 實作以下 API：
   - GET /api/v1/attractions
   - GET /api/v1/attractions/{attraction_id}
   - POST /api/v1/attractions
   - PATCH /api/v1/attractions/{attraction_id}
   - DELETE /api/v1/attractions/{attraction_id}
4. GET list 要支援以下 query params：
   - city_name
   - category
   - is_free
   - min_rating
5. 使用 MongoDB Atlas
6. 回傳內容請做 ObjectId 轉字串
7. 錯誤處理清楚
8. 程式碼要簡潔、適合一天內完成

請輸出完整程式碼。
```

---

### Prompt 6：註冊 Routers 與 Swagger 整理

```text
請幫我修改 app/main.py，將 cities 與 attractions routers 註冊到 FastAPI。

需求：
1. include_router(cities.router)
2. include_router(attractions.router)
3. 加上 tags 與 description，讓 Swagger /docs 更清楚
4. 保留 /health route
5. 若有需要可補充簡單的 root route

請輸出完整程式碼。
```

---

### Prompt 7：部署到 Render

```text
請幫我整理這個 FastAPI 專案部署到 Render 所需的內容。

需求：
1. 說明 requirements.txt 是否需要補充
2. 說明 Render 的 Build Command 與 Start Command
3. 說明環境變數設定
4. 若需要，請產生 render.yaml
5. 內容要以最小可行部署為主
6. 不要使用 Docker

請用 README 教學格式回答。
```

---

### Prompt 8：GitHub Actions（可選）

```text
請幫我為這個 FastAPI 專案建立最簡單的 GitHub Actions workflow。

需求：
1. 當 push 到 main 時觸發
2. 安裝 Python dependencies
3. 執行基本語法檢查或簡單啟動檢查
4. 適合面試展示，不要做得太複雜
5. 請輸出 .github/workflows/ci.yml 完整內容
```

---

## 13. 你在 VSCode / Codex 的使用策略

建議你不要一次叫 Codex 寫完整專案，原因是：

- 容易一次產出過大
- 錯誤比較難修
- 跟你的一天完成目標衝突

### 正確方式

每次只叫它完成一個小段：

1. 先骨架
2. 再 DB
3. 再 schema
4. 再 cities router
5. 再 attractions router
6. 最後修 main.py 與部署

這樣你比較能掌控品質，也比較能真的看懂。

---

## 14. 面試時可怎麼介紹這個專案

你可以這樣講：

> 我用 FastAPI 做了一個以歐洲城市與景點為主題的 RESTful API，資料庫使用 MongoDB Atlas，主要是想展示 CRUD、query filtering、Pydantic schema 驗證，以及 FastAPI 自動產出的 Swagger 文件。部署部分我放到 Render，並透過 GitHub 做基本的 CI/CD 流程。這個專案刻意控制在一天內完成，重點是展示 API 設計與工程化基本能力，而不是堆很多功能。

這段很適合面試，因為它聽起來是有策略地取捨，而不是亂做一通。

---

## 15. 後續第二版可以再加什麼

當你第一版完成後，可以再加：

- `city_id` 真正關聯化
- itinerary collection
- pagination
- sorting
- JWT 驗證
- Docker
- pytest
- rate limiting
- API versioning 更完整設計

但請記住：

**第一版先活著、能 demo、能部署，比什麼都重要。**

---

## 16. 本專案 mock_data 說明

本專案已提供 `mock_data/` 範例資料，可手動匯入 MongoDB Atlas 或使用 Atlas UI 逐筆新增。

檔案：

- `mock_data/cities.json`
- `mock_data/attractions.json`

你也可以把這些資料當作 POST API 的測試 payload。

---

## 17. 建議 requirements.txt

```txt
fastapi
uvicorn
pymongo
python-dotenv
pydantic
```

若你的 FastAPI / Pydantic 版本相容性有差異，可以由 Codex 補成固定版本。

---

## 18. 最後提醒

如果你的目標是：

- **一天內完成**
- **可展示 RESTful API 能力**
- **可部署**
- **文件漂亮**

那這份規格是合理而且可落地的。  
請不要一開始就加太多進階功能，不然你會把時間花在 debug，而不是完成作品。
