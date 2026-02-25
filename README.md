# 課程搶課機器人

自動化搶課工具，使用 Selenium 自動監控並搶選目標課程。

## 功能特色

- 🔄 自動重複掃描課程狀態
- ⚡ 發現可加選時立即點擊
- 🔔 處理課程額滿、衝堂等情況
- 🔁 課程額滿時自動等待並重試
- 📊 即時顯示執行狀態

## 使用前準備

### 1. 安裝依賴套件

```bash
pip install selenium webdriver-manager
```

### 2. 啟動 Chrome 瀏覽器（開啟遠端調試）

在終端執行以下命令：

**Windows:**
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
```

**Mac:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev"
```

### 3. 登入選課系統

在開啟的瀏覽器中手動登入學校選課系統，並進入加退選頁面。

## 使用方法

1. 修改 `main.py` 中的 `TARGET_COURSE_ID` 為你想搶的課程代碼：

```python
TARGET_COURSE_ID = "B5704M22"  # 修改為你的目標課程代碼
```

2. 執行程式：

```bash
python main.py
```

3. 程式會自動開始監控，發現可加選時會自動點擊。

## 運作流程

1. 連接到已開啟的 Chrome 瀏覽器
2. 持續掃描目標課程的「加選」按鈕
3. 發現按鈕可點擊時立即執行加選
4. 處理系統彈窗（確認加選、顯示結果）
5. 若課程額滿，等待 10 秒後重新整理並繼續嘗試
6. 成功或出現異常時停止並通知

## 注意事項

⚠️ **重要提醒**

- 請遵守學校選課規定，合理使用此工具
- 建議在選課時段前測試確保功能正常
- 確保網路連線穩定
- 不要關閉或操作連接的瀏覽器視窗

## 技術細節

- **語言**: Python 3.x
- **主要套件**: Selenium, WebDriver Manager
- **瀏覽器**: Google Chrome

## License

此專案僅供學習和個人使用。
