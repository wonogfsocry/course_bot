from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 1. 設定與你的 main.py 相同
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

print("--- 步驟 1: 連接瀏覽器 ---")
# 這裡為了單純化，直接用預設路徑，若報錯請補回你原本的 Service 設定
driver = webdriver.Chrome(options=options)
print("✅ 成功連接！")

# 2. 檢查當前控制的頁面資訊
print("\n--- 步驟 2: 檢查當前控制的頁面 ---")
print(f"當前分頁標題 (Title): {driver.title}")
print(f"當前分頁網址 (URL)  : {driver.current_url}")

# 3. 測試控制能力
print("\n--- 步驟 3: 測試動作 ---")
print("正在嘗試重新整理頁面...")
driver.refresh()
print("✅ 重新整理指令已發送 (請觀察瀏覽器是否有閃爍/重整)")

# 4. 如果標題不對，列出所有分頁
print("\n--- 步驟 4: 尋找正確的分頁 ---")
all_handles = driver.window_handles
print(f"偵測到共有 {len(all_handles)} 個分頁/視窗")

found_target = False
for handle in all_handles:
    driver.switch_to.window(handle)
    print(f"👉 切換到分頁: {driver.title}")
    # 這裡可以根據你的課程頁面關鍵字來判斷，例如 '選課' 或 'Course'
    if "選課" in driver.title or "Course" in driver.title:
        print("   (✨ 找到疑似目標頁面！)")
        found_target = True
        # 如果要在這裡測試，可以在這邊 break，並讓 driver 停留在這裡

if not found_target:
    print("❌ 未找到明顯的選課頁面，請確認你是否已手動開啟該網頁。")