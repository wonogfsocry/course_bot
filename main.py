import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- 設定區 ---
# 請依照你截圖中的課號修改
# 截圖1顯示線性代數是 B5701S60，截圖2報錯的是 B57040QM，請確認你要搶哪一門
TARGET_COURSE_ID = "B5704M22" 

# --- 連接現有瀏覽器 ---
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 連接瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("成功連接到瀏覽器！")

def grab_course():
    try:
        # 遍歷所有分頁，切換到標題包含 "選課" 或特定關鍵字的頁面
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "海洋大學" in driver.title: # 請替換成你學校選課系統實際的標題關鍵字
                print(f"已鎖定分頁: {driver.title}")
                break
        while True: # 無限迴圈
            try:
                print(f"[{time.strftime('%H:%M:%S')}] 正在掃描課程: {TARGET_COURSE_ID}...")

                # 1. 尋找按鈕
                xpath_locator = f"//tr[.//td[contains(text(), '{TARGET_COURSE_ID}')]]//a[text()='加選']"
                add_btn = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_locator))
                )
                
                # 2. 點擊按鈕
                print("!!! 發現目標，點擊加選 !!!")
                add_btn.click()

                # --- 階段一：處理「是否確定加選」的詢問 (如果有) ---
                try:
                    # 等待一下看有沒有第一個詢問視窗
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    # 不管內容是什麼，通常是確認，直接按接受
                    alert.accept()
                    print("已確認『是否加選』詢問")
                except TimeoutException:
                    # 有些系統不會問，直接送出，所以這裡沒抓到也沒關係
                    pass

                # --- 階段二：處理「加選結果」 (如：人數已達上限) ---
                try:
                    # 這裡要等久一點，因為伺服器處理需要時間
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    result_alert = driver.switch_to.alert
                    msg = result_alert.text
                    print(f"網頁回應結果: {msg}")

                    # 判斷結果內容
                    if "人數上限" in msg or "額滿" in msg:
                        print("❌ 課程已滿。執行等待策略...")
                        result_alert.accept() # 按下確定關閉彈窗
                        
                        print("⏳ 等待 10 秒後重試...")
                        time.sleep(10) # 你的要求：等待 10 秒
                        
                        print("🔄 重新整理頁面...")
                        driver.refresh() # 重整頁面以更新狀態
                        continue # 跳過下面程式碼，直接進入下一輪迴圈
                        
                    elif "衝堂" in msg:
                        print("⚠️ 衝堂警告。")
                        result_alert.accept()
                        # 衝堂通常不會因為重試而解決，這裡你可以選擇 break 停止或繼續
                        # 這裡暫時設定為繼續，避免因誤判而停止
                        time.sleep(2)
                        driver.refresh()
                        continue

                    else:
                        # 如果沒有出現「額滿」字眼，假設是成功或其他重要訊息
                        print("✅ 可能搶課成功！(或出現未預期訊息)")
                        print("程式將暫停，請人工確認。")
                        # 這裡不關閉彈窗，讓你親眼確認
                        break 

                except TimeoutException:
                    print("❓ 沒有收到結果彈窗，可能網頁還在跑或已經成功。")
                    driver.refresh()
                    continue # 重整後繼續下一輪

            except TimeoutException:
                # 找不到加選按鈕 (可能還沒釋出)
                print("找不到加選按鈕 (可能未釋出或網頁延遲)，重新整理...")
                time.sleep(2)
                driver.refresh()
                continue # 重整後繼續下一輪
            
            except Exception as e:
                print(f"發生錯誤: {e}")
                driver.refresh() # 錯誤時也重整頁面
                time.sleep(5) # 等待較長時間避免連續錯誤
                continue # 繼續下一輪
                
    except KeyboardInterrupt:
        print("使用者手動停止程式")

if __name__ == "__main__":
    grab_course()