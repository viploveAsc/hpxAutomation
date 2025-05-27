import pyautogui
import time
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pygetwindow as gw

# Optional: Configure Chrome options
# options = Options()
# options.add_argument("--start-maximized")  # Opens the browser in maximized mode
# # options.add_argument("--headless")       # Uncomment to run in headless mode
# options.debugger_address = "127.0.0.1:9222"

# Instantiate Chrome browser using Selenium Manager (built-in)
# driver = webdriver.Chrome(service=Service(), options=options)

# Launch UWP app
app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"
subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)

# Wait for app to open fully
time.sleep(5)
print("Waiting for bell icon to appear...")

# Screenshot folder path
screenshot_path = "screenshot/"

# Locate and click bell icon
bell_icon = pyautogui.locateCenterOnScreen(screenshot_path + "bell_icon.png", confidence=0.8)

if bell_icon:
    pyautogui.moveTo(bell_icon)
    pyautogui.click()
    print("Clicked on bell icon!")
    time.sleep(5)
    close_btn = pyautogui.locateCenterOnScreen(screenshot_path + "close_btn.png", confidence=0.7)
    pyautogui.moveTo(close_btn)
    pyautogui.click()
else:
    print("Bell icon not found!")

# # Kill app
# print("Closing myHP app...")
# os.system("taskkill /f /im myHP.exe")  # Adjust to 'myhp.exe' if needed


profile_icon = pyautogui.locateOnScreen(screenshot_path + 'profile_icon.png', confidence=0.7)
pyautogui.click(pyautogui.center(profile_icon))
time.sleep(5)

# ---------- FUNCTIONS ----------
def verify_user_profile():
    if pyautogui.locateOnScreen(screenshot_path + 'viplove_email.png', confidence=0.9):
        print("✅ User email displayed.")
    else:
        print("❌ User email not found.")

    if pyautogui.locateOnScreen(screenshot_path + 'viplove_name.png', confidence=0.9):
        print("✅ User name displayed.")
    else:
        print("❌ User name not found.")


def click_menu_option(image_name):
    full_path = screenshot_path + image_name
    location = pyautogui.locateOnScreen(full_path, confidence=0.8)
    if location:
        pyautogui.click(pyautogui.center(location))
        print(f"✅ Clicked on {image_name}")
    else:
        print(f"❌ {image_name} not found.")


def verify_battery_status():
    if pyautogui.locateOnScreen(screenshot_path + 'charging_97.png', confidence=0.8):
        print("✅ Battery status displayed correctly.")
    else:
        print("❌ Battery status not found.")


def close_hp_app_ui():
    close_btn = pyautogui.locateOnScreen(screenshot_path + 'close_btn.png', confidence=0.9)
    if close_btn:
        pyautogui.click(pyautogui.center(close_btn))
        print("✅ Clicked Close button.")
    else:
        print("❌ Close button not found.")


def click_feedback():
    time.sleep(2)
    profile_icon = pyautogui.locateOnScreen(screenshot_path + 'profile_icon.png', confidence=0.7)
    pyautogui.click(pyautogui.center(profile_icon))
    time.sleep(3)
    feedback_btn = pyautogui.locateOnScreen(screenshot_path + 'send_feedback.png', confidence=0.9)
    if feedback_btn:
        pyautogui.click(pyautogui.center(feedback_btn))
        print("✅ Clicked on Send feedback.")
    else:
        print("❌ Send feedback button not found.")

# ---------- USAGE ----------

click_menu_option('account.png')
# click_menu_option('support.png')
# click_menu_option('settings.png')
time.sleep(5)

# 3. Wait and detect if Chrome window with expected title is open
time.sleep(5)

windows = gw.getWindowsWithTitle('account.hp.com')  # fuzzy title matching
if windows:
    print("✅ Chrome window with expected title opened.")
else:
    print("❌ Chrome window not found.")
    