import subprocess

import time
import pyautogui

# Correct way to launch UWP app using explorer.exe
app_id = "AD2F1837.myHP_v10z8vjag6ke6!App"

subprocess.Popen(f'explorer shell:AppsFolder\\{app_id}', shell=True)

time.sleep(5)
screenshot = pyautogui.screenshot()
screenshot.save("launched_app.png")
print("Launched MyHP app successfully!")
