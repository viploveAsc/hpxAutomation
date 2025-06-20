from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# STEP 1: Ensure Chrome is already started externally or via subprocess
# Example (already launched before this step):
# subprocess.Popen(r'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"', shell=True)

# STEP 2: Connect Selenium to the existing session
options = Options()
options.debugger_address = "localhost:9222"

driver = webdriver.Chrome(options=options)

# STEP 3: Wait for the page to load
time.sleep(5)

# STEP 4: Verify current page
current_url = driver.current_url
if "account.hp.com/us/en/profile" in current_url:
    print("✅ HP Account Profile page is open.")
else:
    print(f"⚠️ Unexpected page: {current_url}")

# STEP 5: Optionally verify a page element (like the Profile menu or icon)
try:
    element = driver.find_element(By.XPATH, "//span[text()='Profile']")
    print("✅ Profile element found.")
except:
    print("❌ Profile element not found.")

# Don't quit driver if you want the session to continue
# driver.quit()
