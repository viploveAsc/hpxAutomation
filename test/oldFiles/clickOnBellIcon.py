import pyautogui
import time
import subprocess
import os

# Correct way to launch UWP app using explorer.exe
app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"

subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)

# Wait for app to open fully
time.sleep(15)
print("Waiting for bell icon to appear...")


# Screenshot folder path
screenshot_path = "screenshot/"

# Locate bell icon on screen
location = pyautogui.locateCenterOnScreen(screenshot_path + "bell_icon.png", confidence=0.8)

if location:
    pyautogui.moveTo(location)
    pyautogui.click()
    print("Clicked on bell icon!")
else:
    print("Bell icon not found!")


# 4. Close the myHP app using taskkill
print("Closing myHP app...")
os.system("taskkill /f /im myHP.exe") # Sometimes it's `myhp.exe`, adjust if needed

def verify_user_profile():
    if pyautogui.locateOnScreen(screenshot_path +'viplove_email.png', confidence=0.9):
        print("✅ User email displayed.")
    else:
        print("❌ User email not found.")

    if pyautogui.locateOnScreen(screenshot_path +'viplove_name.png', confidence=0.9):
        print("✅ User name displayed.")
    else:
        print("❌ User name not found.")

def click_menu_option(option_image):
    location = pyautogui.locateOnScreen(option_image, confidence=0.9)
    if location:
        pyautogui.click(pyautogui.center(location))
        print(f"✅ Clicked on {option_image}")
    else:
        print(f"❌ {option_image} not found.")

# Usage:
click_menu_option(screenshot_path +'account.png')
click_menu_option(screenshot_path +'support.png')
click_menu_option(screenshot_path +'settings.png')


def verify_battery_status():
    if pyautogui.locateOnScreen(screenshot_path +'charging_97.png', confidence=0.9):
        print("✅ Battery status displayed correctly.")
    else:
        print("❌ Battery status not found.")

def close_hp_app_ui():
    close_btn = pyautogui.locateOnScreen(screenshot_path +'close_btn.png', confidence=0.9)
    if close_btn:
        pyautogui.click(pyautogui.center(close_btn))
        print("✅ Clicked Close button.")
    else:
        print("❌ Close button not found.")


def click_feedback():
    feedback_btn = pyautogui.locateOnScreen(screenshot_path +'send_feedback.png', confidence=0.9)
    if feedback_btn:
        pyautogui.click(pyautogui.center(feedback_btn))
        print("✅ Clicked on Send feedback.")
    else:
        print("❌ Send feedback button not found.")
