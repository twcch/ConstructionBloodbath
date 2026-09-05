# Construction Bloodbath (工地血戰)

> **國立成功大學 Python程式語言與互動式遊戲設計 (114) 期末專題**  
> 以 Python & Pygame 開發的 2D 橫向捲軸射擊遊戲《工地血戰》

本專案為一款基於 Python 3.11 與 Pygame 打造的高完成度 2D 橫向捲軸射擊遊戲。專案以經典街機風格（如《魂斗羅》）為靈感，具備流暢的操作手感、模組化架構、資料驅動的關卡設計，以及高擴充性的資源處理管線。

---

## 遊戲特色 (Features)

- **流暢的操作迴圈**：移動、跳躍、射擊等即時反應與打擊感。
- **資料驅動關卡**：採用 Tiled TMX/TSX 地圖編輯器設計關卡地圖 ([assets/data/map.tmx](assets/data/map.tmx))。
- **清晰的分層架構**：應用層 (Application) / 領域層 (Domain) / 設定層 (Config) / 資源層 (Assets)。
- **集中式參數調校**：所有物理、數值設定皆集中於 [configs/settings.py](configs/settings.py)。
- **資源動態加載與校驗**：精靈圖 (Sprites) 與音效資源於啟動時驗證與載入。
- **封裝完善的場景與關卡管理**：([core/scene_manager.py](core/scene_manager.py), [core/level_manager.py](core/level_manager.py))。
- **高度擴充性設計模式**：實體 (Entity) / 工廠 (Factory) / 服務 (Service) 架構 ([model/entity/](model/entity), [model/factory/](model/factory), [model/service/](model/service))。
- **HUD 與使用者介面**：([ui/hud.py](ui/hud.py))。
- **開源授權**：採用 MIT License，允許自由使用與衍生開發 ([LICENSE](LICENSE))。

---

## 設計理念 (Design Philosophy)

- **資料優先 (Data-First)**：遊戲參數與調校數值皆存放在設定檔或資料檔中，避免硬編碼 (Hard-coding)。
- **熱插拔內容 (Hot-Swappable)**：新增精靈圖、關卡或敵人種類時，無需改動主遊戲迴圈。
- **渲染與邏輯分離**：降低邏輯與畫面繪製的耦合度，方便未來的效能分析或切換渲染層。
- **清晰的生命週期**：啟動初始化、資源載入、場景堆疊/切換、關卡重置。

---

## 專案目錄結構 (Project Structure)

```text
ConstructionBloodbath/
├─ app.py                       # 程式進入點：初始化、主迴圈、場景派發
├─ configs/
│  └─ settings.py               # 全域設定與遊戲數值參數
├─ core/
│  ├─ game_app.py               # 核心應用程式封裝
│  ├─ scene_manager.py          # 場景堆疊與切換管理
│  └─ level_manager.py          # 關卡載入與重置
├─ model/
│  ├─ entity/                   # 遊戲實體（玩家、敵人、物件等）
│  ├─ factory/                  # 實體工廠 / 組裝器
│  └─ service/                  # 邏輯服務（碰撞偵測、物理系統、戰鬥計算等）
├─ ui/
│  └─ hud.py                    # 抬頭顯示器 (HUD) 與 UI 介面
├─ assets/
│  ├─ data/                     # Tiled 地圖資料 (map.tmx / *.tsx)
│  ├─ graphics/                 # 角色與物件精靈圖、動畫影格
│  ├─ audio/                    # 背景音樂與音效
│  └─ font/                     # 遊戲字型資源
└─ build/                       # 打包構建輸出目錄
```

---

## 核心模組 (Key Modules)

- **程式進入點**：[app.py](app.py)
- **參數設定**：[configs/settings.py](configs/settings.py)
- **遊戲主迴圈**：[core/game_app.py](core/game_app.py)
- **場景管理**：[core/scene_manager.py](core/scene_manager.py)
- **關卡管理**：[core/level_manager.py](core/level_manager.py)
- **HUD 介面**：[ui/hud.py](ui/hud.py)

---

## 環境建置與安裝 (Setup & Installation)

### 必要條件
- Python 3.11 或以上版本
- pip / venv 虛擬環境工具

### 安裝步驟

```sh
# 1. 建立虛擬環境
python -m venv .venv

# 2. 啟動虛擬環境
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. 安裝相依套件
pip install -r requirements.txt
```

---

## 執行與除錯 (Run & Debug)

### 直接執行
```sh
python app.py
```

### VS Code 執行與除錯
1. 以 VS Code 開啟專案資料夾。
2. 於除錯模式下執行 [app.py](app.py)。
3. 使用「終端機 (Terminal)」與「輸出 (Output)」面板檢視執行紀錄。

---

## 參數設定 (Configuration)

所有設定均集中於 [configs/settings.py](configs/settings.py)：

- **視窗相關**：解析度、視窗標題、目標 FPS。
- **輸入控制**：按鍵映射 (Input mapping)。
- **物理設定**：重力大小、移動速度、跳躍力度。
- **戰鬥數值**：攻擊傷害、冷卻時間、射擊頻率。
- **除錯開關**：各項除錯模式旗標。

**調校流程**：
修改參數後重新執行，即可立即驗證手感與遊戲平衡性。

---

## 遊戲迴圈概覽 (Game Loop)

1. **收集事件**：接收鍵盤、滑鼠或控制器輸入。
2. **更新狀態**：計算物理運動、AI 行為、射擊彈道與各項計時器。
3. **碰撞處理**：進行實體間碰撞偵測與判定結算。
4. **狀態判定**：評估場景轉移或關卡重置條件。
5. **畫面渲染**：依序繪製背景圖層、實體物件與 HUD 介面。

---

## 素材與資源管理 (Assets & Data)

- **地圖檔案**：[assets/data/map.tmx](assets/data/map.tmx) 及其對應圖塊集（如 [assets/data/Platforms.tsx](assets/data/Platforms.tsx)、[assets/data/Subway_tiles_x4.tsx](assets/data/Subway_tiles_x4.tsx)、[assets/data/wall_subway.tsx](assets/data/wall_subway.tsx)）。
- **圖像資源**：[assets/graphics/](assets/graphics/)
- **音效資源**：[assets/audio/](assets/audio/)
- **字型資源**：[assets/font/](assets/font/)

**命名規範**：
- 動畫影格序列：`方向/狀態/影格編號`（例如 `player/right/0.png`）。
- 靜態圖塊、可互動地圖元件與敵人圖片均有獨立資料夾分類存放。

---

## 擴充指南 (Extension Guidelines)

| 擴充項目 | 建議實作步驟 |
| :--- | :--- |
| **新增敵人** | 於 `model/entity/` 建立類別 → 工廠組裝實例 → 設定行為服務 (Behavior Service) |
| **新增武器** | 定義數值與外觀 → 實作射擊/彈道服務 → 綁定輸入按鍵 |
| **新增關卡** | 於 Tiled 繪製 TMX 地圖 → 放入 `assets/data/` → 透過 Level Manager 載入 |
| **新增 UI** | 實作 UI 類別 → 注入渲染管線 → 讀取設定檔參數 |

---

## 打包與發布 (Build / Distribution)

若使用 PyInstaller 等工具打包成獨立執行檔，請遵循以下原則：
- 資源路徑請使用相對路徑，避免寫死絕對路徑。
- 排除未使用的肥大相依套件以縮減執行檔體積。
- 於不同平台上測試中文字型與編碼支援情況。

---

## 測試與驗證 (Validation)

**基礎冒煙測試 (Smoke Tests)**：
- 專案能正常啟動無例外錯誤。
- 精靈圖與音訊資源皆能正確加載。
- 角色能正常進行移動、跳躍與射擊。
- 場景切換流暢無卡頓。

---

## 未來發展規劃 (Roadmap)

- [ ] 更完善的事件匯流排系統 (Event Bus)
- [ ] 可插拔的 AI 行為樹 (Behavior Tree)
- [ ] 存檔 / 讀檔系統 (Save / Load)
- [ ] 粒子特效系統與畫面後製效果
- [ ] 多人連線合作支援

---

## 授權條款 (License)

本專案採用 **MIT License** 授權開源，詳情請參閱 [LICENSE](LICENSE) 檔案。

---

## 聯絡方式 (Contact)

如有任何疑問或建議，歡迎透過以下方式聯絡：

- **Email**: twcch1218 [at] gmail.com

感謝您對《ConstructionBloodbath (工地血戰)》的關注！
